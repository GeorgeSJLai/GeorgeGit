#! python3
#! /usr/bin/python3
import serial

opm=serial.Serial('COM6', 115200)
data = b'\xAA\x03\x70\x00\x1D'
print(data)
opm.write(data)
s = opm.read(9)
print(s)
opm.close()
