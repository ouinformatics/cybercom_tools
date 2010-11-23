'''
Created on Nov 16, 2010
@author: stac3294
version = "0.0.1"
name = "DB Model Functions"
identifier = "edu.ou.it.Model.Input"
'''
import sys
import StringIO
import cx_Oracle as db

def getModelINP(RUN_ID,Model_ID,ConnSTR,FILE_NAME ):
#    connSTR= U'eco/b00mer@129.15.138.12:1521/oubcf'
#    connSTR1= U'eco/b00mer@129.15.138.13:1521/oubcf'
    try:
        conn = db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print type(ConnErr)
    try:
        f1 = open(FILE_NAME,'w')
        #f1 = StringIO.StringIO()
        c1 = conn.cursor()
        c2 = conn.cursor()
        prm = conn.cursor()
        prm.execute("Select PNAME,PVALUE From RT_PARAMETERS Where PARMA_TYPE=0 and MODEL_ID = 'TECO1'") #:1 ',(Model_ID,))
        wd =[]
        sql=''
        for par in prm:
            if par[0] == 'Header': head = par[1]
            if par[0] == 'FWidth': temp = par[1]
            if par[0] == 'SQL': sql = par[1]
        wd = temp.split(',')
        #RUN_ID = sys.argv[1]
        #RUN_ID =500
        f1.write(head + '\n') #' year doy hour tair Tsoil VDEF RH precp rad_h'
        c1.callproc(sql,(RUN_ID,c2)) #TECO_INP_MOD_ID',(RUN_ID,c2))
        for p in c2:
            z=0
            row =''
            for i in p:
                row = row + i.rjust(int(wd[z]),' ')
                z +=1
            f1.write(row + '\n') #i.rjust(int(wd[0]),' ') #+ p[1].rjust(wd[1],' ')+ p[2].rjust(12,' ')+ p[3].rjust(12,' ')+ p[4].rjust(12,' ')+ p[5].rjust(12,' ')+ p[6].rjust(12,' ')+ p[7].rjust(12,' ')+ p[8].rjust(12,' ')
    except Exception as inst:
        print 'Must provide Run ID as input to script.'
        print type(inst)     # the exception instance
        print inst            
    c2.close()   
    c1.close() 
    conn.close()
    return f1
