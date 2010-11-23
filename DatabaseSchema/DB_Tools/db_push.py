'''
Created on Nov 22, 2010

@author: stac3294

RUN_ID Database index of Model Run from DB Table DT_MODEL_RUN
File_Type ('C_FILE','H2O_FILE','Pool_File')
objFile File object
'''
import shlex, sys, datetime
import cx_Oracle as db

def TECO2DB(RUN_ID,File_Type,objFile):
#    f1 = open('C:\App\Database\TECO_Data\TECO_C_daily.csv','r')#objFile
    if not(File_Type.upper() == 'C_FILE' or File_Type.upper() == 'H2O_FILE' or File_Type.upper() == 'POOL_FILE'): sys.exit('File_Type must be H2O_FILE, POOL_FILE, or C_FILE')
    f1 = objFile
    f1.seek(0,0)# Set current position at the beginning of the file.
    ConnSTR= 'eco/b00mer@129.15.138.12:1521/oubcf'
#    connSTR1= U'eco/b00mer@129.15.138.13:1521/oubcf'
    try: # DB Connection
        conn = db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit()  
    c1 = conn.cursor()
    c2 = conn.cursor() 
    temps = f1.readline()
    temps = temps.replace(' ','') 
    header = shlex.split(temps.replace(',',' '))     
    sqlyear = "SELECT DISTINCT MDRI_PARAMETER.PVALUE FROM MDRI_PARAMETER WHERE RUN_ID=500 AND PARAM_ORDER=0"#" + str(RUN_ID) + " AND PARAM_ORDER=0"
    
    c2.execute(sqlyear)
    row =c2.fetchone() 
    d = datetime.datetime(int(row[0]),1,1,0,0,0)
    P_ID = 0 
    for line in f1.readlines():
        temp= shlex.split(line.replace(',',''))
       
        idx = 0
        for col in temp:
            if idx==0:
                if File_Type.upper() == 'POOL_FILE':
                    delta = datetime.timedelta(days=(float(col)-1)*365)
                    TS = d + delta
                else:
                    delta = datetime.timedelta(days=(float(col)-1))
                    TS = d + delta
            sql = 'INSERT INTO ECO.MDR_OUTPUT ( RUN_ID, PARAM_ID, DATA_TYPE, VAR_NAME, VALUE, PARAM_ORDER, TIME_INDEX) VALUES ('
            sql= sql + str(RUN_ID) + ', ' + str(P_ID) + ", '" + File_Type + "', '" + header[idx] + "', '" + str(col)+ "', " + str(idx)+ ", TO_DATE('" + str(TS) + "','YYYY-MM-DD HH24:MI:SS'))" 
            c1.execute(sql)
            idx +=1
            P_ID +=1
    print str(P_ID) + " rows insert into Database."
    conn.commit()
    conn.close()

        