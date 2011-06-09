#from cybercom.data.catalog import datalayer
import dataloader
from datetime import datetime, timedelta 
import sys.argv as argv
#*******Configuration variables******************
MongoDB = 'mesonet'
MongoCollection = 'weather'
userid ='mstacy'
Server='fire.rccc.ou.edu'
file_find_results = argv[1]
commonsID = 600

#******Class declarations***********************
md=dataloader.Metadata_load()
ml=dataloader.Mongo_load(MongoDB)

#*****Functions ********************************

def loadMD_Mongo(filepath):
    session=md.getSession()
    try:
        pks=catalog(filepath)
        event_LocalFile(filepath,pks)
        event_RemoteWS(filepath,pks)
        event_LocalWS(filepath,pks)
        event_Mongo(filepath,pks)
        success=insertmongo(filepath,pks)
        session.commit()
    except:
        session.rollback()
        raise
def catalog(filepath):
    '''Catalog mesonet datafiles - Mesonet specific function'''
    param={'commons_id':commonsID,'cat_type':'MESO_DAILY','cat_method':'Meso_Sync'}
    temp=filepath.split('/')
    fname=temp[len(temp)-1].rstrip('\n').rstrip('\r')
    loc_id = fname[8:12]
    sdate = fname[0:8]
    dt=datetime(int(sdate[0:4]),int(sdate[4:6]),int(sdate[6:8]),0,0,0)
    url = 'http://www.mesonet.org/index.php/dataMdfMts/dataController/getFile/' + fname[0:12] + '/mts/TEXT/' 
    param['cat_name']=fname
    param['cat_desc']=url
    param['observed_date']=dt
    param['observed_year']=dt.year
    param['userid']=userid 
    param['loc_id']=loc_id.upper()
    #**Insert dt_catalog items return primary key dictionary
    dic = md.catalog(param)
    dic['location']=loc_id.upper()
    dic['file']=fname
    dic['observed_date']= dt
    return dic
def event_LocalFile(filepath,catDict):
    md.event_local_file(catDict['commons_id'],catDict['cat_id'], filepath,Server,userid)
def event_Mongo(filepath,catDict):
    Query='db.' + MongoCollection + '.find({cat_id:' + str(catDict['cat_id']) + '})'
    md.event_MongoDB_Access(catDict['commons_id'],catDict['cat_id'], MongoDB,MongoCollection,Query,Server,userid)
def event_RemoteWS(filepath,catDict):
    URL='http://www.mesonet.org/index.php/dataMdfMts/dataController/getFile/' + catDict['file'][0:12] + '/mts/TEXT/'
    addDict = {'event_name':'Remote Web Service','event_desc':'Remote Source Web Service'}
    md.event_WebService(catDict['commons_id'],catDict['cat_id'],URL,'Remote_Web_Service',userid,eventUpdateDict=addDict)
def event_LocalWS(filepath,catDict):
    URL="http://fire.rccc.ou.edu/mongo/db_find/" + MongoDB + "/" + MongoCollection + "/{'spec':{'cat_id':" + str(catDict['cat_id']) + "}}/"
    addDict = {'event_name':'Local Web Service','event_desc':'Local Mongo data Web Service'}
    md.event_WebService(catDict['commons_id'],catDict['cat_id'],URL,'Local_Web_Service',userid,eventUpdateDict=addDict)
def insertmongo(filepath,addDict1):
    ml.file2mongo(filepath,MongoCollection,file_type='fixed_width',addDict=addDict1,specificOperation=calcTime,skiplines=2)
def calcTime(row):
    try:
        minuts = row['TIME']
        dt = row['observed_date']
        diff = timedelta(minutes=int(minuts))
        newdt=dt + diff #Add minutes to base time for each individual record
        row['observed_date']=newdt
        return row
    except:
        raise
def iterate_file():
    f1=open(file_find_results,'r')
    i=0
    for file in f1:
        loadMD_Mongo(file.rstrip('\n'))    
        i=i+1
        print str(i) + ' ' + file
    f1.close()
#*************Call Functions******************
iterate_file()
