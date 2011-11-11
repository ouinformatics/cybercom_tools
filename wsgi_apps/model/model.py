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
    def teco(self,task_type=None,**kwargs):
        if task_type == None:
            return json.dumps({'available_urls':['run/','setinput/']},indent=2)
        if task_type.upper() == 'SETINPUT':
            res = task.getTecoinput.apply_async([],queue='celery')
            return json.dumps({'task_id':res.task_id},indent=2)#res.task_id
        if task_type.upper() == 'RUN':
            res= task.runTeco.apply_async(["f"],queue='celery')   
            return json.dumps({'task_id':res.task_id},indent=2)#res.task_id
        return json.dumps({'available_urls':['run/','setinput/']},indent=2)
cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

