#! python3
#! /usr/bin/python3
import serial
import Global as g
from ping3 import ping
import time, struct
import telnetlib
class Stelights:      #PM1175(COM6) / AT4301F(COM5)
    def __init__(self):

        self.pmSetWavLen=[4,bytearray(b'\xAA\x04\x57\x01\x03\x09')]
        self.pmGetPower=[9,bytearray(b'\xAA\x03\x70\x00\x1D')]
        self.WaveTable={'pm':('850nm','1300nm','1310nm','1490nm','1550nm','1625nm'),'at':('1270nm','1290nm','1310nm','1330nm','1490nm','1550nm')}
        self.PortID={'pm':None,'at':None}
        if g.resourceManager!=None:
            g.ASRL_List=g.resourceManager.list_resources('ASRL?*INSTR')
            ASRL_List=[]
            for com in g.ASRL_List:
                tmp=com.replace('ASRL','COM')
                comPort=tmp.replace('::INSTR','')
                ASRL_List.append(comPort)
            g.ASRL_List=[]
            for i in ASRL_List:
                g.ASRL_List.append(i)
            breakLoop=False;#print(g.ASRL_List)
            for comport in g.ASRL_List:
                for i in range(4):
                    try:
                        opm=serial.Serial(comport, 115200, timeout=0.2)
                        opm.write(b'\xAA\x02\x78\x24')
                        s = opm.read(10)
                        opm.close()
                    except:
                        s = ''                       
                    if s==b'\xaa\x08\x78\x50\x4d\x31\x31\x37\x35\x95':
                        ASRL_List.remove(comport)
                        breakLoop=True
                        print("PM1175 connected to ",comport)
                        self.PortID['pm']=comport #serial.Serial(comport, 115200, timeout=0.2)
                        break
                    else:
                        pass
                        #print('Error read string',s)
                    #print('Error read from %s：',comport)
                if breakLoop:
                    break
                # else:
                #     print(comport,'This device is not Stelight Instrument')
            #print(ASRL_List)
            breakLoop=False
            for comport in ASRL_List:
                for i in range(4):
                    try:
                        opm=serial.Serial(comport, 115200, timeout=0.3)
                        opm.write(b'\xAA\x05\x00\x52\x44\x50\x4E\xE3')
                        s = opm.read(14)
                        opm.close()
                    except:
                        s = ''
                    #print(s)
                    if s==b'\xaa\x0b\x00\x52\x44\x50\x4e\x41\x54\x34\x33\x30\x31\x46':
                        breakLoop=True
                        print("AT4301F connected to ",comport)
                        self.PortID['at']=comport#serial.Serial(comport, 115200, timeout=0.2)
                        break
                    else:
                        print('Error read string',s)
                if breakLoop:
                    break
    def SetDeviceFun(self,byteCmd,WTkey='pm',waveLength='1310nm'):
        portid=serial.Serial(self.PortID[WTkey], 115200, timeout=0.2)
        byteCmd[1][byteCmd[0]]=self.WaveTable[WTkey].index(waveLength)+1
        byteCmd[1][-1]=self.chksum(byteCmd[1],1)
        portid.write(byteCmd[1])
        portid.close()
    def GetDeviceFun(self,byteCmd,WTkey='pm'):
        portid=serial.Serial(self.PortID[WTkey], 115200, timeout=0.2)
        portid.write(byteCmd[1])
        s=portid.read(byteCmd[0])
        
        if len(s)==byteCmd[0]:
            floatOPM = struct.unpack('f', s[4:-1])[0]
            print(s, floatOPM)
            portid.close()
            return floatOPM
        else:
            print('Error：',s);return -999


        
    def chksum(self,data,dec1=0):
        sum=0
        for i in range(len(data)-dec1):
            sum+=data[i]
        sum &= 255
        return sum
class ONU_Hx10:    #192.168.1.1 / H510 / H610
    def __init__(self):
        self.resetGPON=[' Reset GPON。',b'diag',b'pbt rstgpon',5000,b'exit',500,
            b'rtkbosa -b /var/config/rtkbosa_k_bin',2000,b'reboot']
        self.PRBS31_TX1244RX2488=['A',b'\n',100,b'flash set PON_MODE 1',100,
            b'diag',100,b'register set 0x40094 0x40af',100,
            b'register set 0x40098 0x1',100,b'exit']
        self.ONU_tn=None
    # def ResetGPONfun(self):
    #     if self.ONU_tn==None:
    #         return False
    #     self.tnProc(self.resetGPON)
    #     return True
    def tnProc(self,cmdList):
        typeI=type(123)
        typeB=type(b'A')
        OK=True
        for i in cmdList:
            if cmdList.index(i)==0:
                continue
            elif type(i)==typeI:
                time.sleep(i/1000)
            elif type(i)==typeB:
                try:
                    self.ONU_tn.write(i+b'\n')
                except:
                    OK=False
        return OK
    def openONU(self, ip, port=23):
        typeFloat=type(0.6)
        print('Pinging ONU(H510/H610) ip address.')
        second = ping(ip)
        if(type(second)==typeFloat):
            self.ONU_tn=telnetlib.Telnet(ip, port)
            return True
        else:
            self.ONU_tn=None
            print('ONU IP not found at ethernet.')
            return False
    
class DCAinstrument:      #DCA-x 86100D
    def __init__(self,USBtext,USB_List,DCA_List):
        self.flex=self.findDevice(USBtext,USB_List,DCA_List)
        self.WavLen=('850nm','1310nm','1550nm')            #DCA86100D wavelength=
        #             1       2        3
    
    def findDevice(self,USBtext,USB_List,DCA_List):
        device=USB_List[0] if USBtext[7]=='✔' else DCA_List[0]    #device 
        if g.resourceManager==None:
            return None
        return g.resourceManager.open_resource(device)

