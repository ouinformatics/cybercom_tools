import cherrypy
import json, os #, math,commands,ast
#import urllib
#import pickle
#from celery.result import AsyncResult
#from celery.execute import send_task
#from celery.task.control import inspect
#from pymongo import Connection
from datetime import datetime
from Cheetah.Template import Template
import mdb_model
from json_handler import handler
'''

MongoDB web interface with 

'''
templatepath= os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

def mimetype(type):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = type
            return func(*args, **kwargs)
        return wrapper
    return decorate

class Root(object):
    def __init__(self,mongoHost='fire.rccc.ou.edu',port=27017,database='cybercom_queue',collection='task_log'):
        self.mongo = mdb_model.mongo_catalog()
    @cherrypy.expose
    def data(self,db=None,col=None,query={},record=1,page=1,nPerpage=500, **kwargs):
        fname='data'
        if not db:
            res= self.mongo.getdatabase()
            res.sort()
            nameSpace = dict(database=res,baseurl=cherrypy.url('/')[:-1],FName=fname)        
            t = Template(file = templatepath + '/database.tmpl', searchList=[nameSpace])
            return t.respond()
        if not col:
            res= self.mongo.getcollections(db)
            res.sort()
            nameSpace = dict(database=db,collection=res,baseurl=cherrypy.url('/')[:-1],FName=fname)
            t = Template(file = templatepath + '/collection.tmpl', searchList=[nameSpace])
            return t.respond()
        if record == 'json':
            skip=(int(page)-1)*int(nPerpage)
            limit= int(nPerpage)
            dump_out=[]
            cur = self.mongo.getDoc(db,col,query,skip,limit)
            for item in cur:
                dump_out.append(item)
            serialized = json.dumps(dump_out, default = handler, sort_keys=True, indent=4)
            cur =''
            prev=1
            next=1
        else:
            skip=(int(record)-1)
            prev=int(record)-1
            if prev < 1: 
                prev=1
            next=int(record)+1
            limit=1
            serialized=''
            cur = self.mongo.getDoc(db,col,query,skip,limit)#.skip(int(record)-1).limit(1)
        nameSpace = dict(database=db,collection=col,data=cur,baseurl=cherrypy.url('/')[:-1],serial=serialized,FName=fname,prev=prev,next=next)
        t = Template(file = templatepath + '/data.tmpl', searchList=[nameSpace])
        return t.respond()
    @cherrypy.expose
    def save(self, **kwrgs):
        if cherrypy.request.method =="POST":
            try:
                doc=cherrypy.request.params
                print str(doc)
                db= doc['database']
                col=doc['collection']
                doc.pop('database')
                doc.pop('collection')
                return self.mongo.save(db,col,doc)#'commons',cherrypy.request.params)
            except Exception as inst:
                return str(inst)
        else:
            return 'Error: Save only accepts posts'
cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

