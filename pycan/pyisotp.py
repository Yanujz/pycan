from collections.abc import Callable
from .datatypes import CanMessage
from time import time, sleep


class ISOTP(object):
    def __init__(self,
                 recv: Callable[[int], CanMessage],
                 send: Callable[[int, bool, bool, bytearray], int],
                 rxid: int = 0x718,
                 txid: int = 0x710,
                 extended: bool = False,
                 fd: bool = False):
        self._rxid = rxid
        self._txid = txid
        self._extended = extended
        self._recvFn = recv
        self._sendFn = send
        self._fd = fd

    def recv(self, timeout=2, id=None):
        data = []
        ff = False
        multiFrameSize = 0

        if self._recvFn:
            if None == id:
                id = self._rxid
            startTime = time()
            while 1:
                elapsed = (time() - startTime)

                if elapsed >= timeout:
                    raise Exception("Rx Timeout")

                msg = self._recvFn(id)
                if msg is not None:
                    payload = msg.data()
                    payloadSize = len(payload)

                    # Invalid frame
                    frameType = -1

                    if payloadSize > 1:
                        frameType = (payload[0] >> 4) & 0xF

                    # Single Frame
                    if 0 == frameType:
                        size = payload[0] & 0xF
                        if 0 == size and self._fd and payloadSize > 2:
                            size = payloadSize[1]

                            if payloadSize - 2 >= size:
                                data = payload[2: 2 + size]
                                break

                        elif size >= 1 and size <= 7:
                            if payloadSize - 1 >= size:
                                data = payload[1: 1 + size]
                                break

                    # First frame
                    elif 1 == frameType and payloadSize > 2:
                        ff = True
                        multiFrameSize = (
                            payload[0] & 0xFF << 8 | payload[1] & 0xFF)

                        if 0 == multiFrameSize and self._fd:
                            # TODO: Handle the  size above 0xFFF
                            pass
                        else:
                            self._sendFlowControl()
                            data = payload[2:]
                            multiFrameSize -= len(payload[2:])

                    # Consecutive frame
                    elif 2 == frameType and True == ff:
                        startTime = time()
                        tmp = payload[1:]

                        if multiFrameSize > len(tmp):
                            data += tmp
                            multiFrameSize -= len(tmp)
                        else:
                            data += tmp[0: multiFrameSize]
                            multiFrameSize = 0

                        if 0 == multiFrameSize:
                            ff = False
                            break

                    # Flow control
                    elif 3 == frameType:
                        data = payload
                        break
        return data

    def send(self, data, timeout=2, id=None, extended=None, fd=None):
        extended = extended or self._extended
        fd = fd or self._fd

        size = len(data)
        if fd and size >= 8:
            self._sendFD(data, size, timeout, id)
        else:
            self._send(data, size, timeout, id)

# private
    def _sendFD(self, data, size, timeout, id=None):
        if size >= 8 and size < 63:
            self._sendSingleFrameFD(data, size, id)
        elif size >= 63:
            self._sendMultiFrameFD(data, size, timeout, id)

    def _sendSingleFrameFD(self, data, size, id=None):
        if self._sendFn:
            if None == id:
                id = self._txid

            arr = bytearray(self._getBuffSize(size + 2))
            arr[1] = size & 0x3F

            for i in range(size):
                arr[2 + i] = data[i]

            self._sendFn(id, self._extended, self._fd, arr)

    def _sendMultiFrameFD(self, data, size, timeout, id=None):
        if self._sendFn:
            if None == id:
                id = self._txid

            byteSent = 0

            self._sendFirstFrameFD(data, size)

            byteSent += 62

            # wait for flow control
            flags, blockSize, separationTime = self._waitForFlowControl(
                timeout)

            sleep(separationTime // 1000)

            seq = 0
            blockCount = 0
            while 1:
                toIdx = (byteSent + 63)

                if toIdx > size:
                    toIdx = size

                arr = bytearray(self._getBuffSize(toIdx - byteSent))
                seq = (seq + 1) % 0x10

                if blockSize != 0 and blockCount == blockSize:
                    blockCount = 0
                    # wait for flow control
                    flags, blockSize, separationTime = self._waitForFlowControl(
                        timeout)

                arr[0] = 0x20 | (seq & 0xF)
                arrIdx = 1

                for i in range(byteSent, toIdx):
                    arr[arrIdx] = data[i]
                    arrIdx += 1

                self._sendFn(id, self._extended, self._fd, arr)

                if 0 != blockSize:
                    blockCount += 1

                byteSent += toIdx - byteSent

                if size == byteSent:
                    break

                sleep(separationTime // 1000)

    def _sendFirstFrameFD(self, data, size, id=None):
        if self._sendFD:

            if None == id:
                id = self._txid

            arr = bytearray(64)

            arr[0] = 0x10

            if (size >= 8) and (size <= 0xFFF):
                arr[0] = (1 << 4) | ((size & 0xFFF) >> 8)
                arr[1] = size & 0xFF

                for i in range(min(62, size)):
                    arr[2 + i] = data[i]

                self._sendFn(id, self._extended, self._fd, arr)
            elif size > 0xFFF:
                arr[0] = 0x10
                arr[1] = 0x00

                # Set the next 4 bytes as the size in high byte first order
                for i in range(4):
                    arr[2 + i] = (size >> (24 - i*8)) & 0xFF

                # Copy the data
                for i in range(60):
                    arr[6 + i] = data[i]

                self._sendFn(id, self._extended, self._fd, arr)

    def _send(self, data, size, timeout, id=None):
        if size > 0 and size < 8:
            self._sendSingleFrame(data, size, id)
        elif size >= 8:
            self._sendMultiFrame(data, size, timeout, id)

    def _sendFlowControl(self, flag=0, blockSize=0, separationTime=0, id=None):
        if self._sendFn:
            arr = bytearray(8)
            arr[0] = 0x30 | (flag & 0x3)
            arr[1] = blockSize

            if None == id:
                id = self._txid

            self._sendFn(id, self._extended, self._fd, arr)

    def _sendSingleFrame(self, data, size, id=None):
        if self._sendFn:
            arr = bytearray(8)
            arr[0] = size & 0xFF

            for i in range(size):
                arr[1 + i] = data[i]

            if None == id:
                id = self._txid

            self._sendFn(id, self._extended, self._fd, arr)

    def _sendMultiFrame(self, data, size, timeout, id=None):
        if self._sendFn:
            arr = bytearray(8)

            if None == id:
                id = self._txid

            byteSent = 0

            # Preparing the first frame
            arr[0] = (1 << 4) | ((size & 0xFFF) >> 8)
            arr[1] = size & 0xFF

            for i in range(6):
                arr[2 + i] = data[i]

            byteSent += self._sendFn(id, self._extended, self._fd, arr)

            # wait for flow control
            flags, blockSize, separationTime = self._waitForFlowControl(
                timeout)

            sleep(separationTime // 1000)

            seq = 0
            blockCount = 0
            while 1:
                arr = bytearray(8)
                seq = (seq + 1) % 0x10

                if blockSize != 0 and blockCount == blockSize:
                    blockCount = 0
                    # wait for flow control
                    flags, blockSize, separationTime = self._waitForFlowControl(
                        timeout)

                arr[0] = 0x20 | (seq & 0xF)
                arrIdx = 1
                toIdx = (byteSent + 7)

                if toIdx > size:
                    toIdx = size

                for i in range(byteSent, toIdx):
                    arr[arrIdx] = data[i]
                    arrIdx += 1

                self._sendFn(id, self._extended, self._fd, arr)

                if 0 != blockSize:
                    blockCount += 1

                byteSent += toIdx - byteSent

                if size == byteSent:
                    break

                sleep(separationTime // 1000)

    def _waitForFlowControl(self, timeout):
        startTime = time()

        while 1:
            elapsed = (time() - startTime)
            if elapsed >= timeout:
                raise Exception("Rx Timeout")

            if self._recvFn:
                msg = self._recvFn(self._rxid)

                if msg:
                    data = msg.data()
                    frameType = ((data[0] >> 4) & 0xF)
                    if 3 == frameType and len(data) >= 3:
                        return (data[0] & 0xF), data[1], data[2]

    def _getBuffSize(self, size):
        r = 0

        if size >= 0 and size <= 64:
            arr = [8, 8, 8, 8, 8, 8, 8, 8, 8,                                       #  0 -  8
                   12, 12, 12, 12,                                                  #  9 - 12
                   16, 16, 16, 16,                                                  # 13 - 16
                   20, 20, 20, 20,                                                  # 17 - 20
                   24, 24, 24, 24,                                                  # 21 - 24
                   32, 32, 32, 32, 32, 32, 32, 32,                                  # 25 - 32
                   48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,  # 33 - 48
                   64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64   # 49 - 64
                   ]

            r = arr[size]

        return r
