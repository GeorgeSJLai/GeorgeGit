#! python3
#! /usr/bin/python3
import serial

opm=serial.Serial('COM6', 115200, timeout=0.1)     #COM6 pm1175/OPM4201 instrument
data = bytearray(b'\xAA\x03\x70\x00\x1D')
print(data)
opm.write(data)
s = opm.read(9)  
#b'\xaa\x07\x70\x00\xfb\x7d\xa3\xc2\xfe'
#             1   2   3   4   5   6   7
import struct
if len(s)==9:
    floatOPM = struct.unpack('f', s[4:-1])[0]
    print(s, floatOPM)
    opm.close()
else:
    print('Error：',s)
