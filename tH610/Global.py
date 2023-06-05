import pyvisa
class VisibleObj:
    def __init__(self,Visible,Logic):
        self.Visible=Visible
        self.Logic=Logic
class BGColorObj:
    def __init__(self,BGColor,Text):
        self.BGColor=BGColor
        self.Text=Text
pickleFile=r'c:\users\george\H610.pickle'
Judgement=BGColorObj(13816530,'')
StartKey=VisibleObj(True,False)    #START
#Array變數
Tab_CTRL_case=('initialize','TX_Adj/Cal','RX_Check/Cal','DDM')
#               0            1            2              3
Tab_control=Tab_CTRL_case.index('initialize')
nIndicator={'ONU O/P':None,
'OLT O/P at ONU':None,
'Scope External Att':None,
'ONU_O/P':None,
'TX_PWR DDM':None,
'E.R. (dB)':None,
'Jitterpp+14rms':None,
'Mask Margin(%)':None,
'Crossing(%)':None,
'RX_PWR_DDM':None,
'SD Assert':None,
'SD Deassert':None }


nPlace=[]


Filter=('155.52MBd','622.08MBd','1.25GBd','2.488832GBd','2.5GBd')
Mask=('001.24416 - STM008_OC24.mskx"','002.48832 - STM016_OC48.mskx"')
selectMask=0
Mode=('eye','osc')
selectMode=0

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
VOAerror='''
VOA problem. Folllow steps below:
1. Power cycle the VOA, 
2. Set VOA to remote mode, 
3. Close Labview, 
4. Run the GUI.
'''  #'ASRL6::INSTR', 'ASRL18::INSTR', 'ASRL19::INSTR'
#VISA_ADDRESS = 'USB0::0x0957::0xBE18::K-86100D-50195::INSTR'
#DCA_ADDRESS = 'TCPIP0::127.0.0.1::8805::SOCKET'
try:
    resourceManager = pyvisa.ResourceManager()
except:
    resourceManager = None
ASRL_List = ['Null']
USB_List = ['USB0::0x0957::0xBE18::K-86100D-50195::INSTR']
DCA_List = ['TCPIP0::127.0.0.1::8805::SOCKET']
#PM1175 = 'Null'
#AT4301F = 'Null'
#Control = {'Assign a Serial No.':False,'Reset GPON':True,'Engineering':True,'H610':True,'Password':False}
ONU_IP_Address = '192.168.1.1'
SerialNo_='PBG230412140958'
ONU_tn = None