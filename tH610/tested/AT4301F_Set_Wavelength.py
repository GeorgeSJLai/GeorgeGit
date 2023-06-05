#! python3
#! /usr/bin/python3
#AT4301 / VOA：StelightVOA串口指令手册.pdf
import serial
waveLen=(1270,1290,1310,1330,1490,1550) #單位：nm
opm=serial.Serial('COM19', 115200, timeout=0.1)
data = b'\xAA\x07\x00\x53\x54\x57\x49\x01\x04\xFD'
#                                         ^^^
waveLen={1270:0,1290:1,1310:2,1330:3,1490:4,1550:5} #單位：nm
print(data)
opm.write(data)
s = opm.read(9)  
#b'\xaa\x06\x00\x53\x54\x57\x49\x00\xf7'
#import struct
#floatOPM = struct.unpack('f', s[4:-1])[0]
print(s)
opm.close()
