import sys
from tkinter import messagebox
import mysql.connector
n=len(sys.argv)
dBaseItem=('macused','countrycode','bomsasn','gponsn','wifissid','wifipwd','customersn','fwver',
           'caltest','ledtest','usbtest','wpsbtntest','resetbtntest','gpontest','telporttest','lanporttest',
           'ldeasmtest','wifitest','verifycodetest','closebackdoortest')    #'MacAddr',
dBaseData=['']*len(dBaseItem)
if n==4:
    TableName="H610_2023"
elif n==5:
    TableName=sys.argv[4]
else:
    messagebox.showerror("Python test H610 Error：", "argument No. must==4 or 5")
    quit()#7c8334501ea0/00e04c867001
print(sys.argv)
MacAddr=sys.argv[1]
if len(MacAddr)!=12:     #Check len(MacAddr)==12
    messagebox.showerror("Python test H610 Error：", "Mac address length must==12。")
    quit()
try:                     #Check MacAddr is a hexdecimal。
    a=int('0x'+MacAddr,0)  
except:
    messagebox.showerror("Python test H610 Error：", "Mac address not hexdecimal。")
    quit()
sysargv2lower=sys.argv[2].lower()
if not sysargv2lower in dBaseItem:
    messagebox.showerror("Python test H610 Error：", "Argument 2 must be an one of dBase item。")
    quit()
n=dBaseItem.index(sysargv2lower)
dBaseData[n]=sys.argv[3]
dBaseTable="ManageMac."+TableName                  #H610_2023"
tmp="insert into "+dBaseTable+" values (5,'"+MacAddr+"',"
for x in dBaseData:
    tmp+="'";tmp+=x;tmp+="',"
tmp+='.,'
ttt=tmp.replace(',.,',')')
try:
    mydb=mysql.connector.connect(host="localhost",
    user="miles",password="Aa123456",database="ManageMac")
except:
    messagebox.showerror("Python test H610 Error：", "No database in your system。")
    quit()
mycursor = mydb.cursor()
mycursor.execute(ttt)
print(ttt)
mydb.commit()
