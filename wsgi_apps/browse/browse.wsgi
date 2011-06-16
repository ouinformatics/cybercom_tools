activate_this = '/scratch/www/wsgi_sites/browse/virtpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import site
site.addsitedir('/scratch/www/wsgi_sites/browse')
import cherrypy
from cherrypy import wsgiserver
from  browse import DataBrowse


application = cherrypy.Application(DataBrowse(), script_name=None, config = None )

if __name__ == '__main__':
    wsgi_apps = [('/databrowse', application)]
    server = wsgiserver.CherryPyWSGIServer(('localhost', 8080), wsgi_apps, server_name='localhost')
    try:
        server.start()
    except KeyboardInterrupt():
        server.stop()
