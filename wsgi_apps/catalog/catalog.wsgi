import os
if os.uname()[1] == 'test.cybercommons.org':
    basedir = '/var/www/apps/'
elif os.uname()[1] == 'fire.rccc.ou.edu':
    basedir = '/scratch/www/wsgi_sites/'

activate_this = os.path.join(basedir,'catalog/virtpy/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

import site
site.addsitedir('/scratch/www/wsgi_sites/catalog')
import cherrypy
from cherrypy import wsgiserver
from cybercom.api.catalog.search import Root

    
application = cherrypy.Application(Root(), script_name=None, config = None )# , config={ '/': {'tools.xmlrpc.on': True, 'tools.gzip': True }} )

if __name__ == '__main__':
    wsgi_apps = [('/catalog', application)]
    server = wsgiserver.CherryPyWSGIServer(('localhost', 8080), wsgi_apps, server_name='localhost')
    try:
        server.start()
    except KeyboardInterrupt():
        server.stop()


