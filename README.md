# pycan

A Python module for implementing a UDS (Unified Diagnostic Services) + ISO-TP (ISO 15765-2) stack for automotive diagnostics.

## Installation

You can install the module using `pip`:

```bash
pip install pycan
```


## Usage
```python
from pycan import ISOTP, UDS

def bytearray2hex(d):
    return " ".join("{:02X}".format(x) for x in d)

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