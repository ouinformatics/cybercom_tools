import os
if os.uname()[1] == 'test.cybercommons.org':
    basedir = '/var/www/apps/'
elif os.uname()[1] == 'fire.rccc.ou.edu':
    basedir = '/scratch/www/wsgi_sites/'
elif os.uname()[1] == 'production.cybercommons.org':
    basedir = '/var/www/apps/'

activate_this = basedir + 'mongo/virtpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import site
site.addsitedir(basedir + 'mongo')
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


