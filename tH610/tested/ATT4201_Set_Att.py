#! python3
#! /usr/bin/python3
#ATT4201_Set_Att.vi
import serial
import struct
def chksum(data,dec1=0):
    sum=0
    for i in range(len(data)-dec1):
        sum+=data[i]
    sum &= 255
    return sum
#device=serial.Serial('COM19', 115200, timeout=0.1)   #COM5
Attenuation=10.0
#def Att4201SetAtt(device, Attenuation):

data = b'\xAA\x0A\x00\x53\x54\x41\x54\x01'     #加上\x0\x0\xB0\x40\xE1
data += struct.pack('f', Attenuation)
sum=chksum(data)
data += sum.to_bytes(1,'big')
print(data)   #b'\xaa\x0a\x00\x53\x54\x41\x54\x01\x00\x00\x20\x41\x52'
# device.write(data)
# s = opm.read(3)  
# num=s[2]*256+s[1]
# s2 = opm.read(num)
# if len(s2)!=num:
#     return -1   #error
# else
#     s+=s2
#     sum=chksum(s,dec1=1)
#     if sum.to_bytes(1,'big')==s[-1]:
#         return 0
#     else:
#         return -1

#b'\xaa\x06\x00\x53\x54\x57\x49\x00\xf7'

