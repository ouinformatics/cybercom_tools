import cherrypy
import json, os #, math,commands 
#import urllib
#import pickle
#from celery.result import AsyncResult
#from celery.execute import send_task
#from celery.task.control import inspect
from pymongo import Connection
from datetime import datetime
from Cheetah.Template import Template
'''

Method name lookups should eventually be driven by catalog.
[
('teco', 'cybercomq.model.teco.task.runTeco'),
('setTecoInput', 'cybercomq.model.teco.task.setTecoinput')
]


'''
templatepath= os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
print templatepath

def mimetype(type):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = type
            return func(*args, **kwargs)
        return wrapper
    return decorate

class Root(object):
    def __init__(self,mongoHost='localhost',port=27017,database='teco',collection='forcing'):
        self.db = Connection(mongoHost,port)#[database]
        self.database = database
        self.collection = collection
    @cherrypy.expose
    def index(self):
        return None
    @cherrypy.expose
    #@mimetype('application/javascript')
    def tecodata(self,site='US-HA1',upload=None,model=None,callback=None,**kwargs):
        ''' usertasks returns celery tasks perform and the link to the task result page.
            task_name-  string optional
            pageNumber and nPerPage is optional
        ''' 
        #db=self.db[self.database][self.collection]
        if model:
            if upload:
                yrs=self.db[self.database]['uploaded_grass'].find({'Site':site,'user':upload}).distinct('year')
            else:
                yrs=self.db[self.database]['years'].find_one({'Site':site,'type':model})['years']
        else:
            if upload:
                yrs=self.db[self.database]['uploaded_data'].find({'Site':site,'user':upload}).distinct('Year')
            else:
            #yrs=self.db[self.database][self.collection].find({'Site':site}).distinct('Year')
                yrs=self.db[self.database]['years'].find_one({'Site':site,'type':'default'})['years']
        yrs.sort()
        nameSpace = dict(years=yrs,site=site,start=yrs[0],end=yrs[-1])
        if callback:
            cherrypy.response.headers['Content-Type'] = "application/json"
            t = Template(file = templatepath + '/tecodata_call.tmpl', searchList=[nameSpace])
            return str(callback) + "(" + json.dumps({'html':t.respond()}) + ")"
        else:
            cherrypy.response.headers['Content-Type'] = "text/html"
            t = Template(file = templatepath + '/tecodata.tmpl', searchList=[nameSpace])
            return t.respond()
    @cherrypy.expose
    # @mimetype('application/javascript')
    def tecositeparam(self,site='US-HA1',model=None,callback=None,**kwargs):
        ''' usertasks returns celery tasks perform and the link to the task result page.
            task_name-  string optional
            pageNumber and nPerPage is optional
        '''
        if model=='grassland':
            db=self.db[self.database]['siteparam_grass']
            sp=db.find({'site':site})
            col1 =["spinup_years","Lat","Co2ca","a1","Ds0","Vcmx0","extku","xfang"]
            col2 =["alpha","stom_n","Wsmax","Wsmin","rdepth","SLA","LAIMAX","LAIMIN"]
            col3 = ['nsc',"Storage",'Q_leaf','Q_wood','Q_root1','Q_root2','Q_root3','Q_coarse','Q_fine',"Q_soil1","Q_soil2","Q_soil3"]
            hidden=["rfibre","output","Rootmax","Stemmax","SenS","SenR"]#["site"]
            carboncol=[]
            labels={"spinup_years":{"label":"Spin-up Years","tooltip":"Spin-up Years"},
                    "Lat":{"label":"Latitude","tooltip":"Site Latitude"},
                    "Co2ca":{"label":"Co2 Concentration","tooltip":"Co2 Concentration(ppm)"},
                    "output":{"label":"Output Integer","tooltip":"Output Integer"},
                    "a1":{"label":"a1 coefficient","tooltip":"a1 is an empirical coefficient in the photosythetic process (See Wang & leuning - 1998)"},
                    "Ds0":{"label":"Ds0 coefficient","tooltip":" Ds0 is a coefficient related to VPD (Vapor Pressure Deficit) to affect Stomata Coductance in photosythetic subroutines"},
                    "Vcmx0":{"label":"Maximum Rate of Carboxylation (Vcmx0)","tooltip":"Maximum rate of Carboxylation"},
                    "extku":{"label":"Extinction Coefficient (extku)","tooltip":"Extinction Coefficient"},
                    "xfang":{"label":"Coefficient in Photosythesis Subroutine (xfang)","tooltip":"Coefficient in Photosythesis Subroutine(Reference - Sellers 1985 eq.13)"},
                    "alpha":{"label":"Light use efficiency (alpha)","tooltip":"Light use efficiency(alpha)"},
                    "stom_n":{"label":"Stoma Number (stom_n)","tooltip":"Stoma Number: 1 equals only in one side of leaf, 2 equals Stoma in both leaf sides"},
                    "Wsmax":{"label":"Maximum soil water (Wsmax)","tooltip":"Maximum soil water"},
                    "Wsmin":{"label":"Minimum soil water (Wsmin)","tooltip":"Minimum soil water"},
                    "rdepth":{"label":"Root Depth (rdepth)","tooltip":"Root Depth (rdepth)"},
                    "SLA":{"label":"Specific Leaf Area (SLA)","tooltip":"Specific Leaf Area (ratio: leaf area/leaf dry weight)"},
                    "LAIMIN":{"label":"Minimum LAI","tooltip":"Minimum Leaf Area Index"},
                    "LAIMAX":{"label":"Maximum LAI","tooltip":"Maximum Leaf Area Index"},
                    "nsc":{"label":"Non Structural Carbon","tooltip":"Initial Non Structural Carbon"},
                    "Storage":{"label":"Storage of Carbon for leaf flush","tooltip":"Initial Storage of Carbon for leaf flush"},
                    "Q_leaf":{"label":"Leaf Carbon Pool Size (Q_leaf)","tooltip":"Initial Leaf Carbon Pool Size (Q_leaf)"},
                    "Q_wood":{"label":"Wood Carbon Pool Size (Q_wood)","tooltip":"Initial Wood Carbon Pool Size (Q_wood)"},
                    "Q_root1":{"label":"Root1 Carbon Pool Size (Q_root1)","tooltip":"Initial Root1 Carbon Pool Size (Q_root1)"},
                    "Q_root2":{"label":"Root2 Carbon Pool Size (Q_root2)","tooltip":"Initial Root2 Carbon Pool Size (Q_root2)"},
                    "Q_root3":{"label":"Root3 Carbon Pool Size (Q_root3)","tooltip":"Initial Root3 Carbon Pool Size (Q_root3)"},
                    "Q_coarse":{"label":"Coarse-litter Carbon Pool Size (Q_coarse)","tooltip":"Initital Coarse-litter Carbon Pool Size (Q_coarse"},
                    "Q_fine":{"label":"Fine-litter Carbon Pool Size (Q_fine)","tooltip":"Initial Fine-litter Carbon Pool Size (Q_fine)"},
                    "Q_soil1":{"label":"Soil1 Carbon Pool Size (Q_soil1)","tooltip":"Initial Soil1 Carbon Pool Size (Q_soil1)"},
                    "Q_soil2":{"label":"Soil2 Carbon Pool Size (Q_soil2)","tooltip":"Initial Soil2 Carbon Pool Size (Q_soil2)"},
                    "Q_soil3":{"label":"Soil3 Carbon Pool Size (Q_soil3)","tooltip":"Initial Soil3 Carbon Pool Size (Q_soil3)"},
                    }              
        else:
            db=self.db[self.database]['siteparam']# Default Site Parameters
            sp=db.find({'site':site})#.distinct('Year')#.sort()#,{'Site':site}).sort()
            col1 =[ 'vegtype','wsmax','wsmin','gddonset','LAIMAX','LAIMIN','rdepth','Rootmax','Stemmax','SapR','SapS','SLA','GLmax']
            col2 =['GRmax','Gsmax','stom_n','a1','Ds0','Vcmx0','extkU','xfang','alpha','co2ca','Tau_Leaf','Tau_Wood','Tau_Root']
            col3=['Tau_F','Tau_C','Tau_Micro','Tau_SlowSOM','Tau_Passive','TminV','TmaxV','ToptV','Tcold','Gamma_Wmax','Gamma_Tmax']
            hidden=['site','inputfile','NEEfile','outputfile','lat','Longitude']
            carboncol=['nsc','Q_leaf','Q_wood','Q_root1','Q_root2','Q_root3','Q_coarse','Q_fine','Q_micr','Q_slow','Q_pass','S_w_min','Q10_h']
            labels={}
        #    'vegtype','GRmax','LAIMAX','co2ca','Tau_Leaf','Ds0','extkU','wsmax']
        #col2=['SapR','SapS','Vcmx0','wsmin','stom_n','Gsmax','Tau_Micro','Longitude','xfang','a1',
        #    'Rootmax','lat','alpha','SLA','Tau_F','Tau_C','Tau_Root','gddonset','Tau_SlowSOM','_id','inputfile']

        #yrs.sort()
        #res = sp.next()
        nameSpace = dict(siteparam=sp,site=site,col1=col1,col2=col2,col3=col3,hidden=hidden,carboncol=carboncol,label=labels)#tresult)
        #print nameSpace
        #t = Template(file = templatepath + '/siteparam.tmpl', searchList=[nameSpace])
        if callback:
            cherrypy.response.headers['Content-Type'] = "application/json"
            t = Template(file = templatepath + '/siteparam_call.tmpl', searchList=[nameSpace])
            return str(callback) + "(" + json.dumps({'html':t.respond()}) + ")"
        else:
            cherrypy.response.headers['Content-Type'] = "text/html"
            t = Template(file = templatepath + '/siteparam.tmpl', searchList=[nameSpace])
            return t.respond()
    def mongoform(self):
        pass
    @cherrypy.expose
    @mimetype('application/javascript')
    def getSite(self,callback=None,**kwargs):
        f1= urllib.urlopen('http://genexpdb.ou.edu/teco/')    
        result = f1.read()
        result=result.replace('<link type="text/css" href="/web/eco/jquery-ui-1.8.13.custom.css" rel="Stylesheet"/>',"")
        result=result.replace('<script type="text/javascript" src="/web/eco/jquery-1.6.2.min.js"></script>',"")
        result=result.replace('<script type="text/javascript" src="/web/eco/jquery-ui-1.8.10.custom.min.js"></script>',"")
        result=result.replace('<script type="text/javascript" src="/web/eco/OpenLayers-2.10/OpenLayers.js"></script>','')
        #result=result.replace('<table>','<table class="table-striped table-bordered table-condensed">')
        if callback:
            return str(callback) + "(" + json.dumps({'html':result}) + ")"
        else:
            return result
    @cherrypy.expose
    @mimetype('application/javascript')
    def getLocations(self,callback=None,update=None,**kwargs):
        # db = Connection('fire.rccc.ou.edu')
        if update:
            #check if site in siteparams
            siteparam = self.db[self.database]['siteparam'].distinct('site')
            #   check if site in forcing data
            forcing = self.db[self.database]['forcing'].distinct('Site')
            sites=[]
            for site in forcing:
                if site in siteparam:
                    sites.append(site)
            findloc=[]
            #check if catalog location metadata
            for row in sites:
                for rr in  self.db['catalog']['location'].find({'loc_id':row}):
                    findloc.append(row)
        else:
            #for rr in self.db['catalog']['location'].find({'commons_id':300,'loc_id':{$in:['US-HA1','US-ARM','US-ATQ','US-BRW','US-DK2','US-DK3','US-UMB','US-VAR','US-NE3','US-NE1','US-SYV','US-LOS','US-ME2','US-TON','US-SO2','US-WCR','US-IB1','US-MOZ','US-MMS','US-IB2','US-HO1','US-NR1','US-PFA','US-SHD','US-NE2']}}):
            findloc=['US-HA1','US-ARM','US-ATQ','US-BRW','US-DK2','US-DK3','US-UMB','US-VAR','US-NE3','US-NE1','US-SYV','US-LOS','US-ME2','US-TON','US-SO2','US-WCR','US-IB1','US-MOZ','US-MMS','US-IB2','US-HO1','US-NR1','US-PFA','US-SHD','US-NE2']
        if callback:
            return str(callback) + "(" + json.dumps({'location':findloc}) + ")"
        else:
            return json.dumps({'location':findloc})
cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

