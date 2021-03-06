import os
if os.uname()[1] == 'fire.rccc.ou.edu':
    basedir = '/scratch/www/wsgi_sites/'
else:
    basedir = '/var/www/apps/'

activate_this = basedir + 'mongo/virtpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import site
try:
    site.addsitedir(basedir + 'mongo')
except:
    pass
import cherrypy
from cherrypy import wsgiserver
from cybercom.api.mongo.mongoapi import Root

    
application = cherrypy.Application(Root(), script_name=None, config = None )# , config={ '/': {'tools.xmlrpc.on': True }} )

if __name__ == '__main__':
    wsgi_apps = [('/mongo', application)]
    server = wsgiserver.CherryPyWSGIServer(('localhost', 8080), wsgi_apps, server_name='localhost')
    try:
        server.start()
    except KeyboardInterrupt():
        server.stop()


