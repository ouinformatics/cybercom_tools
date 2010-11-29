#!/usr/bin/python
'''
Created on Nov 16, 2010

@author: stac3294
Requires RUN_ID as argv Input Must be integer : Output Teco Model Input file
'''
import shlex, datetime, sys
import cx_Oracle as db
#connSTR = getpass.getpass()
connSTR= 'eco/b00mer@129.15.138.12:1521/oubcf'
conn = db.connect(connSTR)
c1 = conn.cursor()
c2 = conn.cursor()
MOD_ID = int(sys.argv[1])
OUT_FILE = sys.argv[2]
f=open(OUT_FILE,'w')
#MOD_ID =500
#f1 = open('stdOut', 'w')
f.write(' year doy hour tair Tsoil VDEF RH precp rad_h\n')
c1.callproc('TECO_INP_MOD_ID',(MOD_ID,c2))
for p in c2: 
     f.write(p[0].rjust(6,' ') + p[1].rjust(12,' ')+ p[2].rjust(12,' ')+ p[3].rjust(12,' ')+ p[4].rjust(12,' ')+ p[5].rjust(12,' ')+ p[6].rjust(12,' ')+ p[7].rjust(12,' ')+ p[8].rjust(12,' ')+'\n')
#    print p[0].rjust(6,' ') + p[1].rjust(12,' ')+ p[2].rjust(12,' ')+ p[3].rjust(12,' ')+ p[4].rjust(12,' ')+ p[5].rjust(12,' ')+ p[6].rjust(12,' ')+ p[7].rjust(12,' ')+ p[8].rjust(12,' ')
    
c2.close()   
c1.close() 
conn.close()
