'''
Created on Jan 10, 2011
@author: Mark Stacy - markstacy@ou.edu

Current Module provides takes ftp inventory and inserts to DB
ftp Inventory is performed by ftpINV.py creates inventory of ftp site. 
Filename is location of the output file, Skip lines is the directory lines which do not have AMF site info.
'''
import shlex, sys, datetime #,StringIO, tempfile
import ast
import cx_Oracle as db
ConnSTR= 'eco/b00mer@oubcf1' 
COMMONS_ID= 300

def getDBConnection():
    try: # DB Connection
        return db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit() 

def loadAMF(filename,locName,ftpsite, skiplines=1):
    conn =  getDBConnection()   
    c1 = conn.cursor()
    locate = open('location.dat','r')#locName,'r')
    locID=[]
    locDir=[]
    temp=''
    dbNull = None
    for loc in locate:
        LLOC = loc.split(',')
        locID.append(LLOC[0].rstrip('\n'))
        locDir.append(LLOC[1].rstrip('\n'))
    '''
        root, Dirs, files = ast.literal_eval(loc)
        for file in files:
            #Error Checks found on Ftp Site
                        
            if file[0]=='Metolius_First_Young_Pine':
                locID.append('US-Me5')
                locDir.append('Metolius_First_Young_Pine')
            elif file[0]=='Rosemount_G19_Alternative_Management_Corn_Soybean_Rotation':
                locID.append('US-Ro3')
                locDir.append('Rosemount_G19_Alternative_Management_Corn_Soybean_Rotation')                 
            else:
                locID.append(file[0])
                temp= file[4].replace('../Sites_ByName/','')
                locDir.append(temp)#'Metolius_First_Young_Pine')
            #print locID[len(locID)-1] + ' ' + locDir[len(locID)-1] 
        locID.append('US-Ro3')
        locDir.append('Rosemount_G19_Alternative_Management_Corn_Soybean_Rotation') 
        locID.append('US-Ro1')
        locDir.append('Rosemount_G21_Conventional_Management_Corn_Soybean_Rotation') 
        #locID.append('UKN')
        #locDir.append('Lucky_Hills_Shrubland')
     
    locfile = open('location.dat','w')
    for x in range(len(locID)):
        locfile.write(locID[x] + ',' + locDir[x] +'\n')
    ''' 
                    
    input = open(filename,'r')
    listDict =[]
    ''' Header lines to skip '''
    Rowdb = 0 #Existing Files in DB
    RowInput = 0
    for i in range(skiplines):
        input.readline()
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
                if checkInDB('ftp://' + ftpsite + root + '/' + fname,c1):
                    Rowdb+=1
                else:
                    CAT =[]
                    CAT.append(COMMONS_ID)
                    catid=getSEQ_NEXTVAL('SEQ_CAT_ID',c1)
                    CAT.append(catid)
                    CAT.append(fname)#CATNAME
                    CAT.append(dbNull)#DATAPROVIDER
                    CAT.append(getType(fname))#Type
                    CAT.append(loc)
                    CAT.append(dbNull)
                    CAT.append('ftp://' + ftpsite + root + '/' + fname)
                    CAT.append('ftpINV')#Method
                    year,datestr = getYearDATE(fname)
                    CAT.append(datestr)
                    CAT.append(dbNull)
                    CAT.append(year)
                    CAT.append(dbNull)
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
def getType(fname):
    return 'UKN'
def checkInDB(catDESC,cur):
    flag=1
    cur.execute("Select count(*) from DT_CATALOG WHERE CAT_DESC = '" + catDESC + "' AND COMMONS_ID =" + str(COMMONS_ID))
    cur.fetchall()
    if cur.rowcount==0:
        flag=0
    return flag
               
def checkLocationTable(commonID, Locid, cur):
    cur.execute("Select * from DT_LOCATION WHERE LOC_ID = '" + Locid + "'")
    cur.fetchall()
    if cur.rowcount==0:
        cur.execute("INSERT INTO ECO.DT_LOCATION (COMMONS_ID, LOC_ID, LOC_NAME) VALUES (" + str(commonID) + ", '" +  Locid + "', '" + Locid +"')")
        print 'Inserted '  + Locid
def getYearDATE(fname):
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
    '''conn = getDBConnection()
    'c1 = conn.cursor()'''
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
def getDBConnection():
    try: # DB Connection
        return db.connect(ConnSTR)
    except Exception as ConnErr:
        print 'Unable to connect to Database '
        print ConnErr
        print type(ConnErr)
        sys.exit()      