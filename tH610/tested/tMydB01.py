import mysql.connector
MacAddr='PBG230412140958'
mydb=mysql.connector.connect(
    host="localhost",
    user="miles",
    password="Aa123456",
    database="ManageMac"
)
mycursor = mydb.cursor()
dBTab=["ManageMac","H610_2023"]
dBaseTable=dBTab[0]+'.'+dBTab[1]
mycursor.execute("insert into "+dBaseTable+" values (5,'"+MacAddr+"','','','','','','','','','','','','','','Ｏ','Ｘ','','','','','');")

#mycursor.execute("DELETE FROM "+dBaseTable+" WHERE MACADDR='"+MacAddr+"' limit 999;")
#mycursor.execute("DELETE FROM "+dBaseTable+" limit 999;")
#mycursor.execute("SELECT * FROM "+dBaseTable+" where macaddr='"+MacAddr+"';")
mydb.commit()



