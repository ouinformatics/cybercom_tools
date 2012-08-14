from pymongo import ReplicaSetConnection, Connection, ReadPreference
from pymongo.objectid import ObjectId
import ConfigParser,os,ast,pymongo


#appdir = os.path.join(os.path.expanduser('~'), '.cybercom')

class mongo_catalog():

    def __init__(self,configfile='.cybercom',appdir='~'):
       # cfgfile = os.path.join(os.path.expanduser(appdir), configfile)
       # config= ConfigParser.RawConfigParser()
       # config.read(cfgfile)
        #slaveOk = ast.literal_eval(config.get('database','slave_ok'))
        #readpreference = config.get('database','read_preference')#,'SECONDARY')
        #SECONDARY
        #pymongo.ReadPreference= readpreference
        #self.dbconn = Connection(config.get('database','host'))
        self.dbcon = Connection('129.15.41.76')#config.get('database','host'),replicaset=config.get('database','replica_set'))#,read_preference=0)
        #self.db= self.dbconn[config.get('catalog','database')]
        self.dbcon.read_preference = ReadPreference.SECONDARY
    def getdatabase(self, **kwargs):
        return self.dbcon.database_names()
    def getcollections(self,database):
        return self.dbcon[database].collection_names()
    def getInfo(self,db,collection,query=None,skip=0,limit=0):
        info = {}
        if query:
            query = ast.literal_eval(query)
            info['totalRecords']=self.dbcon[db][collection].find(**query).count()
        else:
            info['totalRecords']=self.dbcon[db][collection].find().count()
        if info['totalRecords'] > skip + limit:
            info['startRecord']=skip + 1
            info['endRecord']=skip + limit
        else:
            info['startRecord']=skip + 1
            info['endRecord']=info['totalRecords']
        info['totalCollection']=self.dbcon[db][collection].find().count()
        return info

    def getDoc(self,db,collection,query=None,skip=0,limit=0):
        #return self.db.collection_names()
        if query:
            query = ast.literal_eval(query)
            cur = self.dbcon[db][collection].find(**query).skip(skip).limit(limit)
        else:
            cur = self.dbcon[db][collection].find().skip(skip).limit(limit)
        return cur #self.db[collection].find(query,fields)        
    def save(self,db,collection,document):
        return "Save turned off while no auth in place for MongoDB"
        if document['_id']:
            document['_id']=ObjectId(document['_id'])
        return self.dbcon[db][collection].save(document)
    def getIndexes(self,database,collection):
            return self.dbcon[database][collection].index_information()
    def getkeys(self,database,collection,popID=True):
        col=database + "." + collection  #+ ".Keys"
        cur = self.dbcon['mongoSchema'][col].find({'value.type':{'$nin':['function','object']}})#{'$ne':'function'}})
        cur1= self.dbcon['mongoSchema'][col].find({'value.type':{'$nin':['function']}})
        out=[]
        for row in cur:
            if not (row['_id']['key']=='_id' and popID):
                out.append(row['_id']['key'])
        cols=[]
        for row in cur1:
            if not (row['_id']['key']=='_id' and popID):
                cols.append(row['_id']['key'])
        out.sort()
        cols.sort()
        return out,cols
    def getID_timestamp(self,id,type='iso_string'):
        if type == 'iso_string':
            try:
                return str(ObjectId(id).generation_time)
            except:
                return str(id.generation_time)
    def seqNext(self,sequence,collection='sequences'):
        #result = self.db.runCommand( { "findandmodify" : collection,"query" : { "name" :sequence},"update" : { $inc : { "id" : 1 }},"new" : true } ) 
        result=self.db.command("findandmodify", collection, query={"name":sequence}, update={"$inc":{"id":1}}, new=1)
        return result['value']['id']       
