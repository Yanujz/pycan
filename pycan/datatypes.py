# Copyright 2024 Yanujz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
