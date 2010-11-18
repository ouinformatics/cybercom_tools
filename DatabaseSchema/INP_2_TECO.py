'''
Created on Nov 16, 2010

@author: stac3294
Required Input: RUN_ID this is an Integer corresponding to Run parameters
Output: TECO formated parameters (Input TECO Model)
'''
import sys
import cx_Oracle as db
#connSTR = getpass.getpass()
connSTR= 'eco/b00mer@129.15.138.12:1521/oubcf'
connSTR1= 'eco/b00mer@129.15.138.13:1521/oubcf'
try:
    conn = db.connect(connSTR)
except ValueError:
    try:
        conn = db.connect(connSTR1)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print type(ConnErr)
    
try:
    c1 = conn.cursor()
    c2 = conn.cursor()
    #RUN_ID = sys.argv[1]
    RUN_ID =500
    print ' year doy hour tair Tsoil VDEF RH precp rad_h'
    c1.callproc('TECO_INP_MOD_ID',(RUN_ID,c2))
    for p in c2: 
        print p[0].rjust(6,' ') + p[1].rjust(12,' ')+ p[2].rjust(12,' ')+ p[3].rjust(12,' ')+ p[4].rjust(12,' ')+ p[5].rjust(12,' ')+ p[6].rjust(12,' ')+ p[7].rjust(12,' ')+ p[8].rjust(12,' ')
except Exception as inst:
    print 'Must provide Run ID as input to script.'
    print type(inst)     # the exception instance
    print inst            
c2.close()   
c1.close() 
conn.close()