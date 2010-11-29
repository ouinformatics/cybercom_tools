'''
Created on Nov 22, 2010

@author: stac3294
'''

import db_push as db1
import cx_Oracle as db
import shlex
# getRUN_ID ( Description )
rID = db1.getRUN_ID('TECO Model ', 'TECO RUN','TECO1')
print str(rID)
#*************** Examples push TECo Output files to DB **********************************
'''
# Fetch next sequence value
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
''' 

#db1.INP_2_DB('C:\App\TECO_amb_h.txt')
'''************** Examples Get Model Input File *********************************************
f2=db1.getModelINP(500,'TECO1')
f2.seek(0,0)
for line in f2.readlines():
    print line
    
#print f2.readlines()
'''
'''************* Examples for set and get Parameters ****************************************
# Set
Header ='Lat,Co2ca,output,a1,Ds0,Vcmx0,extku,xfang,alpha,stom_n,Wsmax,Wsmin,rdepth,rfibre,SLA,LAIMAX,LAIMIN,Rootmax,Stemmax,SenS,SenR'
pvalue = '35.9,3.70E-04,2,7.0,2000,0.80E-04,0.5,0,0.385,2,35,6,70.0,0.7,1.2E-2,4.5,0.1,1000.0,1000.0,0.0005,0.0005'
H = shlex.split(Header.replace(',',' '))
P = shlex.split(pvalue.replace(',',' '))
db1.setRunParameter(500, Header, pvalue)

#get
f= db1.getRunParameter(500)
for item in f:
    print 'Parameter Name: ' + item[0] + ' Value equals  '+ item[1]
'''    
