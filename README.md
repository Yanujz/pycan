---
hide:
  - navigation
  - toc
---

# pycan

A Python module for implementing a UDS (Unified Diagnostic Services) + ISO-TP (ISO 15765-2) stack for automotive diagnostics.

## Installation

You can install the module using `pip`:

```bash
pip install pycan
```


## Usage
```py title="example.py"
from pycan import ISOTP, UDS

def bytearray2hex(d):
    return " ".join("{:02X}".format(x) for x in d)

def recv(id):
    ret = None

    # Peripheral logic here

    return ret

def send(id, extended, fd, data):
    print("CAN TX    {:02X}|{}|{}|{}".format(id,
                                             "EXT" if extended else "NOEXT",
                                             "FD" if fd else "NOFD",
                                             bytearray2hex(data)))
    # Peripheral logic here

    return len(data)

def main():
    isotp = ISOTP(recv=recv,
                  send=send, 
                  fd=True)
    
    uds = UDS(rxid=0x718,       # Default configuration (can be changed on each function if supported)
              txid=0x710,       # Default configuration (can be changed on each function if supported)
              extended=False,   # Default configuration (can be changed on each function if supported) 
              recv=isotp.recv,  # Select here the lower layer in the stack
              send=isotp.send,  # Select here the lower layer in the stack
              fd=True)          # Default configuration (can be changed on each function if supported)

    print('Start routine')
    ret, data = uds.routineStart(0xaabb)
›    if ret:
        print("Positive response with value: {}".format(bytearray2hex(data)))
    
    print('Stop routine')
    ret, data = uds.routineStop(0xaabb)
    if ret:
        print("Positive response with value: {}".format(bytearray2hex(data)))
    
    print('Results routine')
    ret, data = uds.routineResult(0xaabb)
    if ret:
        print("Positive response with value: {}".format(bytearray2hex(data)))

if __name__ == '__main__':
    main()
```


## Roadmap
### Phase 1: Initial Setup

#### Step 1: Project Structure
- [x] Create the initial project structure.
    ```
    pycan/
    ├── pycan/
    │   ├── __init__.py
    │   ├── pyisotp.py
    │   ├── pyuds.py
    │   └── utility.py
    ├── setup.py
    └── README.md
    ```

#### Step 2: Implement CAN Interface
- [x] Write `can_interface.py` to handle basic CAN communication.

#### Step 3: Implement ISO-TP Layer
- [x] Write `pyisotp.py` to manage ISO-TP message fragmentation and reassembly.

#### Step 4: Implement UDS Protocol
- [x] Write `pyuds.py` to implement UDS over ISO-TP.

#### Step 5: Create Setup Script
- [x] Write `setup.py` for module packaging and installation.

#### Step 6: Write README
- [ ] Create a comprehensive `README.md` with installation and usage instructions.

### Phase 2: Development and Testing

#### Step 7: Develop Core Features
- [x] (0x10) Diagnostic Session Control.
- [x] (0x11) ECU Reset.
    - [x] (0x0) Hard Reset
    - [x] (0x1) Key OffOn
    - [x] (0x2) Soft Reset
    - [x] (0x3) Enable Rapid Power Shutdown
- [ ] (0x14) Clear Diagnostic Information.
- [ ] (0x19) Read DTCI nformation.
- [x] (0x22) Read Data By Identifier.
- [ ] (0x23) Read Memory By Address.
- [ ] (0x24) Read Scaling Data By Identifier.
- [x] (0x27) Security Access.
- [ ] (0x28) Communication Control.
- [ ] (0x29) Authentication.
- [ ] (0x2A) Read Data By Periodic Identifier.
- [ ] (0x2C) Dynamically Define Data Identifier.
- [x] (0x2E) Write Data By Identifier.
- [ ] (0x2F) Input Output Control By Identifier.
- [x] (0x31) RoutineControl.
    - [x]  (0x01) Start Routine
    - [x]  (0x02) Stop Routine
    - [x]  (0x03) Result Routine
- [x]  (0x34) Request Download
- [ ]  (0x35) Request Upload
- [x]  (0x36) Transfer Data
- [x]  (0x37) Request Transfer Exit
- [ ]  (0x38) Request File Transfer
- [ ]  (0x3D) Write Memory By Address
- [x]  (0x3E) Tester Present
- [ ]  (0x84) SecuredDataTransmission
- [x]  (0x85) Control DTC Setting
- [ ]  (0x86) ResponseOnEvent
- [ ]  (0x87) LinkControl

#### Step 8: Unit Testing
- [ ] Write unit tests for `pyisotp.py`.
- [ ] Write unit tests for `pyuds.py`.

#### Step 9: Integration Testing
- [ ] Perform integration tests to ensure all components work together.

