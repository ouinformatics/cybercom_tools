import os
if os.uname()[1] == 'test.cybercommons.org':
    basedir = '/var/www/apps/'
elif os.uname()[1] == 'fire.rccc.ou.edu':
    basedir = '/scratch/www/wsgi_sites/'
elif os.uname()[1] == 'production.cybercommons.org':
    basedir = '/var/www/apps/'

activate_this = basedir + 'browse/virtpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import site
site.addsitedir(basedir + 'browse')


import cherrypy
from cherrypy import wsgiserver
from  browse import DataBrowse


application = cherrypy.Application(DataBrowse(), script_name=None, config = None )

if __name__ == '__main__':
    wsgi_apps = [('/browse', application)]
    server = wsgiserver.CherryPyWSGIServer(('localhost', 8080), wsgi_apps, server_name='localhost')
    try:
        server.start()
    except KeyboardInterrupt():
        server.stop()
