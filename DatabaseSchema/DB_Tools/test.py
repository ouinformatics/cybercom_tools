'''
Created on Nov 22, 2010

@author: stac3294
'''
import db_push as db1
import cx_Oracle as db

ConnSTR= 'eco/b00mer@129.15.138.12:1521/oubcf'
try: # DB Connection
    conn = db.connect(ConnSTR)
except Exception as ConnErr:
    print 'Unable to connect to Database '
    print ConnErr
    print type(ConnErr)
    sys.exit() 
c1 = conn.cursor()
c1.execute('SELECT SEQ_RUN_ID.NEXTVAL FROM DUAL')
row =c1.fetchone()
newSEQ = int(row[0]) 
f1 = open('C:\App\Database\TECO_Data\TECO_C_daily.csv','r')#objFile
db1.TECO2DB(newSEQ,'C_FILE',f1)
f2 = open('C:\App\Database\TECO_Data\TECO_H2O_daily.csv','r')#objFile
db1.TECO2DB(newSEQ,'H2O_FILE',f2)
f3 = open('C:\App\Database\TECO_Data\TECO_pools_C.csv','r')#objFile
db1.TECO2DB(newSEQ,'POOL_FILE',f3)

f1.close()
f2.close()
f3.close()
conn.close()
