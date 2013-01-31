import cherrypy,codecs,ast
import json, os,csv #, math,commands 
from StringIO import StringIO
#import urllib
#import pickle
#from celery.result import AsyncResult
#from celery.execute import send_task
#from celery.task.control import inspect
from pymongo import Connection
import cookielib
import Cookie
import time
import urllib2
#from datetime import datetime
#from Cheetah.Template import Template
'''
Tools for cybercommons
'''
#templatepath= os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
#print templatepath

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
        self.celery_submission='http://test.cybercommons.org/queue/run/'
    @cherrypy.expose
    def index(self):
        return """
        <html><body>
            <h2>Upload a file</h2>
            <form action="upload" method="post" enctype="multipart/form-data">
            filename: <input type="file" name="fileToUpload" /><br />
            dest: <input type="text" name="dest" value="/static/teco_fileupload" /><br />
            task: <input type="text" name="task" value='{"name":"cybercomq.model.teco.task.add","param":"x=23&y=23"}' /><br />
            <input type="submit" />
            </form>
            <h2>Download a file</h2>
            <a href='download'>This one</a>
        </body></html>
        """
    #index.exposed = True
    @cherrypy.expose
    #@cherrypy.tools.protect(users=['me', 'myself', 'I'])
    def upload(self, fileToUpload,dest=None,task=None,filetype=None,teco_file=None, **kwargs):
        out = """<html>
        <body>
            myFile length: %s<br />
            myFile filename: %s<br />
            myFile mime-type: %s<br />
            user: %s <br />
            task: %s <br />
        </body>
        </html>"""
        message=""
        try:
            if cherrypy.request.login:
                user = cherrypy.request.login
            else:
                user = "guest" 
        except:
            user = "guest"
        # Set dest folder
        if not dest:
            dest = 'static/fileUpload/'
        datafile= fileToUpload
        message={'status':True,'description':'','task_id':'None'}
        # myFile.file.read reads from that. 
        if datafile is not None and datafile.filename:
            # strip leading path from file name to avoid directory traversal attacks
            fn = os.path.basename(datafile.filename)
            f = open(dest + fn, 'wb', 10240)

            size = 0
            while True:
                data = fileToUpload.file.read(10240)
                if not data:
                    break
                size += len(data)
                f.write(data)
            message['description']='Uploaded file: ' + dest + fn
            if task: 
                task=json.loads(task)
                if task['param']=="":
                    task['param']= 'user_id=' + user + '&filename=' + datafile.filename + '&file_type=' + filetype
                else:
                    task['param']= 'user_id=' + user + '&filename=' + datafile.filename + '&file_type=' + filetype + '&' + task['param'] 
                url = self.celery_submission + task['name'] + '?' + task['param']
                response = urllib2.urlopen(url)
                result_id = json.loads(response.read())
                message['task_id']=result_id['task_id']
                message = json.dumps(message) #{'upload': message,'task_id':result_id['task_id']}, indent=4)
            return message #out % (size, fileToUpload.filename, fileToUpload.content_type,str(user),message)
        else:
            return json.dumps({'status':False,'description':'No file to upload'}, indent=4)
cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

