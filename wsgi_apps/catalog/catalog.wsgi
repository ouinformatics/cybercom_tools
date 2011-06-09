activate_this = '/scratch/www/wsgi_sites/catalog/virtpy/bin/activate_this.py'
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


