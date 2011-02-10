'''
Created on Jan 10, 2011
@author: Mark Stacy - markstacy@ou.edu

syncAMF.py provides method to sync ftp inventory with the DT_CATALOG with Database.
Requires: 
        ftpINV --> create file of ftp files on site
        locations.dat file within the same directory of ftpINV produced inventory
        location.dat has LOC_ID,Folder - Created from Directory line skipped in syncAMF.


'''
import sys, datetime #,StringIO, tempfile
import ast, shlex
import urllib as url
import cx_Oracle as db
ConnSTR= 'eco/b00mer@oubcf1' 
COMMONS_ID= 300 #'COMMONS_ID For Ameriflux'
ECOMMONS_ID= 400 #'COMMONS_ID For EOMF'

'''***************************************EOMF web service Data Functions *****************************************''' 
def getEOMFdata(LAT,LON,modisProd,mYear,strVarables='*'):
    conn = getDBConnection()
    c1 = conn.cursor()
    myears = mYear.split(',')
    svar = stripVariables(strVarables)
    CAT_ID=[]
    for yr in myears:
        CAT_ID.append( syncEOMFdata(str(LAT) + '_' + str(LON),modisProd, yr))
    for c in CAT_ID:
        if strVarables=='*':
            sql = "SELECT TO_CHAR(E.EVENT_DATE,'YYYY-MM-DD') TIME_INDEX, R.VAR_ID, R.RESULT_TEXT, R.RESULT_NUMERIC FROM DT_EVENT E, DT_RESULT R WHERE E.CAT_ID=" + str(c) + " AND E.EVENT_ID = R.EVENT_ID ORDER BY E.EVENT_ID, R.RESULT_ORDER"
        else:
            sql = "SELECT TO_CHAR(E.EVENT_DATE,'YYYY-MM-DD') TIME_INDEX, R.VAR_ID, R.RESULT_TEXT, R.RESULT_NUMERIC FROM DT_EVENT E, DT_RESULT R WHERE E.CAT_ID=" + str(c) + " AND E.EVENT_ID = R.EVENT_ID AND R.VAR_ID in (" + svar.upper() + ") ORDER BY E.EVENT_ID, R.RESULT_ORDER"
        c1.execute(sql)
        for col in c1:
            print col
def syncEOMFdata(locid,Product,mYear):
    conn = getDBConnection()
    c1 = conn.cursor()
    #locid = str(LAT) + '_' + str(LON)
    CAT_ID=0
    checkLocationTable(ECOMMONS_ID,locid , c1)
    u_rl='http://www.eomf.ou.edu/visualization/ascii_' + Product.lower() + '_'  + str(mYear) + '_' + locid + '.txt'  
    if checkInDB(u_rl,ECOMMONS_ID,c1)==0:
        CAT_ID=getSEQ_NEXTVAL('SEQ_CAT_ID',c1)
        catSQL= "INSERT INTO ECO.DT_CATALOG ( COMMONS_ID, CAT_ID, CAT_NAME, DATA_PROVIDER, CAT_TYPE, LOC_ID, CAT_DESC, CAT_METHOD, OBSERVE_DATE, REMARK, YEAR, CUSTOM_FIELD_1, CUSTOM_FIELD_2, STATUS_FLAG, STATUS_DATA) VALUES ("
        catSQL= catSQL + "400," + str(CAT_ID) + ",'EOMF Web Service Call','EOMF','" + Product.upper() + "','" + locid + "','" + u_rl + "','EMOF_MEHOD',TO_DATE('" + str(mYear) + "-01-01','YYYY-MM-DD'), NULL," + str(mYear) + ", NULL, NULL,'A','N')"
        c1.execute(catSQL)
        conn.commit()
    c1.execute("Select CAT_ID, STATUS_DATA FROM DT_CATALOG WHERE CAT_DESC = '" + str(u_rl) + "'")
    row = c1.fetchone()
    CAT_ID = row[0]
    STATUS = row[1]
    if STATUS == 'N':
        PushEOMFdata(CAT_ID)
        setDATA_STATUS(CAT_ID,'Y')
    return CAT_ID
def PushEOMFdata(CAT_ID, skipLines=5):
    conn =  getDBConnection()   
    c1 = conn.cursor()
    c1.execute('Select CAT_DESC, YEAR, CAT_TYPE FROM DT_CATALOG WHERE CAT_ID = ' + str(CAT_ID))
    row = c1.fetchone()
    CAT_TYPE = row[2]
    #if not (CAT_TYPE=='TDF_M' or CAT_TYPE=='TDF_W' or CAT_TYPE=='TDF_D' or CAT_TYPE=='TDF_H'):
    #    print 'File must be a Text Data File format (TDF_H, TDF_D, TDF_W, TDF_M).\n' + 'CAT_ID: ' + str(CAT_ID) + ' has File Format ' + CAT_TYPE
    #    sys.exit() 
    mYear = row[1]
    rows = pullData(row[0]) 
    for x in range(skipLines):
        rows.readline()
    EVT_DESC = rows.readline().strip()
    rows.readline()
    header = shlex.split(rows.readline())
    checkRTVarables(header, 'EOMF')
    evtDict =[]
    rstDict =[]
    for rec in rows:
        record = []
        record = shlex.split(rec)
        if len(record)<=0:
            i=1
        else:
            EVT=[]
            EVT.append(ECOMMONS_ID)
            EVTid=getSEQ_NEXTVAL('SEQ_EVENT_ID',c1)
            EVT.append(EVTid)
            EVT.append(CAT_ID)
            EVT.append('Data File Time Index Event')
            EVT.append(CAT_TYPE + '_Method')
            EVT.append(record[0])
            EVT.append(EVT_DESC)
            EVT.append('EOMF_DATA_File')
            EVT.append(None)
            EVT.append(None)
            EVT.append(None)
            EVT.append('A')
            evtDict.append(convertSequenceToDict(EVT))
            idx=0
            for itm in record:
                #result 
                RST=[]
                RST.append(ECOMMONS_ID)
                RST.append(EVTid)
                var= (((header[idx].strip()).rstrip('\n')).rstrip('\r')).upper()
                RST.append(var)
                RST.append(itm.strip().rstrip('\n').rstrip('\r'))
                if idx==0 or idx==14:
                    RST.append(None)
                    RST.append(None)#Error Code
                    RST.append(itm)           
                else:
                    RST.append(float(itm.strip().rstrip('\n').rstrip('\r')))
                    RST.append(None)#Error Code
                    RST.append(None)
                RST.append(None)
                RST.append(idx)
                RST.append(None)
                RST.append(None)
                if idx==0 or idx==14:
                    RST.append('DATE')
                else:
                    RST.append('NUM')
                RST.append(None)
                RST.append(None)
                idx+=1
                rstDict.append(convertSequenceToDict(RST))
    evtSQL="INSERT INTO ECO.DT_EVENT ( COMMONS_ID, EVENT_ID, CAT_ID, EVENT_NAME, EVENT_METHOD, EVENT_DATE, EVENT_DESC, EVENT_TYPE, LOC_ID, CUSTOM_1, REMARK, STATUS_FLAG) VALUES ( :1,:2,:3,:4,:5,TO_DATE(:6,'YYYY-MM-DD'),:7,:8,:9,:10,:11,:12)"
    rstSQL="INSERT INTO ECO.DT_RESULT ( COMMONS_ID, EVENT_ID, VAR_ID, RESULT_TEXT, RESULT_NUMERIC, RESULT_ERROR, RESULT_DATE, STAT_RESULT, RESULT_ORDER, RESULT_UNIT, REMARK, VALUE_TYPE, STAT_TYPE, VALIDATED) VALUES (:1,:2,:3,:4,:5,:6,TO_DATE(:7,'YYYY-MM-DD'),:8,:9,:10,:11,:12,:13,:14)"        
    c1.executemany(evtSQL, evtDict)
    c1.executemany(rstSQL, rstDict)
    conn.commit()
    conn.close()  

'''*********************** Ameriflux ftp DATA ******************************************'''
def getAMF_SiteID(SiteID,year,Type,strVarables='*'):
    conn =  getDBConnection()   
    c1 = conn.cursor()
    c1.execute("Select CAT_ID FROM DT_CATALOG WHERE LOC_ID = '" + str(SiteID).upper() + "' AND YEAR in ( " + str(year) +  ") AND CAT_TYPE = '" + str(Type).upper() + "' ORDER BY YEAR" )
    '''
    row = c1.fetchone()  
    if c1.rowcount==0:
        print 'Error retrieving Data. Please double check SiteID, Year, And Type'
        sys.exit()
    '''    
    idx=1
    for c in c1:
        idx+=1
        #print stripVariables(strVarables).upper()
        getAMFdata(c[0],stripVariables(strVarables).upper())
    #print str(idx) + ' Years of Data. Retrieved  Data for the Following Years - (' + year + ')'
        
           
def getAMFdata(CAT_ID,strVarables='*'):
    try:
        conn =  getDBConnection()   
        c1 = conn.cursor()
        c1.execute('Select STATUS_DATA FROM DT_CATALOG WHERE CAT_ID = ' + str(CAT_ID))
        row = c1.fetchone()
        if row[0] == 'N':
            pushData(CAT_ID)
            setDATA_STATUS(CAT_ID,'Y')
        if strVarables=='*':
            sql = "SELECT TO_CHAR(E.EVENT_DATE,'YYYY-MM-DD HH24:MI:SS') TIME_INDEX, R.VAR_ID, R.RESULT_TEXT, R.RESULT_NUMERIC FROM DT_EVENT E, DT_RESULT R WHERE E.CAT_ID=" + str(CAT_ID) + " AND E.EVENT_ID = R.EVENT_ID ORDER BY E.EVENT_ID, R.RESULT_ORDER"
        else:
            sql = "SELECT TO_CHAR(E.EVENT_DATE,'YYYY-MM-DD HH24:MI:SS') TIME_INDEX, R.VAR_ID, R.RESULT_TEXT, R.RESULT_NUMERIC FROM DT_EVENT E, DT_RESULT R WHERE E.CAT_ID=" + str(CAT_ID) + " AND E.EVENT_ID = R.EVENT_ID AND R.VAR_ID in (" + strVarables.upper() + ") ORDER BY E.EVENT_ID, R.RESULT_ORDER"
        c1.execute(sql)
        for c in c1:
            print c
               
    except Exception as ConnErr:
        print ConnErr
        print type(ConnErr)
        sys.exit()        
def pushData(CAT_ID):
    conn =  getDBConnection()   
    c1 = conn.cursor()
    c1.execute('Select CAT_DESC, YEAR, CAT_TYPE FROM DT_CATALOG WHERE CAT_ID = ' + str(CAT_ID))
    row = c1.fetchone()
    CAT_TYPE = row[2]
    if not (CAT_TYPE=='TDF_M' or CAT_TYPE=='TDF_W' or CAT_TYPE=='TDF_D' or CAT_TYPE=='TDF_H'):
        print 'File must be a Text Data File format (TDF_H, TDF_D, TDF_W, TDF_M).\n' + 'CAT_ID: ' + str(CAT_ID) + ' has File Format ' + CAT_TYPE
        sys.exit() 
    mYear = row[1]
    rows = pullData(row[0])
    header = (rows.readline()).split(',')
    checkRTVarables(header,'Ameriflux')
    doy=0.0
    evtDict =[]
    rstDict =[]
    for rec in rows:
        record = []
        record = rec.split(',')
        EVT=[]
        EVT.append(COMMONS_ID)
        EVTid=getSEQ_NEXTVAL('SEQ_EVENT_ID',c1)
        EVT.append(EVTid)
        EVT.append(CAT_ID)
        EVT.append('Data File Time Index Event')
        EVT.append(CAT_TYPE + '_Method')
        if CAT_TYPE == 'TDF_M':
            EVT.append(setTimeIndex(CAT_TYPE, mYear, record[0]))
        elif CAT_TYPE == 'TDF_W':
            doy = doy + float(record[1])
            EVT.append(setTimeIndex(CAT_TYPE, mYear,1,doy))
        elif CAT_TYPE == 'TDF_H':
            EVT.append(setTimeIndex(CAT_TYPE, mYear,1,record[3],record[2])) 
        elif CAT_TYPE == 'TDF_D':
            EVT.append(setTimeIndex(CAT_TYPE, mYear,1,record[2])) 
        EVT.append(CAT_TYPE + ' Data File')
        EVT.append('AMF_DATA_File')
        EVT.append(None)
        EVT.append(None)
        EVT.append(None)
        EVT.append('A')
        evtDict.append(convertSequenceToDict(EVT))
        idx=0
        for itm in record:
            #result 
            RST=[]
            RST.append(COMMONS_ID)
            RST.append(EVTid)
            var= (((header[idx].strip()).rstrip('\n')).rstrip('\r')).upper()
            RST.append(var)
            RST.append(itm.strip().rstrip('\n').rstrip('\r'))
            RST.append(float(itm.strip().rstrip('\n').rstrip('\r')))
            RST.append(None)#Error Code
            RST.append(None)
            RST.append(None)
            RST.append(idx)
            RST.append(None)
            RST.append(None)
            RST.append(None)
            RST.append(None)
            RST.append(None)
            idx+=1
            rstDict.append(convertSequenceToDict(RST))
    evtSQL="INSERT INTO ECO.DT_EVENT ( COMMONS_ID, EVENT_ID, CAT_ID, EVENT_NAME, EVENT_METHOD, EVENT_DATE, EVENT_DESC, EVENT_TYPE, LOC_ID, CUSTOM_1, REMARK, STATUS_FLAG) VALUES ( :1,:2,:3,:4,:5,TO_DATE(:6,'YYYY-MM-DD HH24:MI:SS'),:7,:8,:9,:10,:11,:12)"
    rstSQL="INSERT INTO ECO.DT_RESULT ( COMMONS_ID, EVENT_ID, VAR_ID, RESULT_TEXT, RESULT_NUMERIC, RESULT_ERROR, RESULT_DATE, STAT_RESULT, RESULT_ORDER, RESULT_UNIT, REMARK, VALUE_TYPE, STAT_TYPE, VALIDATED) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)"        
    c1.executemany(evtSQL, evtDict)
    c1.executemany(rstSQL, rstDict)
    conn.commit()
    conn.close()

def syncAMF(filename,locFileName,ftpsite, skiplines=1):
    '''
    Filename is location of the ftpINV output file, Skip lines is the directory line which is used for Level Data.
    Ameriflux ftp dependent
    '''
    conn =  getDBConnection()   
    c1 = conn.cursor()
    locate = open(locFileName,'r')
    locID=[]
    locDir=[]
    temp=''
    dbNull = None
    for loc in locate:
        LLOC = loc.split(',')
        locID.append(LLOC[0].rstrip('\n'))
        locDir.append(LLOC[1].rstrip('\n'))
    input = open(filename,'r')
    listDict =[]
    ''' Header lines to skip '''
    Rowdb = 0 #Existing Files in DB
    RowInput = 0
    for i in range(skiplines):
        root, Dirs, files = ast.literal_eval(input.readline())
        try:
            dataLevel = (root.split('/'))[4]
        except Exception as inst:
            dataLevel='UKN'
    for line in input:
        root, Dirs, files = ast.literal_eval(line)
        temp = root.split('/')
        dir = temp[len(temp)-1]
        try:
            loc = (locID[locDir.index(dir)]).upper()
        except Exception as inst:
            loc='UKN'
        print 'Checking AmeriFlux Location: ' + loc
        checkLocationTable(COMMONS_ID, loc, c1)
        for f in files:
            fname=f[0]
            if fname=='ReadMe_First_AmeriFlux_Fair_Use_Policy.txt': i=i+1
            elif fname=='history_changes.txt': i=i+1
            elif fname=='README': i=i+1
            else:
                if checkInDB('ftp://' + ftpsite + root + '/' + fname,COMMONS_ID,c1)==1:
                    Rowdb+=1
                else:
                    CAT =[]
                    CAT.append(COMMONS_ID)
                    catid=getSEQ_NEXTVAL('SEQ_CAT_ID',c1)
                    CAT.append(catid)
                    CAT.append(fname)#CATNAME
                    CAT.append(dataLevel)#DATAPROVIDER
                    CAT.append(getType(fname))#Type
                    CAT.append(loc)
                    CAT.append(dbNull)
                    CAT.append('ftp://' + ftpsite + root + '/' + fname)
                    CAT.append('ftpINV')#Method
                    year,datestr = getYearDATE(fname)
                    CAT.append(datestr)
                    CAT.append(dbNull)
                    CAT.append(year)
                    CAT.append(filename)
                    CAT.append(dbNull)
                    CAT.append('A')#Status Flag
                    CAT.append('N')#In DB
                    listDict.append(convertSequenceToDict(CAT))
                    RowInput=+1
    catSQL= "INSERT INTO ECO.DT_CATALOG ( COMMONS_ID, CAT_ID, CAT_NAME, DATA_PROVIDER, CAT_TYPE, LOC_ID, SOURCE_ID, CAT_DESC, CAT_METHOD, OBSERVE_DATE, REMARK, YEAR, CUSTOM_FIELD_2, CUSTOM_FIELD_3, STATUS_FLAG, STATUS_DATA) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,TO_DATE(:10,'YYYY-MM-DD HH24:MI:SS'),:11,:12,:13,:14,:15,:16)"
    c1.executemany(catSQL, listDict)
    print str(Rowdb) + ' files already Cataloged.'
    print str(RowInput) + ' files inputed into Catalog.'
    conn.commit()
    
''' ******************************* Shared Function Calls ******************************************'''

def pullData(CAT_DESC):
    return url.urlopen(CAT_DESC)
def stripVariables(var):
    temp=var.replace("'","")
    temp=temp.replace('"','')
    list=temp.split(',')
    idx =0
    vars=''
    for itm in list:
        if idx == len(list)-1:
            vars= vars + "'" + itm + "'"
        else:
            vars= vars + "'" + itm + "',"
        idx+=1
    if var=='*':
        return var
    else:
        print vars
        return vars
        
def setDATA_STATUS(CAT_ID,Status):
    conn =  getDBConnection()   
    c1 = conn.cursor()
    c1.execute("UPDATE DT_CATALOG SET STATUS_DATA = '" + Status + "'  WHERE CAT_ID = " + str(CAT_ID))
    conn.commit()
    conn.close()

def setTimeIndex(CAT_TYPE, mYEAR,Month=1,DoY=1.0,Hour='0.0'):
    '''
    mYear year of data; Month of Year; 
    DoY is Day of year - have to keep track for Weekly ; CAT_TYPE
    '''
    if CAT_TYPE == 'TDF_M':
        d = datetime.datetime(int(mYEAR),int(Month),1,0,0,0)
        TS = d
    elif CAT_TYPE == 'TDF_H':
        tmp = Hour.split('.')
        min= int(float('0.' + tmp[1])* 60)
        d = datetime.datetime(int(mYEAR),1,1,int(tmp[0]),min,0)
        tmp1 = str(DoY).split('.')
        trundoy=int(tmp1[0])
        delta = datetime.timedelta(days=(float(trundoy)-1))
        TS = d + delta
    elif CAT_TYPE == 'TDF_D' or CAT_TYPE == 'TDF_W':
        d = datetime.datetime(int(mYEAR),1,1,0,0,0)
        delta = datetime.timedelta(days=(float(DoY)-1))
        TS = d + delta
    return str(TS)
   
def checkRTVarables(LISTvarid, Source):
    conn =  getDBConnection()   
    c1 = conn.cursor()
    idx=0
    for varid in LISTvarid:
        var=(((varid.strip()).rstrip('\n')).rstrip('\r')).upper()
        c1.execute("Select VAR_ID FROM RT_VARABLES WHERE VAR_ID = '" + var + "'")
        c1.fetchall()
        if c1.rowcount<=0:
            c1.execute("INSERT INTO ECO.RT_VARABLES ( VAR_ID, VARABLE_NAME, SORT_ORDER, STATUS_FLAG, VAR_SHORT_NAME,REMARK) VALUES ('" + var + "','" + varid + "'," + str(idx) + ",'A','" + varid + "','" + Source + "')" )
        idx+=1
    conn.commit()
    conn.close()

def getDBConnection():
    try: # DB Connection
        return db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit()

def dumpData(CAT_ID):
    try:
        conn =  getDBConnection()   
        c1 = conn.cursor()
        c1.execute("Delete from DT_EVENT where CAT_ID = " + str(CAT_ID))
        setDATA_STATUS(CAT_ID,'N')
        conn.commit()
        conn.close()
    except Exception as ConnErr:
        print ConnErr
        print type(ConnErr)
        sys.exit() 
def getType(fname):
    type='UKN'
    fnam=fname.lower()
    if fnam.find('.txt')>-1:
        if fnam.find('_w_'):
            type= 'TDF_W'
        elif fnam.find('_w.'):
            type='TDF_W'
        elif fnam.find('_m.'):
            type='TDF_M'
        elif fnam.find('_m_'):
            type='TDF_M'
        elif fnam.find('_d.'):
            type='TDF_D'
        elif fnam.find('_d_'):
            type='TDF_D'
        elif fnam.find('_h.'):
            type='TDF_H'
        elif fnam.find('_h_'):
            type='TDF_H'
    elif fnam.find('.pdf')>-1:
        type='PDF'
    elif fnam.find('.png')>-1:
        type='PNG'
    elif fnam.find('.mat')>-1:
        type='MAT'
    else:
        type='UKN'      
    return type
def checkInDB(catDESC,CommID,cur):
    flag=1
    cur.execute("Select CAT_ID from DT_CATALOG WHERE CAT_DESC = '" + catDESC + "' AND COMMONS_ID =" + str(CommID))
    cur.fetchall()
    if cur.rowcount<=0:
        flag=0
    return flag
               
def checkLocationTable(commonID, Locid, cur):
    cur.execute("Select * from DT_LOCATION WHERE LOC_ID = '" + Locid + "'")
    cur.fetchall()
    if cur.rowcount==0:
        cur.execute("INSERT INTO ECO.DT_LOCATION (COMMONS_ID, LOC_ID, LOC_NAME) VALUES (" + str(commonID) + ", '" +  Locid + "', '" + Locid +"')")
        #print 'Inserted '  + Locid
def getYearDATE(fname):
    '''
    Ameriflux site dependent
    Returns Integer year and date string of year with default 'YYYY-MM-DD HH24:MI:SS'
    '''
    try:
        yr=''
        datestr=''
        if (fname.split('_'))[0]=='AMF':
            yr=(fname.split('_'))[2]
            if not yr.isdigit():
                yr=fname[9:13]
        else:
            yr=fname[5:9]
            
        if yr.isdigit():
            if len(yr)==4:
                datestr= yr + '-01-01 00:00:00' 
            else:
                temp= raw_input('Filename is ' + fname + ' What is the Year?')
                yr=temp
                datestr= temp + '-01-01 00:00:00'
        else:
            temp= raw_input('Filename is ' + fname + ' What is the Year?')
            yr=temp
            datestr= temp + '-01-01 00:00:00'
    except Exception as inst:
        temp= raw_input('Filename is ' + fname + ' What is the Year?')
        yr=temp
        datestr= temp + '-01-01 00:00:00'        
    return int(yr),datestr 
          
def getSEQ_NEXTVAL(Sequence,cursor):
    '''
    Oracle Dependent Call Returns Next Value of sequence
    '''
    sql = 'SELECT ' + Sequence + '.NEXTVAL FROM DUAL'
    cursor.execute(sql)
    row =cursor.fetchone()
    return row[0]

def convertSequenceToDict(list):
    """For each element in the sequence, creates a dictionary item equal
    to the element and keyed by the position of the item in the list.
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
   