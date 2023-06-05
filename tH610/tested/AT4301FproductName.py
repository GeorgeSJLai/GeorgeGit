#! python3
#! /usr/bin/python3
import serial

opm=serial.Serial('COM5', 115200, timeout=0.1)     #COM5 AT4301F instrument
data = b'\xAA\x05\x00\x52\x44\x50\x4E\xE3'
print(data)
opm.write(data)
s = opm.read(14)
print(s)
#b'\xaa\x0b\x00\x52\x44\x50\x4e\x41\x54\x34\x33\x30\x31\x46'
#               R   D   P   N   A   T   4   3   0   1   F
# import struct
# if len(s)==9:
#     floatOPM = struct.unpack('f', s[4:-1])[0]
#     print(s, floatOPM)
#     opm.close()
# else:
#     print('Error：',s)
