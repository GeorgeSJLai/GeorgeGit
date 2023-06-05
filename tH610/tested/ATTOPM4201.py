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
                    #g.opm4201=com
                    #print(g.opm4201)
                    break
            for com in g.ASRL_List:
                self.DetectATT4201(com)
                g.COM_List.append(com)
    def DetectOPM4201(self,com):
        tmp=com.replace('ASRL','COM')
        com=tmp.replace('::INSTR','')
        while True:
            try:
                opm=serial.Serial(com, 115200, timeout=0.3)
                opm.write(b'\xAA\x03\x70\x00\x1D')
                s = opm.read(9)
                opm.close()
            except:
                s = ''
                return False
            if len(s)==9:
                if s[0:3]==b'\xAA\x07\x00':
                    g.opm4201=com   # print(g.opm4201)
                    return True
            else:
                print('Error read from OPM4201：',s)
    def DetectATT4201(self,com):
        tmp=com.replace('ASRL','COM')
        com=tmp.replace('::INSTR','')
        # print(com)
        try:
            opm=serial.Serial(com, 115200, timeout=0.3)
            opm.write(b'\xAA\x06\x00\x52\x44\x57\x49\x01\xe7')
            s = opm.read(10)
            opm.close()
        except:
            s = ''
        if len(s)==10:
            if s[0:8]==b'\xAA\x07\x00\x52\x44\x57\x49\x01':
                g.att4201=com
                return True
        return False
