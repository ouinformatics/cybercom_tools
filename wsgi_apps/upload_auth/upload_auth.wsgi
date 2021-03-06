import os
if os.uname()[1] == 'test.cybercommons.org':
    basedir = '/var/www/apps/'
elif os.uname()[1] == 'fire.rccc.ou.edu':
    basedir = '/scratch/www/wsgi_sites/'
elif os.uname()[1] == 'production.cybercommons.org':
    basedir = '/var/www/apps/'

activate_this = basedir + 'upload_auth/virtpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import site
site.addsitedir(basedir + 'upload_auth')
import cherrypy
from cherrypy import wsgiserver
from views import Root

    
application = cherrypy.Application(Root(), script_name=None, config = None )# , config={ '/': {'tools.xmlrpc.on': True }} )

if __name__ == '__main__':
    wsgi_apps = [('/upload_auth', application)]
    server = wsgiserver.CherryPyWSGIServer(('localhost', 8080), wsgi_apps, server_name='localhost')
    try:
        server.start()
    except KeyboardInterrupt():
        server.stop()


