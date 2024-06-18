from dataclasses import dataclass


@dataclass
class CanMessage:
    def __init__(self,
                 timestamp,
                 id: int,
                 extended: bool,
                 data: bytearray,
                 fd: bool = False):
        self._timestamp = timestamp
        self._id = id
        self._extended = extended
        self._data = data
        self._fd = fd

    def timestamp(self):
        return self._timestamp

    def id(self):
        return self._id

    def extended(self):
        return self._extended

    def data(self):
        return self._data

    def fd(self):
        return self._fd
