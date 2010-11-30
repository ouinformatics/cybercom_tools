'''
Created on Nov 22, 2010

@author: stac3294


'''
import shlex, sys, datetime,StringIO, tempfile
import cx_Oracle as db
ConnSTR= 'eco/b00mer@oubcf1' 

def INP_2_DB(RUNID, Filename):
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
    temp = []
    listDict =[]
    
    RUN_ID = int(RUNID) #getRUN_ID()
    i=0
    for j in input:
       DRow = shlex.split(j)
       d = datetime.datetime(int(DRow[0]),1,1,0,0,0)
       delta = datetime.timedelta(days=(float(DRow[1])-1)+(float(DRow[2])/24))
       TS = d + delta
       for k in range(len(header)):
           #runSQL= 'INSERT INTO ECO.MDRI_PARAMETER ( RUN_ID, PARAM_ID, VAR_NAME, PVALUE, PARAM_ORDER, TIME_INDEX, DATA_TYPE) VALUES ('
           #runSQL = runSQL + str(RUN_ID) + ", " + str(i) + ", '" + header[k] + "', '" + DRow[k] + "'," + str(k)+ ", TO_DATE('" + str(TS) + "','YYYY-MM-DD HH24:MI:SS'),'DATA_INPUT')"
           #print runSQL
           #c1.execute(runSQL)
           sdate= "TO_DATE('" + str(TS) + "','YYYY-MM-DD HH24:MI:SS')"
           list=[]
           list.append(RUN_ID)
           list.append(i)
           list.append(header[k].strip())
           list.append(DRow[k].strip())
           list.append(k)
           list.append(str(TS))
           list.append('DATA_INPUT')
           #print list
           
           #list =  str(RUN_ID) + ";" + str(i).strip() + ";" + header[k].strip() + ";" + DRow[k].strip() + ";" + str(k).strip() + ";" + sdate +  ";DATA_INPUT"
           
           #print list
           #temp= list.split(';')
           #print temp
           
           listDict.append(convertSequenceToDict(list))
           #print listDict
           #sys.exit()
           i +=1
    runSQL= "INSERT INTO ECO.MDRI_PARAMETER ( RUN_ID, PARAM_ID, VAR_NAME, PVALUE, PARAM_ORDER, TIME_INDEX, DATA_TYPE) VALUES (:1,:2,:3,:4,:5,TO_DATE(:6,'YYYY-MM-DD HH24:MI:SS'),:7)"
    c1.executemany(runSQL, listDict)
    c1.close() 
    conn.commit() # 
    print str(i) + ' records inserted'
def convertSequenceToDict(list):
    """For each element in the sequence, creates a dictionary item equal
    to the element and keyed by the position of the item in the list.
    Thanks to Dick Wall.
    Example:
    >>> convertListToDict(("Matt", 1))
    {'1': 'Matt', '2': 1}
    """
    dict = {}
    argList = range(1,len(list)+1)
    #print argList
    for k,v in zip(argList, list):
        dict[str(k)] = v
    return dict
def getRUN_ID(RUN_NAME, RUN_DESC, MODEL_ID):
    '''
    Returns the next Sequence value for RUN_ID. Insert Record of RUN_NAME and DESC in DT_MODEL_RUN
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
    TimeS = str(datetime.datetime.now())
    TS = TimeS.split('.')
    sql='INSERT INTO ECO.DT_MODEL_RUN ( RUN_ID, RUN_NAME, DESCRIPTION, START_TIMESTAMP, END_TIMESTAMP, TIME_ID, LOC_ID, MODEL_ID) VALUES ('
    sql = sql + str(row[0]) + ", '" + RUN_NAME + "', '" + RUN_DESC + "', " + " TO_DATE('" + str(TS[0]) + "','YYYY-MM-DD HH24:MI:SS'),Null , NULL, NULL,'" + MODEL_ID + "')"
    c1.execute(sql)
    conn.commit()
    conn.close()
    return int(row[0])
'''
def getRUN_ID():
    
    #Returns the next Sequence value for RUN_ID
    
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
'''
def TECO2DB(RUN_ID,File_Type,objFile):
    '''
    TECO Output files are passed and inputed into the Database.
    
    RUN_ID Database index of Model Run from DB Table DT_MODEL_RUN
    File_Type ('C_FILE','H2O_FILE','Pool_File')
    ObjFile File object
    '''
#    f1 = open('C:\App\Database\TECO_Data\TECO_C_daily.csv','r')#objFile
    if not(File_Type.upper() == 'C_FILE' or File_Type.upper() == 'H2O_FILE' or File_Type.upper() == 'POOL_FILE'): sys.exit('File_Type must be H2O_FILE, POOL_FILE, or C_FILE')
    f1 = objFile
    f1.seek(0,0)# Set current position at the beginning of the file.
    
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
    sqlyear = "SELECT DISTINCT MDRI_PARAMETER.PVALUE FROM MDRI_PARAMETER WHERE RUN_ID=500 AND PARAM_ORDER=0 AND DATA_TYPE ='DATA_INPUT'"#" + str(RUN_ID) + " AND PARAM_ORDER=0"
    
    c2.execute(sqlyear)
    row =c2.fetchone() 
    d = datetime.datetime(int(row[0]),1,1,0,0,0)
    P_ID = 0 
    listDict =[]
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
            #sql = 'INSERT INTO ECO.MDR_OUTPUT ( RUN_ID, PARAM_ID, DATA_TYPE, VAR_NAME, VALUE, PARAM_ORDER, TIME_INDEX) VALUES ('
            #sql= sql + str(RUN_ID) + ', ' + str(P_ID) + ", '" + File_Type + "', '" + header[idx] + "', '" + str(col)+ "', " + str(idx)+ ", TO_DATE('" + str(TS) + "','YYYY-MM-DD HH24:MI:SS'))" 
            #c1.execute(sql)
            row=[]
            row.append(int(RUN_ID))
            row.append(P_ID)
            row.append(File_Type)
            row.append(header[idx])
            row.append(str(col))
            row.append(idx)
            row.append(str(TS))
            listDict.append(convertSequenceToDict(row))
            idx +=1
            P_ID +=1
    sql = "INSERT INTO ECO.MDR_OUTPUT ( RUN_ID, PARAM_ID, DATA_TYPE, VAR_NAME, VALUE, PARAM_ORDER, TIME_INDEX) VALUES (:1,:2,:3,:4,:5,:6,TO_DATE(:7,'YYYY-MM-DD HH24:MI:SS'))"
    c1.executemany(sql, listDict)
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

def setRunParameter(RUN_ID,Header,pvalue): #List of header and list of values 
    '''
    example
    Header ='Lat,Co2ca,output,a1,Ds0,Vcmx0,extku,xfang,alpha,stom_n,Wsmax,Wsmin,rdepth,rfibre,SLA,LAIMAX,LAIMIN,Rootmax,Stemmax,SenS,SenR'
    pvalue = '35.9,3.70E-04,2,7.0,2000,0.80E-04,0.5,0,0.385,2,35,6,70.0,0.7,1.2E-2,4.5,0.1,1000.0,1000.0,0.0005,0.0005'
    H = shlex.split(Header.replace(',',' '))
    P = shlex.split(pvalue.replace(',',' '))
    db1.setRunParameter(500, H, P)
    '''
    try:
        conn = db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit() 
    try:
        c1 = conn.cursor()  
      
        for param in range(len(Header)):
            sql = 'INSERT INTO ECO.MDRI_PARAMETER ( RUN_ID, PARAM_ID, DATA_TYPE, VAR_NAME, PVALUE, PARAM_ORDER, TIME_INDEX) VALUES ( '
            sql = sql + str(RUN_ID) + ', ' + str(param) + ", 'RUN_PARAM', '" + Header[param] + "', '" + pvalue[param] + "', " + str(param) + ", NULL)"
            c1.execute(sql)
    except Exception as modErr:
        print 'Error inserting parameters into Database '
        print modErr
        print type(modErr)
        conn.close()
        sys.exit()
    conn.commit()    
    conn.close() 
def getRunParameter(RUN_ID): #Return Dictionary with List of Header and Values 
    '''
    Example
    f= db1.getRunParameter(500)
    for item in f:
    print 'Parameter Name: ' + item[0] + ' Value equals  '+ item[1]
    '''
    try:
        conn = db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit()      
    try:
        c1 = conn.cursor()  
        sql = "SELECT VAR_NAME,PVALUE FROM MDRI_PARAMETER WHERE RUN_ID=" + str(RUN_ID) + " AND DATA_TYPE='RUN_PARAM'"
        d={}
        c1.execute(sql)
        #for key in c1:
        #    d=key[0] = key[1]
        return c1
    except Exception as modErr:
        print 'Error returning parameters into Database '
        print modErr
        print type(modErr)
        conn.close()
        sys.exit()       
