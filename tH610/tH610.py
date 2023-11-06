
import tkinter as tk
from tkinter import INSERT,messagebox,ttk
from tkinter import simpledialog
#import tkinter.font as tkfont => for git test 000
import Devices,time,pickle,sys
import Global as g

class Application(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master=master;count=0
        while g.resourceManager==None and count<6:
            self.USB_List = ['USB0::0x0957::0xBE18::K-86100D-50195::INSTR']
            self.DCA_List = ['TCPIP0::127.0.0.1::8805::SOCKET'];count+=1
        else:
            if count<6:
                self.USB_List = g.resourceManager.list_resources('USB?*INSTR')
                self.USB_List = ['Null'] if len(self.USB_List)==0 else self.USB_List
                self.DCA_List = g.resourceManager.list_resources('TCP?*')
                if len(self.DCA_List)==0:
                    self.DCA_List = ['TCPIP0::127.0.0.1::8805::SOCKET']         #default value
        self.stelights = Devices.Stelights()
        self.ONU = Devices.ONU_Hx10()
        self.nOuter={}
        self.nIndicator=('ONU O/P'       ,'OLT O/P at ONU','Scope External Att.',            #0:3
                         'ONU_O/P'       ,'TX_PWR DDM'    ,'E.R. (dB)',                      #3:9
                          'Jitterpp+14rms','Mask Margin(%)','Crossing(%)',
                         'RX_PWR_DDM'    ,'SD Assert'     ,                                  #9:13
                         'SD Deassert'   ,'SD Hysteresis (dB)')    #13
        self.nBody=( ([None,60,220],[None,150,220],'light sky blue'),([None,270,220],[None,410,220],'light sky blue'),([None,530,220],[None,682,220],'light sky blue') , 
                     ([None,1,304],[None,95,304],'yellow'),([None,220,304],[None,348,304],'yellow'),([None,475,304],[None,560,304],'yellow'),
                     ([None,1,340],[None,130,340],'yellow'),([None,250,340],[None,390,340],'yellow'),([None,510,340],[None,620,340],'yellow') ,
                     ([None,1,462],[None,135,464],"light green"),([None,250,462],[None,345,464],"light green"),
                     ([None,1,492],[None,135,494],"light green"),([None,250,492],[None,405,494],"light green")  
                   )
        #self.nValue=[None]*len(self.nIndicator)
        self.nLogic=('Set PRBS output','Initialize Oscilloscope','Compensate Fiber Loss',      #0:3
                     'TX_PWR Adjust','TX_PWR Cal','E.R. Adjust','Mask Margin','TX Disable',    #3:8
                     'RX_PWR Cal','SD Level')                                                  #8:10
                    #'Alarm','Warn') #12                                                        10:12
        self.nLEDs=([None,154,180,'light sky blue'],[None,326,180,'light sky blue'],[None,522,180,'light sky blue'],
                    [None,174,260,'yellow'],[None,340,260,'yellow'],[None,490,260,'yellow'],[None,620,260,'yellow'],[None,765,260,'yellow'],
                    [None,210,420,"light green"],[None,370,420,"light green"] )    #[None,111,222,'salmon'],[None,333,444,'salmon'] 
        self.DDM_ColH=        ("Temp. (°C)",'Voltage (V)','Bias (mA)','TX_OP (mW)','RX_OP (mW)')
        self.DDM_RowH=("Alarm+",
                       "Warn+",
                       "Tested",
                       "Warn-",
                       "Alarm-") #https://docs.devexpress.com/OfficeFileAPI/images/spreadsheetcontrol_row_column_indexes19675.png
        self.DDM_Tabl=[(80,   4,   65,   3.981, 0.1995),   #rIdx=0 cIdx=0..4
                       (75,   3.5, 55,   3.5481,0.1584),   #rIdx=1 cIdx=0..4
                       [36.71,3.24,10.05,1.95,  0.1055],
                       (-8,   3.1, 1,    1,     0.0012),
                       (-13,  3,   0,    0.8912,0.001) ]   #rIdx=4 cIdx=0..4
        self.fgColor=('black','red','orange red','green','orange red','red')

        ################################ row 1 ################################
        self.l_usb = tk.Button(self.master)
        self.l_usb["text"] = "86100D【✔】"
        self.l_usb.place(x=146,y=0)
        self.l_usb.config(command=self.b86100DFunc)
        # self.bSelector = tk.Button(self.master) -----------------------------
        # self.bSelector["text"] = "Switch to DCA4201"
        # self.bSelector.place(x=250,y=0) -------------------------------------
        self.l_dca = tk.Button(self.master)
        self.l_dca["text"] = "DCA4201【　】"         # ✔
        self.l_dca.place(x=466,y=0)
        self.l_dca.config(command=self.bDCA4201Func)

        self.l_SN=tk.Label(self.master,text='S/N：',font='Helvetica 12 bold')
        self.l_SN.place(x=790,y=0)
        self.SN_Val=tk.Label(self.master,text=' '+g.SerialNo_+' ',bg="black",fg='yellow',font='Helvetica 12 bold')
        self.SN_Val.place(x=835,y=0)
        self.DCA = Devices.DCAinstrument(self.l_usb["text"],self.USB_List,self.DCA_List)
        ################################ row 2 ################################
        self.usb = tk.StringVar()
        self.usb.set(self.USB_List[0])
        self.optionUSB = tk.OptionMenu(self.master,self.usb,*self.USB_List)
        self.optionUSB.place(x=0,y=28)

        self.dca = tk.StringVar()
        self.dca.set(self.DCA_List[0])
        self.optionDCA = tk.OptionMenu(self.master,self.dca,*self.DCA_List)
        self.optionDCA.place(x=400,y=28)

        self.l_St=tk.Label(self.master,text='Statement：',font='Helvetica 13 bold')
        self.l_St.place(x=735,y=32)
        self.Statement=tk.Label(self.master,text=' 　　　　　　　　 ',bg="black",fg='yellow',font='Helvetica 13 bold')
        self.Statement.place(x=835,y=32)
        ################################ row 3 ################################
        self.ca=tk.Canvas(self.master,width=995,height=90,bg="pale green")  #------Line---------------
        self.ca.place(x=0,y=61)

        yy=55;self.l_ip = tk.Label(self.master,bg='pale green')
        self.l_ip["text"] = "ONU Address：" 
        self.l_ip.place(x=5,y=yy+14)
        
        self.entry = tk.Entry(self.master,width=15,bd=2)
        self.entry.insert(INSERT,g.ONU_IP_Address);#print(self.entry.get())
        self.entry.place(x=140,y=yy+14)
        ################################ row 4 ################################
        self.l_iq = tk.Label(self.master,bg='pale green')
        self.l_iq["text"] = "Optical Power Meter：" 
        self.l_iq.place(x=10,y=yy+44)
        
        self.v = tk.StringVar()
        self.v.set(self.stelights.PortID['pm'])
        self.optionmenu = tk.OptionMenu(self.master,self.v,*g.ASRL_List)
        self.optionmenu.place(x=180,y=yy+42)
        self.optionmenu.config(bg="pale green")
        self.v.trace("w",self.optionmenu_event)

        self.l_e63 = tk.Label(self.master,bg='pale green')
        self.l_e63["text"] = "Optical Attenuator：" 
        self.l_e63.place(x=295,y=yy+44)
        
        self.vv = tk.StringVar()
        self.vv.set(self.stelights.PortID['at'])  #print(g.PM1175,g.AT4301F)
        self.optionmenu2 = tk.OptionMenu(self.master,self.vv,*g.ASRL_List)
        self.optionmenu2.place(x=450,y=yy+42)
        self.optionmenu2.config(bg="pale green")
        self.vv.trace("w",self.optionmenu_event)
        ################################ row 5 ################################
        self.ca=tk.Canvas(self.master,width=995,height=60,bg="gold")  #------Line---------------
        self.ca.place(x=0,y=133)
        self.clickButton=('Assign a Serial No.','Reset GPON','Engineering','H610','Password')
        self.clickButtonArray=([None,None,8,139,self.AssignSNevent],[None,None,178,139,self.ResetGPONevent],
                               [None,None,307,139,self.Engineeringevent],[None,None,475,139,self.H610event],
                               [None,None,568,139,self.Passwordevent])  #tk.Checkbutton/BooleanVar
        self.clickButt()
        ################################ row 6 ################################
        self.ca=tk.Canvas(self.master,width=995,height=90,bg="light sky blue")  #------Line---------------
        self.ca.place(x=0,y=171)
        self.bStartInit = tk.Button(self.master,text="Start Initialize ▶",font=('Helvetica 14'),bg='White')   #,12))   #,style='W.TButton')
        self.bStartInit.place(x=0,y=177)
        self.bStartInit.config(command=self.StartInitFun)

        self.nNoLedFun(0,3)
        ################################ row 7 ################################
        self.nIndFun(0,3)
        ################################ row 8 ################################
        self.ca=tk.Canvas(self.master,width=995,height=170,bg="yellow")  #------Line---------------
        self.ca.place(x=0,y=250)
        
        self.bStartTxAdjCal = tk.Button(self.master,text="Start Tx Adj/Cal ▶",font=('Helvetica 14'),bg='White')    #Helvetica 14 underline
        self.bStartTxAdjCal.place(x=0,y=260)
        self.bStartTxAdjCal.config(command=self.StartTxAdjCalFun)
        self.nNoLedFun(3,8)
        ################################ row 9 /10 ################################
        self.nIndFun(3,9)
        ################################ row 11 ################################
        self.TxSpec=("O/P Target", "E.R.upper limit", "E.R.lower limit","Jitter upper limit")
        self.TxSpecBody=([None,1,376,None,100,380,0,9,0.1],[None,225,376,None,346,380,10,19,0.25],
                         [None,465,376,None,583,380,7,17,0.25],[None,710,376,None,840,380,200,356,1])
        self.TxSpecFun()
        ################################ row 12 ################################
        self.ca=tk.Canvas(self.master,width=995,height=120,bg="light green")  #pale green
        self.ca.place(x=0,y=410)

        self.bStartRxChkCal = tk.Button(self.master,text="Start Rx Check/Cal ▶",font=('Helvetica 14'),bg='White')
        self.bStartRxChkCal.place(x=0,y=420)
        self.bStartRxChkCal.config(command=self.StartRxChkCalFun)
        self.nNoLedFun(8,10)
        ################################ row 13 / 14 ################################
        self.nIndFun(9,13)
        ################################ row 15 ################################
        self.frame1=tk.Frame(self.master,bg='light cyan')     #bg='burlywood'/'light cyan'
        self.frame1.place(x=6,y=540)
        self.DDM_Build()
        

        # self.l00=tk.Entry(self.frame1,width=14,bg='light cyan',font=('Helvetica 14'),justify='center')
        # self.l00.grid(row=1,column=1,sticky=tk.NSEW)
        # self.l11=tk.Entry(self.frame1,width=14,bg='light cyan',font=('Helvetica 14'),justify='center')
        # self.l11.grid(row=2,column=2,sticky=tk.NSEW)
        # self.l22=tk.Entry(self.frame1,width=14,bg='light cyan',font=('Helvetica 14'),justify='center')
        # self.l22.grid(row=3,column=3,sticky=tk.NSEW)

    
    def DDM_Build(self):
        self.eArray=[[None]*(len(self.DDM_ColH)+1)]*(len(self.DDM_RowH)+1)
        self.DDM_Tabl[2]=self.readPickle(5)
        for rIdx in range(len(self.DDM_RowH)+1):
            for cIdx in range(len(self.DDM_ColH)+1):
                if rIdx==0:
                    if cIdx==0:
                        self.eArray[rIdx][cIdx]=tk.Button(self.frame1,text="Scan ▶",bg='White',width=14,font=('Helvetica 14'),justify='center') 
                        self.eArray[rIdx][cIdx].grid(row=0,column=0,sticky=tk.NSEW)
                    else:
                        self.eArray[rIdx][cIdx]=tk.Entry(self.frame1,width=14,bg='light cyan',font=('Helvetica 14'),justify='center')
                        self.eArray[rIdx][cIdx].insert(INSERT,self.DDM_ColH[cIdx-1])
                        self.eArray[rIdx][cIdx].grid(row=rIdx,column=cIdx,sticky=tk.NSEW)
                else:
                    if cIdx==0:
                        self.eArray[rIdx][cIdx]=tk.Entry(self.frame1,width=14,bg='light cyan',font=('Helvetica 14'),justify='center')
                        self.eArray[rIdx][cIdx].insert(INSERT,self.DDM_RowH[rIdx-1])
                        self.eArray[rIdx][cIdx].grid(row=rIdx,column=cIdx,sticky=tk.NSEW)
                    else:
                        self.eArray[rIdx][cIdx]=tk.Entry(self.frame1,width=14,bg='light cyan',font=('Helvetica 14'),justify='center',fg=self.fgColor[rIdx])
                        nV='---' if self.DDM_Tabl[rIdx-1][cIdx-1]==None else self.DDM_Tabl[rIdx-1][cIdx-1]
                        self.eArray[rIdx][cIdx].insert(INSERT,nV)
                        self.eArray[rIdx][cIdx].grid(row=rIdx,column=cIdx,sticky=tk.NSEW)

    def TxSpecFun(self):
        txspec=self.readPickle(2)   #type=float
        for i in self.TxSpec:
            n=self.TxSpec.index(i)
            self.TxSpecBody[n][0]=tk.Label(self.master,text=i+"：",font=('Helvetica',12),bg='yellow')
            x,y=self.TxSpecBody[n][1:3]
            self.TxSpecBody[n][0].place(x=x,y=y)
            self.TxSpecBody[n][3]=ttk.Spinbox(self.master,from_=self.TxSpecBody[n][6],to=self.TxSpecBody[n][7],increment=self.TxSpecBody[n][8],justify='center',width=10)
            self.TxSpecBody[n][3].insert(INSERT,str(txspec[n]))
            x,y=self.TxSpecBody[n][4:6]
            self.TxSpecBody[n][3].place(x=x,y=y)        
    def nNoLedFun(self,J,K):
        LedStatus=self.readPickle(3)
        for i in self.nLogic[J:K]:
            n=self.nLogic.index(i);#print(i)
            bgtmp=self.nLEDs[n][-1] if LedStatus[n]==None else ('green' if LedStatus[n] else 'red')
            fgtmp='black' if LedStatus[n]==None else 'white'
            self.nLEDs[n][0]=tk.Label(self.master,text=str(n+1)+'. '+i+" ? ",borderwidth=3,relief="ridge",bg=bgtmp,fg=fgtmp,font=('Helvetica',12))
            x,y=self.nLEDs[n][1:3]
            self.nLEDs[n][0].place(x=x,y=y)
    def nIndFun(self,J,K):
        self.nValue=self.readPickle(4)
        for i in self.nIndicator[J:K]:
            n=self.nIndicator.index(i);#print(i)
            nV='---' if self.nValue[n]==None else self.nValue[n]
            self.nBody[n][0][0]=tk.Label(self.master,text=i+' =',font=('Helvetica',12),bg=self.nBody[n][2])
            x,y=self.nBody[n][0][1:]
            self.nBody[n][0][0].place(x=x,y=y)
            self.nBody[n][1][0]=tk.Label(self.master,width=10,bg='black',fg='yellow',height=1,justify='center',text=nV,font=('Helvetica 12 bold'))
            x,y=self.nBody[n][1][1:]
            self.nBody[n][1][0].place(x=x,y=y)
    def readPickle(self,n):
        lenNominal=(5,4,10,13,5)
        with open(g.pickleFile,'rb') as f:
            try:
                for i in range(n):
                    tmp=pickle.load(f)
            except:
                messagebox.showerror("錯誤", g.pickleFile+" input data not enough!!!")
                quit()
        if len(tmp)!=lenNominal[n-1]:
            messagebox.showerror("錯誤", g.pickleFile+" data error!!!")
            sys.exit()
        return tmp
    def writePickle(self):
        cBA=[];txspec=[]
        for i in range(len(self.clickButtonArray)):
            cBA+=[self.clickButtonArray[i][1].get()]
        for i in range(len(self.TxSpecBody)):
            txspec+=[float(self.TxSpecBody[i][3].get())]

        # with open(g.pickleFile,'wb') as f:
        #     pickle.dump(cBA,f)
        #     pickle.dump(txspec,f)
    def clickButt(self):
        cBA=self.readPickle(1)
        for i in self.clickButton:
            n=self.clickButton.index(i)
            self.clickButtonArray[n][1]=tk.BooleanVar(value=cBA[n])          #value=False
            self.clickButtonArray[n][0]=tk.Checkbutton(self.master,text=self.clickButton[n],variable=self.clickButtonArray[n][1],onvalue=True,offvalue=False,command=self.clickButtonArray[n][4],bg='gold')
            x, y=self.clickButtonArray[n][2:4]
            self.clickButtonArray[n][0].place(x=x,y=y)

    def b86100DFunc(self):
        #if self.l_usb["text"][7]=='　':
        self.l_usb["text"] = "86100D【✔】"
        self.l_dca["text"] = "DCA4201【　】"
        self.nOuter['ONU O/P']['text']=456.78
    def bDCA4201Func(self):
        self.l_usb["text"] = "86100D【　】"
        self.l_dca["text"] = "DCA4201【✔】"
        print(self.nOuter['ONU O/P']['text'])
    def StartRxChkCalFun(self):
        pass
    def StartInitFun(self):
        self.bStartInit['bg']='green'
        self.bStartInit['fg']='white'
        if self.stelights.PortID['pm']==None or self.stelights.PortID['at']==None:
            messagebox.showerror("Unconnect!","PM1175 and AT4301F")
            return
        g.ONU_IP_Address=self.entry.get()
        
        if not self.ONU.openONU(g.ONU_IP_Address):
            messagebox.showerror("Unconnect!","ONU(H510/H610) device")
            return
        if self.DCA.flex==None:
            messagebox.showerror("Unconnect!","DCA-X 86100D device")
            return
        if g.Control['ResetGPON']:
            self.Statement['text']=self.ONU.resetGPON[0]
            self.ONU.tnProc(self.ONU.resetGPON)
            self.Statement['text']=' reboot。'
            for i in range(91):
                time.sleep(1)
                self.Statement['text']=' rebooting '+str(90-i)+'s'
                if i==80:  #and self.DCA.flex!=None:
                    self.DCA.flex.write('ACQ:CDIS\n')
            self.ResetGPON=tk.BooleanVar(value=False)    #☑⇒  ⃞   
            g.Control['ResetGPON']=False
            if not g.Control['AssignSN']:
                g.SerialNo_=' '+simpledialog.askstring('Assign', 'Assign an Serial Number')+' '
                self.SN_Val['text']=g.SerialNo_
        PRBS31_Status=self.ONU.tnProc(self.ONU.PRBS31_TX1244RX2488)
        try:
            self.DCA.flex.write('*rst\n')
            time.sleep(0.5)
            cmd='chan1:wav wav'+str(self.DCA.WavLen.index('1310nm')+1)+'\n';self.DCA.flex.write(cmd)
            cmd='chan1:fsel filter'+str(g.Filter.index('1.25GBd')+1)+'\n';self.DCA.flex.write(cmd)
            self.DCA.flex.write('chan1:filt on\n')
            #cmd='mtest1:load:fnam "%DEMO_DIR%\\Masks\\SONET_SDH\\'+g.Mask[g.selectMask]+'\n'
            cmd='mtest1:load:fnam "c:\\Program Files\\Keysight\\FlexDCA\\Demo\\Masks\\SONET_SDH\\'+g.Mask[g.selectMask]+'\n'
            self.DCA.flex.write(cmd)
            self.DCA.flex.write('mtest1:load\n')
            self.DCA.flex.write('mtest1:load\n')
            self.DCA.flex.write('mtes1:marg:meth auto\n')
            self.DCA.flex.write('mtes1:marg:stat on\n')
            self.DCA.flex.write('syst:mod'+g.Mode[g.selectMode]+'\n')  #syst:mod eye
            self.DCA.flex.write('aut\n')           #
            time.sleep(3)
            self.DCA.flex.write(':meas:mtes:marg?\n')
            maskMargin=self.DCA.flex.read()
            self.MaskMarginValue['text']=float(maskMargin.rstrip('\n') )
            self.DCA.flex.write('meas:eye:apow:unit dbm\n')
            self.DCA.flex.write('meas:eye:apow\n')
            self.DCA.flex.write('meas:eye:cros\n')
            self.DCA.flex.write('meas:eye:jitt:form pp\n')
            self.DCA.flex.write('meas:eye:jitt\n')
            self.DCA.flex.write('meas:eye:jitt:form rms\n')
            self.DCA.flex.write('meas:eye:jitt\n')
            self.DCA.flex.write('aut\n')
            DCA_OK=True
        except:
            DCA_OK=False
        self.InitOscope['bg']='light green' if DCA_OK else 'tomato'
        self.SetPRBSout['bg']='light green' if PRBS31_Status and self.MaskMarginValue['text']>30 else 'tomato'
        self.stelights.SetDeviceFun(self.stelights.pmSetWavLen,waveLength='1310nm')
        messagebox.showinfo('Connect','ONU/H510/H610 optical port to (OPM)Optical Power Meter')
        #self.ONU_OP_Value['text']=self.stelights.GetDeviceFun(self.stelights.pmGetPower)
        self.nOuter['ONU O/P']['text']=self.stelights.GetDeviceFun(self.stelights.pmGetPower)








        #self.bStartInit['bg'] = 'light green';print(self.ONU_OP_Value['text'])



        #self.ONU_OP_Value.configure(text=456.78)

    def StartTxAdjCalFun(self):
        pass
    def optionmenu_event(self,*args):
        pass
    def AssignSNevent(self):
        pass
    def ResetGPONevent(self):
        pass
    def Engineeringevent(self):
        pass
    def H610event(self):
        pass
    def Passwordevent(self):
        pass
def close_win():
    global win, app
    app.writePickle()
    app.destroy()
    win.destroy()
    sys.exit()
win = tk.Tk()
win.option_add('*Font','Helvetica 12')       #'','20'
win.title("永辰科技：H510/H610 Auto Test System @ DCA86100D Analyzer ☯△")
win.geometry("1000x900+300+30") #寬x高
win.resizable(False,False)
app = Application(win)
win.protocol("WM_DELETE_WINDOW",close_win)
win.mainloop()
# self.ONU_OP_Value=tk.Text(self.master,width=9,bd=2,bg='black',fg='yellow',height=1)  #,justify='center')
# self.ONU_OP_Value.insert('end',str(123))
# self.ONU_OP_Value.place(x=250,y=220)
# self.ONU_OP_Value.delete('1.0','end');self.ONU_OP_Value.insert('end',str(456.34))