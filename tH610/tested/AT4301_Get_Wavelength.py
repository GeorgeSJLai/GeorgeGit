#! python3
#! /usr/bin/python3
#AT4301 / VOA：StelightVOA串口指令手册.pdf
import serial
waveLen=(1270,1290,1310,1330,1490,1550) #單位：nm
opm=serial.Serial('COM19', 115200, timeout=0.1)
data = b'\xAA\x06\x00\x52\x44\x57\x49\x01\xe7'
#                                         
waveLen={1270:0,1290:1,1310:2,1330:3,1490:4,1550:5} #單位：nm
print(data)
opm.write(data)
s = opm.read(10)  
#b'\xAA\x07\x00\x52\x44\x57\x49\x01\x04\xec'    1490nm
print(s)
opm.close()
