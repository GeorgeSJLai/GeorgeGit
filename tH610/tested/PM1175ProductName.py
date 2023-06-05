#! python3
#! /usr/bin/python3
import serial

opm=serial.Serial('COM6', 115200, timeout=0.1)     #COM6 PM1175 instrument
data = b'\xAA\x02\x78\x24'
print(data)
opm.write(data)
s = opm.read(10)
print(s)
#b'\xaa\x08\x78\x50\x4d\x31\x31\x37\x35\x95
#           x   P   M   1   1   7   5
# 

