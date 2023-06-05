#! python3
#! /usr/bin/python3
import serial
import Global as g
class OPM4201:
    def __init__(self):
        g.att4201 = g.opm4201 = 'Null'
        if g.resourceManager!=None:
            g.ASRL_List=g.resourceManager.list_resources('ASRL?*INSTR')
            for com in g.ASRL_List:
                if self.DetectOPM4201(com):
                    g.opm4201=com
                    break
            for com in g.ASRL_List:
                if self.DetectATT4201(com):
                    g.att4201=com
                    break
    def DetectOPM4201(self,com):
        tmp=com.replace('ASRL','COM')
        com=tmp.replace('::INSTR','')
        opm=serial.Serial(com, 115200, timeout=0.1)
        opm.write(b'\xAA\x03\x70\x00\x1D')
        try:
            s = opm.read(9)
        except:
            s = ''
        opm.close()
        if len(s)==9:
            if s[0:3]==b'\xAA\x07\x00':
                g.opm4201=com
                return True
        return False
    def DetectATT4201(self,com):
        tmp=com.replace('ASRL','COM')
        com=tmp.replace('::INSTR','')
        opm=serial.Serial(com, 115200, timeout=0.1)
        opm.write(b'\xAA\x06\x00\x52\x44\x57\x49\x01\xe7')
        try:
            s = opm.read(10)
        except:
            s = ''
        opm.close()
        if len(s)==10:
            if s[0:8]==b'\xAA\x07\x00\x52\x44\x57\x49\x01':
                g.att4201=com
                return True
        return False
