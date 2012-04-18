import cherrypy
import json, os, math,commands,ast
import urllib
import pickle
from celery.result import AsyncResult
from celery.execute import send_task
from celery.task.control import inspect
from pymongo import Connection
from datetime import datetime
from Cheetah.Template import Template

templatepath= os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

def check_memcache(host='127.0.0.1',port=11211):
    ''' Check if memcache server is running '''
    import socket
    s = socket.socket()
    try:
        s.connect((host,port))
        return True
    except:
        return False

if check_memcache():
    import memcache 
else:
    memcache = None

def update_tasks():
    ''' Enable the use of memcache to save tasks and queues when possible '''
    i = inspect()
    if memcache:
        mc = memcache.Client(['127.0.0.1:11211'])
        tasks = 'REGISTERED_TASKS'
        queues = 'AVAILABLE_QUEUES'
        REGISTERED_TASKS = mc.get(tasks)
        AVAILABLE_QUEUES = mc.get(queues)
        if not REGISTERED_TASKS:
            REGISTERED_TASKS = set()
            for item in i.registered().values():
                REGISTERED_TASKS.update(item)
            mc.set(tasks, REGISTERED_TASKS, 10)
            REGISTERED_TASKS = mc.get('REGISTERED_TASKS')
        if not AVAILABLE_QUEUES:
            mc.set(queues, set([ item[0]['exchange']['name'] for item in i.active_queues().values() ]), 10)
            AVAILABLE_QUEUES = mc.get('AVAILABLE_QUEUES')
    else:
        REGISTERED_TASKS = set()
        for item in i.registered().values():
            REGISTERED_TASKS.update(item)

        AVAILABLE_QUEUES = set([ item[0]['exchange']['name'] for item in i.active_queues().values() ])
    return (REGISTERED_TASKS,AVAILABLE_QUEUES)
            

def mimetype(type):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = type
            return func(*args, **kwargs)
        return wrapper
    return decorate

class Root(object):
    def __init__(self,mongoHost='localhost',port=27017,database='cybercom_queue',collection='task_log'):
        self.db = Connection(mongoHost,port)#[database]
        self.database = database
        self.collection = collection
    @cherrypy.expose
    @mimetype('text/html')
    def index(self):
        doc = """<html><body><ul><li><a href="report">report</a></li><li><a href="usertasks">tasks</a></li> </ul></body></html>"""
        return doc
    @cherrypy.expose
    @mimetype('text/html')
    def usertasks(self,task_name=None,pageNumber=1,nPerPage=1500,callback=None,**kwargs):
        ''' usertasks returns celery tasks perform and the link to the task result page.
            task_name-  string optional
            pageNumber and nPerPage is optional
        ''' 
        db=self.db[self.database][self.collection]
        try:
            page=int(pageNumber)
            perPage=int(nPerPage)
        except:
            page=1
            perPage=100
        try:
            if cherrypy.request.login:
                user = cherrypy.request.login
            else:
                user = "guest"
        except:
            pass 
        if not task_name:
            res=db.find({'user':user}).skip((page-1)* int(nPerPage)).limit(int(nPerPage)).sort([('timestamp',-1)]) 
            rows=db.find({'user':user}).count()
        else:
            res=db.find({'user':user,'task_name':task_name}).skip((page-1) * int(nPerPage)).limit(int(nPerPage)).sort([('timestamp',-1)])
            rows=db.find({'user':user,'task_name':task_name}).count()
        ePage= int(math.ceil(float(rows)/float(perPage)))
        nameSpace = dict(tasks=res,page=page,endPage=ePage)#tresult)
        #t = Template(file = templatepath + '/usertasks.tmpl', searchList=[nameSpace])
        if callback:
            t = Template(file = templatepath + '/usertasks_call.tmpl', searchList=[nameSpace])
            return str(callback) + "(" + json.dumps({'html':t.respond()}) + ")"
        else:
            t = Template(file = templatepath + '/usertasks.tmpl', searchList=[nameSpace])
            return t.respond()
    @cherrypy.expose
    @mimetype('text/html')
    def report(self,taskid,callback=None,**kwargs):
        ''' Generates task result page. This description provides provenance and all information need to rerun tasks
            taskid is required
        '''
        db=self.db[self.database]
        res=db[self.collection].find({'task_id':taskid})
        resb = {}
        tresult=db['cybercom_queue_meta'].find({'_id':taskid})
        if not tresult.count() == 0:
            resb['Completed']=str(tresult[0]['date_done'])
            resb['Result'] = pickle.loads(tresult[0]['result'].encode())
            try:
                urlcheck = commands.getoutput("wget --spider " + resb['Result'] + " 2>&1| grep 'Remote file exists'")
                if urlcheck:
                    resb['Result']='<a href="' + resb['Result'] + '" target="_blank">' + resb['Result'] + '</a>'
            except:
                pass
            resb['Status'] = tresult[0]['status']
            resb['Traceback'] =pickle.loads( tresult[0]['traceback'].encode())
        for row in res:
            resclone=row
            for k,v in resclone['kwargs'].items():
                try:
                    temp = ast.literal_eval(v)
                    if type(temp) is dict:
                        hml = "<table class='table table-border'>"
                        for key, val in temp.items():
                            hml = hml + "<tr><td>" + str(key) + "</td><td>" + str(val) + "</td></tr>"
                        hml = hml + "</table>"
                        resclone['kwargs'][k]=hml
                except:
                    pass
        nameSpace = dict(tasks=[resclone],task_id=taskid,tomb=[resb])
        #t = Template(file=templatepath + '/result.tmpl', searchList=[nameSpace])
        if callback:
            t = Template(file=templatepath + '/result_call.tmpl', searchList=[nameSpace])
            return str(callback) + "(" + json.dumps({'html':t.respond()}) + ")"   
        else:
            t = Template(file=templatepath + '/result.tmpl', searchList=[nameSpace])
            return t.respond()
    @cherrypy.expose
    @mimetype('application/json')
    def run(self,*args,**kwargs):
        REGISTERED_TASKS,AVAILABLE_QUEUES = update_tasks()
        #return REGISTERED_TASKS
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
            rtasks = list(REGISTERED_TASKS)
            rtasks.sort() 
            return json.dumps({'error': "Unknown task", 'available_tasks': rtasks}, indent=2)
        if queue not in AVAILABLE_QUEUES: # Check if queue is known, if not show possible queue
            aqs = list(AVAILABLE_QUEUES)
            aqs.sort() 
            return json.dumps({'error': "Unknown queue", 'available_queues': aqs}, indent=2)
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
            self.db[self.database][self.collection].insert({'task_id':taskobj.task_id,'user':user,'task_name':funcname,'args':args,'kwargs':kwargs,'queue':queue,'timestamp':datetime.now()})
        except:
            pass
        if not callback:
            return json.dumps({'task_id':taskobj.task_id}, indent=2)
        else:
            return str(callback) + "(" + json.dumps({'task_id':taskobj.task_id}, indent=2) + ")"
    @cherrypy.expose
    @mimetype('application/json')
    def task(self,task_id=None,type=None,callback=None,**kwargs):
        try:
            if callback == None:
                return self.serialize(task_id,type)
            else:
                return str(callback) + '(' + self.serialize(task_id,type) + ')'
        except Exception as inst:
            #error = str(type(inst)) + '\n'
            #error = error + str(inst)
            return str(inst)#error
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
            if len(res['tombstone']) > 0:
                res['tombstone'][0]['result'] = pickle.loads(res['tombstone'][0]['result'].encode())
            res['task_id']=task_id
            return json.dumps(res,indent=2) #result.read()
        return json.dumps({'available_urls':['/<task_id>/','/<task_id>/status/','/<task_id>/tombstone/']},indent=2)
cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

