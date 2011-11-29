from xmlrpclib import ServerProxy
from rpc4django.utils import CookieTransport
from datetime import datetime, timedelta
import  os,dataloader  #commands, smtplib,os, dataloader
import ConfigParser
#get username and password from .cybercom file in home directory
config_file = os.path.join(os.path.expanduser('~'),'.cybercom')
config = ConfigParser.RawConfigParser()
config.readfp(open(config_file, 'r'))
username = config.get('api','user')
password = config.get('api','password')
#import sys.argv as argv
#*******Configuration variables******************
Server='panda.rccc.ou.edu'
commonsID = 807


class eomfSync():
    '''sync files to cybercom catalog with files store with file with find command'''
    def __init__(self,URL,user,passwd,findfile):
        #self.location ={}
        #self.initLocation()
        self.split=[]
        self.catid = {'aerosolmask':1452140,'blue':1452141,'phenology':1452142,'ndwi':1452143,'ndsi':1452144,'snow':1452145,
                        'cloudmask':1452146,'oceanmask':1452147,'lswi':1452148,'evi':1452149,'ndvi':1452150}
        self.commonsID = 807
        self.mdl = dataloader.Metadata_load()#msg='\n\r'
        self.user = user
        self.passwd = passwd
        self.findfile= findfile
        self.Server = ServerProxy(URL, transport=CookieTransport(),use_datetime=True)
        try:
            self.Server.system.login(user,passwd)
        except:
            raise
        #self.session.autoflush=False
    def iterate_file(self):
        i=1
        f1 = open(self.findfile,'r')
        f2 = open('error_files.dat','w')
        for file in f1:
            i=i+1
            self.split = file.split('/')
            catid = self.get_catid()
            if catid == None:
                pass
            else:
                fname = self.split[10].replace('\n','').replace('\r','')
                loc = self.split[9]
                if self.checkEvent(catid,fname):#check if file exists! slow need to use datalayer instead of JSONRPC
                    if not self.insertEventResult(catid,loc,fname,file.replace('\n','').replace('\r','')):
                        f2.write(file)
            if i%10000 == 0:
                print i    
    def insertEventResult(self,catid,loc,fname,filepath):
        try:
            tmp = fname.split('.')
            cdate = datetime.strptime(tmp[1],'A%Y%j')
            sdate = str(cdate)
        except:
            try:
                t2= tmp[0].split('_')
                cdate = datetime.strptime(t2[1],'%Y%j')
                sdate=str(cdate)
            except:
                return False
                #sdate= ''
        try:
            URL=filepath.replace('/data/','http://panda.rccc.ou.edu/')
            erow={'commons_id':self.commonsID,'cat_id':catid,'event_name':fname,'loc_id':loc.upper(),'event_method':'Local_File','event_date':sdate}
            lrow=[{'commons_id':self.commonsID,'var_id':'URL','result_text':URL,'result_order':1},
                  {'commons_id':self.commonsID,'var_id':'Server','result_text':Server,'result_order':2},
                  {'commons_id':self.commonsID,'var_id':'File_Path','result_text':filepath,'result_order':3}]
            self.mdl.event_result(erow,lrow)
            #self.Server.catalog.EventResult(erow,lrow)
            return True
        except:
            return False
    def get_catid(self):
        folder = self.split[7]
        try:
            return self.catid[folder.lower()]
        except:
            return None
    def checkEvent(self,catid,file_name):
        if not self.Server.catalog.getEventItems_byName({'commons_id':commonsID,'cat_id':catid,'event_name':file_name}) == [] :
            return True
        else:
            return False

sync = eomfSync('http://test.cybercommons.org/dataportal/RPC2/',username,password,'vol05_prod_files.dat')#vol22.dat')#02_prod_files.dat')
sync.iterate_file()
