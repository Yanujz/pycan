from collections.abc import Callable
from .datatypes import CanMessage
from time import time, sleep
from typing import Tuple
from enum import Enum


class UDS:
    def __init__(self,
                 rxid: int,
                 txid: int,
                 extended: bool,
                 recv: Callable[[int, int], bytearray],
                 send: Callable[[bytearray, int, int, bool, bool, ], int],
                 fd: bool = False):
        self._rxid = rxid
        self._txid = txid
        self._extended = extended
        self._recvFn = recv
        self._sendFn = send
        self._fd = fd

    # Diagnostic Session Control
    def setSession(self, v: int,
                   timeout: int = 2,
                   waitResponse=True,
                   txid: int = None,
                   rxid: int = None,
                   extended: bool = None,
                   fd: bool = None) -> Tuple[bool, bytearray]:
        assert isinstance(v, int), "The session value must be an integer."

        payload = bytearray([0x10, v])

        if self._sendFn is None:
            return False, []

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x10 + 0x40, 2, 3)
            return ret, data
        else:
            return True, []

    # ECU Reset
    class ResetType:
        HARD_RESET = 0x01
        KEY_OFF_ON_RESET = 0x02
        SOFT_RESET = 0x03
        ENABLE_RAPID_POWER_SHUT_DOWN = 0x04
        DISABLE_RAPID_POWER_SHUT_DOWN = 0x05

    def reset(self,
              v: ResetType | int,
              timeout: int = 2,
              waitResponse=True,
              txid: int = None,
              rxid: int = None,
              extended: bool = None,
              fd: bool = None) -> Tuple[bool, bytearray]:
        assert isinstance(v, (UDS.ResetType, int)
                          ), "v must be of type ResetType or int"

        payload = bytearray([0x11, v])

        if self._sendFn is None:
            return False, []

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x11 + 0x40, 2, 3)
            return ret, data
        else:
            return True, []

    # Security Access
    def requestSeed(self,
                    level: int,
                    timeout: int = 2,
                    waitResponse=True,
                    txid: int = None,
                    rxid: int = None,
                    extended: bool = None,
                    fd: bool = None) -> Tuple[bool, bytearray]:
        assert isinstance(level, int), "The level value must be an integer."
        assert level % 2 != 0, "The number must be an odd integer"

        payload = bytearray([0x27, level])

        if self._sendFn is None:
            return False, []

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x27 + 0x40, 2, 3)
            return ret, data
        else:
            return True, []

    def sendKey(self,
                level: int,
                key: bytearray,
                timeout: int = 2,
                waitResponse=True,
                txid: int = None,
                rxid: int = None,
                extended: bool = None,
                fd: bool = None) -> Tuple[bool, bytearray]:
        assert isinstance(level, int), "The level value must be an integer."
        assert level % 2 == 0, "The number must be an even integer"

        payload = bytearray([0x27, level])

        if self._sendFn is None:
            return False, []

        payload += key

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x27 + 0x40, 2, 3)
            return ret, data
        else:
            return True, []

    # Tester present
    def testerPresent(self,
                      timeout: int = 2,
                      waitResponse=True,
                      txid: int = None,
                      rxid: int = None,
                      extended: bool = None,
                      fd: bool = None) -> Tuple[bool, bytearray]:
        payload = bytearray([0x3E, 0x00])

        if self._sendFn is None:
            return False, []

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x3E + 0x40, 1, 3)
            return ret, data
        else:
            return True, []

    # Read Data By Identifier
    def readDataByIdentifier(self,
                             id: int,
                             params: bytearray = None,
                             timeout: int = 2,
                             waitResponse=True,
                             txid: int = None,
                             rxid: int = None,
                             extended: bool = None,
                             fd: bool = None) -> Tuple[bool, bytearray]:
        payload = bytearray([0x22])
        if self._sendFn is None:
            return False, []

        payload += self._int2bytes(id)

        if params:
            payload += params

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x22 + 0x40, 3, 3)
            return ret, data
        else:
            return True, []

    def writeDataByIdentifier(self,
                              id: int,
                              params: bytearray = None,
                              timeout: int = 2,
                              waitResponse=True,
                              txid: int = None,
                              rxid: int = None,
                              extended: bool = None,
                              fd: bool = None) -> Tuple[bool, bytearray]:
        payload = bytearray([0x2E])
        if self._sendFn is None:
            return False, []

        payload += self._int2bytes(id)

        if params:
            payload += params

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x2E + 0x40, 3, 3)
            return ret, data
        else:
            return True, []

    # Routine Control
    def routineStart(self,
                     id: int,
                     params: bytearray = None,
                     timeout: int = 2,
                     waitResponse=True,
                     txid: int = None,
                     rxid: int = None,
                     extended: bool = None,
                     fd: bool = None) -> Tuple[bool, bytearray]:
        return self._routineControl(1, id, params, timeout,
                                    waitResponse, txid, rxid, extended, fd)

    def routineStop(self,
                    id: int,
                    #  params: bytearray = None,
                    timeout: int = 2,
                    waitResponse=True,
                    txid: int = None,
                    rxid: int = None,
                    extended: bool = None,
                    fd: bool = None) -> Tuple[bool, bytearray]:
        return self._routineControl(2, id, None, timeout,
                                    waitResponse, txid, rxid, extended, fd)

    def routineResult(self,
                      id: int,
                      #  params: bytearray = None,
                      timeout: int = 2,
                      waitResponse=True,
                      txid: int = None,
                      rxid: int = None,
                      extended: bool = None,
                      fd: bool = None) -> Tuple[bool, bytearray]:
        return self._routineControl(3, id, None, timeout,
                                    waitResponse, txid, rxid, extended, fd)
# private

    def _routineControl(self,
                        type: int,
                        id: int,
                        params: bytearray = None,
                        timeout: int = 2,
                        waitResponse=True,
                        txid: int = None,
                        rxid: int = None,
                        extended: bool = None,
                        fd: bool = None) -> Tuple[bool, bytearray]:
        assert isinstance(id, int), "The id value must be an integer."

        payload = bytearray([0x31, type])
        if self._sendFn is None:
            return False, []

        payload += self._int2bytes(id)

        if params:
            payload += params

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x31 + 0x40, 4, 3)
            return ret, data
        else:
            return True, []

    def eraseMemory(self,
                    addr: int,
                    size: int,
                    timeout: int = 5,
                    waitResponse=True,
                    txid: int = None,
                    rxid: int = None,
                    extended: bool = None,
                    fd: bool = None) -> Tuple[bool, bytearray]:
        id = 0xFF00

        params = bytearray([0x44])

        for i in range(4):
            params.append((addr >> (24 - i*8)) & 0xFF)

        for i in range(4):
            params.append((size >> (24 - i*8)) & 0xFF)

        return self.routineStart(id, params, timeout, waitResponse, txid, rxid, extended, fd)

    # Request Download
    def requestDownload(self,
                        addr: int,
                        size: int,
                        fmt: int = 0,
                        timeout: int = 5,
                        waitResponse=True,
                        txid: int = None,
                        rxid: int = None,
                        extended: bool = None,
                        fd: bool = None) -> Tuple[bool, bytearray]:
        
        payload = bytearray([0x34, fmt, 0x44])
        if self._sendFn is None:
            return False, []

        for i in range(4):
            payload.append((addr >> (24 - i*8)) & 0xFF)

        for i in range(4):
            payload.append((size >> (24 - i*8)) & 0xFF)

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x34 + 0x40, 1, 3)
            return ret, data
        else:
            return True, []

    # Trasnfer Data
    def transferData(self,
                     seq: int,
                     data : bytearray, 
                     timeout: int = 2,
                     waitResponse=True,
                     txid: int = None,
                     rxid: int = None,
                     extended: bool = None,
                     fd: bool = None) -> Tuple[bool, bytearray]:
        payload = bytearray([0x37, seq])
        
        if self._sendFn is None:
            return False, []
        
        payload += data

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x36 + 0x40, 1, 3)
            return ret, data
        else:
            return True, []
    
    # Request Transfer Exit
    def transferExit(self,
                     timeout: int = 2,
                     waitResponse=True,
                     txid: int = None,
                     rxid: int = None,
                     extended: bool = None,
                     fd: bool = None) -> Tuple[bool, bytearray]:
        payload = bytearray([0x37])

        if self._sendFn is None:
            return False, []

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x37 + 0x40, 1, 3)
            return ret, data
        else:
            return True, []

    # Control DTC Settings
    class DTCSettings:
        ON = 1,
        OFF = 2
            
    def controlDTCSettings(self,
                           v: int | DTCSettings,
                           timeout: int = 2,
                           waitResponse=True,
                           txid: int = None,
                           rxid: int = None,
                           extended: bool = None,
                           fd: bool = None) -> Tuple[bool, bytearray]:
        assert isinstance(v, (UDS.DTCSettings, int)), "v must be of type DTCSettings or int"

        payload = bytearray([0x85, v])

        if self._sendFn is None:
            return False, []

        txid = txid or self._txid
        rxid = rxid or self._rxid
        extended = extended or self._extended
        fd = fd or self._fd

        self._sendFn(payload, timeout, txid, extended, fd)

        if waitResponse:
            ret, data = self._handleResponse(rxid, 0x85 + 0x40, 2, 3)
            return ret, data
        else:
            return True, []
# private

    def _handleResponse(self, id, expectedPositiveResponse, offset=3, timeout=3):
        if self._recvFn:
            startTime = time()

            while 1:
                elapsed = (time() - startTime)

                if elapsed >= timeout:
                    print("uds timeout")
                    break

                data = self._recvFn(timeout, id)
                if data and len(data):
                    if expectedPositiveResponse == data[0]:
                        tmp = []

                        if offset <= len(data):
                            tmp = data[offset:]

                        return True, tmp
                    elif 0x7f == data[0]:
                        # we need to wait
                        if 0x78 == data[2]:
                            startTime = time()
                            pass
                        else:
                            return False, data[1:]
            return False, []

    def _int2bytes(self, int: int):
        from math import ceil, log

        return int.to_bytes(ceil(log(int)/log(256)))
