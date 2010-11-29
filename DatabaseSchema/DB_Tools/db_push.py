'''
Created on Nov 22, 2010

@author: stac3294


'''
import shlex, sys, datetime,StringIO, tempfile
import cx_Oracle as db
ConnSTR= 'eco/b00mer@oubcf'

def INP_2_DB(Filename):
    '''
    TECO input file is loaded into database.
    '''
    try: # DB Connection
        conn = db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit() 
        
    c1 = conn.cursor()
    input = open(Filename)
    header = shlex.split(input.readline())
    DRow =[]
    RUN_ID = getRUN_ID()
    i=0
    for j in input:
       DRow = shlex.split(j)
       d = datetime.datetime(int(DRow[0]),1,1,0,0,0)
       delta = datetime.timedelta(days=(float(DRow[1])-1)+(float(DRow[2])/24))
       TS = d + delta
       for k in range(len(header)):
           runSQL= 'INSERT INTO ECO.MDRI_PARAMETER ( RUN_ID, PARAM_ID, VAR_NAME, PVALUE, PARAM_ORDER, TIME_INDEX, DATA_TYPE) VALUES ('
           runSQL = runSQL + str(RUN_ID) + ", " + str(i) + ", '" + header[k] + "', '" + DRow[k] + "'," + str(k)+ ", TO_DATE('" + str(TS) + "','YYYY-MM-DD HH24:MI:SS'),'DATA_INPUT')"
           #print runSQL
           c1.execute(runSQL)
           i +=1
   
    c1.close() 
    conn.commit() # 
    print str(i) + ' records inserted'

def getRUN_ID():
    '''
    Returns the next Sequence value for RUN_ID
    '''
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
    return int(row[0])
def TECO2DB(RUN_ID,File_Type,objFile):
    '''
    TECO Output files are passed and inputed into the Database.
    
    RUN_ID Database index of Model Run from DB Table DT_MODEL_RUN
    File_Type ('C_FILE','H2O_FILE','Pool_File')
    ObjFile File object
    '''
    if not(File_Type.upper() == 'C_FILE' or File_Type.upper() == 'H2O_FILE' or File_Type.upper() == 'POOL_FILE'): sys.exit('File_Type must be H2O_FILE, POOL_FILE, or C_FILE')
    f1 = objFile
    f1.seek(0,0)# Set current position at the beginning of the file.
    
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
    sqlyear = "SELECT DISTINCT MDRI_PARAMETER.PVALUE FROM MDRI_PARAMETER WHERE RUN_ID=500 AND PARAM_ORDER=0 AND DATA_TYPE ='DATA_INPUT'"#" + str(RUN_ID) + " AND PARAM_ORDER=0"
    
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
def getModelINP(RUN_ID,Model_ID,OUTFILE):
    '''
    Retrieves Input parameters from DB and returns file object.
    RUN_ID and Model_ID needed to retrieve data from DB
    '''
    try:
        conn = db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit()  
    try:
        #f1 = tempfile.NamedTemporaryFile(delete=False)#open('OUTFILE','r+')
        #f1 = StringIO.StringIO()
        f1 = open(OUTFILE,'w')
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
        f1.write(head + '\n') #' year doy hour tair Tsoil VDEF RH precp rad_h'
        c1.callproc(sql,(RUN_ID,c2)) #TECO_INP_MOD_ID',(RUN_ID,c2))
        for p in c2:
            z=0
            row =''
            for i in p:
                row = row + i.rjust(int(wd[z]),' ')
                z +=1
            f1.write(row + '\n' ) 
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst
        #sys.exit()
    c2.close()   
    c1.close() 
    conn.close()
    return f1

        
