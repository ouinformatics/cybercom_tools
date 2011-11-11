import cherrypy
import json 
import urllib
from celery.result import AsyncResult
from cybercomq.model.teco import task

def mimetype(type):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = type
            return func(*args, **kwargs)
        return wrapper
    return decorate

class Root(object):
    @cherrypy.expose
    def index(self):
        return None
    @cherrypy.expose
    @mimetype('application/json')
    def runTeco(self,task_type,**kwargs):
        if task_type == 'input':
        if task_type == 'runTeco':
            res= task.runTeco.    
    @cherrypy.expose
    @mimetype('application/json')
    def getStatus(self,task_id,**kwargs):# db=None, col=None, query=None, callback=None, showids=None, date=None, **kwargs):
        """ 
        Celery Status web service
        """
        return json.dumps({"status": AsyncResult(task_id).status})
    @cherrypy.expose
    @mimetype('application/json')
    def getTombstone(self,task_id,**kwargs):
        result = urllib.urlopen("http://fire.rccc.ou.edu/mongo/db_find/cybercom_queue/cybercom_queue_meta/{'spec':{'_id':'" + task_id + "'}}/Tombstone/True/")
        return result.read()
    @cherrypy.expose
    @mimetype('application/json')
    def task(self,task_id,type=None,**kwargs):
        if type == 'status':
            return json.dumps({"status": AsyncResult(task_id).status},indent=2)
        if type == 'tombstone':
            res={}
            result = urllib.urlopen("http://fire.rccc.ou.edu/mongo/db_find/cybercom_queue/cybercom_queue_meta/{'spec':{'_id':'" + task_id + "'}}")
            res['tombstone']=json.loads(result.read())
            res['task_id']=task_id            
            return json.dumps(res,indent=2) #result.read()
        if type == None:
            res = {}
            result = urllib.urlopen("http://fire.rccc.ou.edu/mongo/db_find/cybercom_queue/cybercom_queue_meta/{'spec':{'_id':'" + task_id + "'}}")
            res["tombstone"]=json.loads(result.read())
            res['status']=AsyncResult(task_id).status
            res['task_id']=task_id
            return json.dumps(res,indent=2)
cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

