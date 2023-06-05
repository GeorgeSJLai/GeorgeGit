#
#變數定義區PBG230412140958
#             yymmddHHMMSS
import pyvisa
import Global as g
class VisibleObj:
    def __init__(self,Visible,Logic):
        self.Visible=Visible
        self.Logic=Logic
class BGColorObj:
    def __init__(self,BGColor,Text):
        self.BGColor=BGColor
        self.Text=Text

Judgement=BGColorObj(13816530,'')
StartKey=VisibleObj(True,False)    #START
Tab_CTRL_case=('initialize','TX_Adj/Cal','RX_Check/Cal','DDM')
#               0            1            2              3
Tab_control=Tab_CTRL_case.index('initialize')
Text={'SN':''}
Text['Statement']=''
Logic={'1. Set PRBS output':False}
Logic['2. initialize Oscilloscope']=False
Logic['3. Compensate Fiber Loss']=False
Logic['4. TX PWR Adjust']=False
Logic['5. TX PWR Cal']=False
Logic['6. E R Adjust']=False
Logic['7. Mask Margin']=False
Logic['8. TX Disable']=False
Logic['9. RX PWR Cal']=False
Logic['10. SD Level']=False
Logic['11. Alarm']=False
Logic['12. Warm']=False
Logic['SCAN']=False
Logic['Assign an SN']=False
Logic['Reset GPON']=True
Logic['Engineer Mode']=True
Logic['H610']=True
wavelength=('850nm','1310nm','1550nm')
OPMwavelength=('1310nm','1490nm','1550nm')
ATTwaveLen=(1270,1290,1310,1330,1490,1550)
Filter=('155.52MBd','622.08MBd','1.25GBd','2.488832GBd','2.5GBd')
Mask=('STM8/OC-24','STM16/OC-48')
Mode=('Eye/Mask','Scope')
VOAerror='''
VOA problem. Folllow steps below:
1. Power cycle the VOA, 
2. Set VOA to remote mode, 
3. Close Labview, 
4. Run the GUI.
'''
VISA_ADDRESS = 'USB0::0x0957::0xBE18::K-86100D-50195::INSTR'
try:
    # Create a connection (session) to the instrument
    resourceManager = pyvisa.ResourceManager()
    session86100D = resourceManager.open_resource(VISA_ADDRESS)
except pyvisa.Error as ex:
    print('Couldn\'t connect to \'%s\', exiting now...' % VISA_ADDRESS)
    sys.exit()

#_86100D=VISA(IO.VISA_Resource['USB0::0x0957::0xBE18::K-86100D-50195::INSTR'])


if Engineering_Mode:
    START['Visible']=True
    Tab_control=Tab_CTRL_case['initialize']
else:
    START['Visible']=False
    Tab_control=Tab_CTRL_case['TX_Adj/Cal']


while True:
    ONU_Address='192.168.1.1'
    if Tab_control==Tab_CTRL_case['initialize']:    #0
        if START['PushOn']:
            if Assign_an_SN:
                pass
            #Block 0
            elif Reset_GPON:
                #State:0
                Statement='Reset GPON'
                telnet:diag, pbt rstgpon, sleep 5000
                telnet:exit, sleep 500
                telnet rtkbosa -b /var/config/rtkbosa_k_bin,sleep 2000
                telnet:reboot
                #State:1
                Statement='reboot'
                #State:2
                for i in range(91):
                    Statement='rebooting '+str(90-i)+'s'
                    sleep(1)   #1 sec
                    if i==10:
                        VISA-Write:(_86100D,"ACQ:CDIS")
                #State:3
                Reset_GPON=False
                Statement['Visible']=True
                if Assign_SN:
                    SN=""
                else:
                    SN=input("input SN string")
            #Block 1
            connectID=telnet(ONU_Address)
            PRBS31_Status=Set_PRBS31_TX1244RX2488_TCP_2(connectID)
            VISA86100D_resource=VISA(_86100D)
            _86100D_Reset(VISA86100D_resource)   #VISA-Write:(_86100D,"*rst")
            sleep 500
            _86100D_Set_CH1_Wavelength(VISA86100D_resource,wavelength.index('1310nm'))    #chan1:wav wav2
            _86100D_Set_CH1_Filter(VISA86100D_resource,Filter['1.25GBd'])                 #chan1:fsel filter3     chan1:filt on
            _86100D_Set_CH1_Mask(VISA86100D_resource,Mask['STM8/OC-24'])                  
            #mtest1:load:fnam "%DEMO_DIR%\Masks\SONET_SDH\001.24416 - STM008_OC24.mskx"
            #mtest1:load
            #mtest1:load
            #mtes1:marg:meth auto
            #mtes1:marg:stat on
            _86100D_Change_Mode(VISA86100D_resource,Mode['Eye/Mask'])
            #syst:mode eye
            ## -------blk0--------
            VISA_Write(VISA86100D_resource,'aut')      
            #aut
            sleep 3000
            Mask_Margin=_86100D_Query_Mask_Margin(VISA86100D_resource)
            #:meas:mtes:marg?
            #read 64
            _86100D_Measure_CH1_OPER(VISA86100D_resource)
            #meas:eye:apow:unit dbm
            #meas:eye:apow
            #meas:eye:cros
            #meas:eye:jitt:form pp
            #meas:eye:jitt
            #meas:eye:jitt:form rms
            #meas:eye:jitt
            Error_out=VISA_Write(VISA86100D_resource,'aut')      
            #aut
            Error_List=unbundle(Error_out)
            _2_initialize_Oscilloscope=~Error_List[0]
            _1_SetPRBS_output=(Mask_Margin>30) & PRBS31_Status
            #Block 2
            Optical_Power_Meter=VISA(IO.VISA_Resource['Optical_Power_Meter'])    #PM1175(COM6)
            Optical_Attenuator=VISA(IO.VISA_Resource['Attenuator'])              #AT4301F(COM5)
            OPM4201_Set_Wavelength(Optical_Power_Meter,OPMwavelength['1310nm'])
            messagebox('Connect DUT/H610 optical output to Optical Power Meter/光纖線')
            for i in range(3):
                try:
                    NumIndicator['ONU O/P']=OPM4201_Get_Power(Optical_Power_Meter)
                    GetOK2=True     #方塊2下方
                except:
                    GetOK2=False
                sleep(300)
            #Block 3
            AT4301_Set_Wavelength(Optical_Attenuator,ATTwaveLen[1490])
            ATT4201_Set_Att(Optical_Attenuator,10.0)
            OPM4201_Set_Wavelength(Optical_Power_Meter,OPMwavelength['1490nm'])
            messagebox('Connect Coupler input to Optical Power Meter/光纖線')
            for i in range(3):
                try:
                    NumIndicator['OLT O/P at ONU']=OPM4201_Get_Power(Optical_Power_Meter)+10.0
                    GetOK3=True     #方塊3中間
                except:
                    GetOK3=True
                    print(VOAerror)
                    return
                sleep(200)
            inRange3 = NumIndicator['OLT O/P at ONU']>=-8 and NumIndicator['OLT O/P at ONU']=<-6
            方塊3上方=inRange3 & GetOK3
            #Block 4
            if GetOK3:
                if BoolSwitch['86100D/DCA4201']:
                    pass
                else:
                    try:
                        _86100D=VISA(IO.VISA_Resource['USB0::0x0957::0xBE18::K-86100D-50195::INSTR'])
                        _86100D_Set_CH1_Externl_Attenuation(_86100D,10.64)    #chan1:att:dec10.64    chan1:att:stat:off
                        AvgPower = _86100D_Query_CH1_Average_Power(_86100D)   #meas:cgr:apow?    VISAread(64)
                        OverPower = NumIndicator['ONU O/P'] - AvgPower
                        InRange4 = OverPower < 12.0 and OverPower > 8.0
                        _86100D_Set_CH1_Externl_Attenuation(_86100D,OverPower)
                        _86100D_Auto_Scale(_86100D)
                        NumIndicator['Scope Exteral Att']=OverPower
                        方塊4_OK=True
                    except:
                        方塊4_OK=False
                    BoolIndicator['Compensate Fiber Loss'] = 方塊4_OK & 方塊2下方 & 方塊3上方 & InRange4
            #Block 5
            START['PushOn']=False
    elif Tab_control==Tab_CTRL_case['TX_Adj/Cal']:
        
                
            
            
def OPM4201_Get_Power(src,cmd=b'\xAA\x03\x70\x00\x1d'):
import serial

opm=serial.Serial('COM6', 115200)
data = b'\xAA\x03\x70\x00\x1D'
print(data)
opm.write(data)
s = opm.read(9)
print(s)
opm.close()

def Set_PRBS31_TX1244RX2488_TCP_2():
    ONU_tn.write(b'\n',100,b'flash set PON_MODE 1\n',100
    b'diag\n',100,b'register set 0x40094 0x40af\n',100,
    b'register set 0x40098 0x1\n',100,b'exit\n'
    


import pyvisa # PyVISA library
rm = visa.ResourceManager()
flex=rm.open_resource('TCPIP0::localhost::hislip0,4880::INSTR')
flex.query('*RST;*OPC?')
flex.write(':SYSTem:GTLocal')
flex.close()
