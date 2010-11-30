#!/usr/bin/python
'''
Created on Nov 22, 2010

@author: stac3294
'''
import db_push as db1
import cx_Oracle as db
import sys
CFILE = sys.argv[1]
H2OFILE = sys.argv[2]
POOLFILE = sys.argv[3]
ConnSTR= 'eco/b00mer@oubcf'
#ConnSTR= 'eco/b00mer@129.15.138.12:1521/oubcf'
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
f1 = open(CFILE,'r')#objFile
db1.TECO2DB(newSEQ,'C_FILE',f1)
f2 = open(H2OFILE,'r')#objFile
db1.TECO2DB(newSEQ,'H2O_FILE',f2)
f3 = open(POOLFILE,'r')#objFile
db1.TECO2DB(newSEQ,'POOL_FILE',f3)

f1.close()
f2.close()
f3.close()
conn.close()
