import cherrypy
import json 
import urllib
import pickle
from celery.result import AsyncResult
from celery.execute import send_task
from celery.task.control import inspect
from pymongo import Connection
from datetime import datetime

'''
Run without arguments:
www.cybercommons.org/api/q/run/cybercom.teco.tasks.runTeco/arg1/arg2?kwarg1=SomeArg

Run with positional arguments
www.cybercommons.org/api/q/run/teco/SomeString/Anotherstring/

Run with keyword arguments:
www.cybercommons.org/api/q/run/teco?arg1=SomeString&arg2=Anotherstring

www.cybercommons.org/api/q/status/UUID


Method name lookups should be driven by catalog.
[
('teco', 'cybercomq.model.teco.task.runTeco'),
('setTecoInput', 'cybercomq.model.teco.task.setTecoinput')
]


'''

i = inspect()
REGISTERED_TASKS = set()
for item in i.registered().values():
    REGISTERED_TASKS.update(item)

AVAILABLE_QUEUES = set([ item[0]['exchange']['name'] for item in i.active_queues().values() ])


def mimetype(type):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = type
            return func(*args, **kwargs)
        return wrapper
    return decorate

class Root(object):
    def __init__(self,mongoHost='fire.rccc.ou.edu',port=27017,database='cybercom_queue',collection='task_log'):
        self.db = Connection(mongoHost,port)[database]
        self.collection = collection
    @cherrypy.expose
    def index(self):
        return None
    @cherrypy.expose
    @mimetype('application/json')
    def run(self,*args,**kwargs):
        # If no arguments return list of tasks
        if len(args) == 0:
            return json.dumps({'error': "Unknown task", 'available_tasks': list(REGISTERED_TASKS)}, indent=2)
        funcq = args[0].split('@') #split function queue 
        funcname = funcq[0] # Get function name for calling
        if len(funcq) == 1: # Set default queue to celery if none defined
            queue = 'celery'
        else:
            queue = funcq[1]
        if funcname not in REGISTERED_TASKS: # Check if funcname is know, if not show possible names
            return json.dumps({'error': "Unknown task", 'available_tasks': list(REGISTERED_TASKS)}, indent=2)
        if queue not in AVAILABLE_QUEUES: # Check if queue is known, if not show possible queue
            return json.dumps({'error': "Unknown queue", 'available_queues': list(AVAILABLE_QUEUES)}, indent=2)
        funcargs = args[1:] # Slice out function arguments for passing along to task.
        
        if kwargs.has_key('callback'):
            callback = kwargs.pop('callback') # pop off callback so it doesn't get passed
            kwargs.pop('_')
        else:
            callback = None
        
        taskobj = send_task( funcname, args=funcargs, kwargs=kwargs, queue=queue, track_started=True )
        #logging tasks performed
        try:
            if cherrypy.request.login:
                user = cherrypy.request.login
            else:
                user = "Anonymous"
            self.db[self.collection].insert({'task_id':taskobj.task_id,'user':user,'task_name':funcname,'args':args,'kwargs':kwargs,'queue':queue,'timestamp':datetime.now()})
        except:
            pass
        if not callback:
            return json.dumps({'task_id':taskobj.task_id}, indent=2)
        else:
            return str(callback) + "(" + json.dumps({'task_id':taskobj.task_id}, indent=2) + ")"
    @cherrypy.expose
    @mimetype('application/json')
    def task(self,task_id=None,type=None,callback=None,**kwargs):
        if callback == None:
            return self.serialize(task_id,type)
        else:
            return str(callback) + '(' + self.serialize(task_id,type) + ')'
    def serialize(self,task_id,type):
        if task_id == None:
            return json.dumps({'available_urls':['/<task_id>/','/<task_id>/status/','/<task_id>/tombstone/']},indent=2)
        if type == None:
            res = {}
            result = urllib.urlopen("http://fire.rccc.ou.edu/mongo/db_find/cybercom_queue/cybercom_queue_meta/{'spec':{'_id':'" + task_id + "'}}")
            res["tombstone"] = json.loads(result.read())
            if len(res['tombstone']) > 0:
                res['tombstone'][0]['result'] = pickle.loads(res['tombstone'][0]['result'].encode())
            res['status']=AsyncResult(task_id).status
            res['task_id']=task_id
            return json.dumps(res,indent=2)
        if type.lower() == 'status':
            return json.dumps({"status": AsyncResult(task_id).status},indent=2)
        if type.lower() == 'tombstone':
            res={}
            result = urllib.urlopen("http://fire.rccc.ou.edu/mongo/db_find/cybercom_queue/cybercom_queue_meta/{'spec':{'_id':'" + task_id + "'}}")
            res['tombstone']=json.loads(result.read())
            res['task_id']=task_id
            return json.dumps(res,indent=2) #result.read()
        return json.dumps({'available_urls':['/<task_id>/','/<task_id>/status/','/<task_id>/tombstone/']},indent=2)
cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

