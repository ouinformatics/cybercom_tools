import cherrypy

activate_this = '/scratch/www/wsgi_sites/plotapi/virtpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import site
site.addsitedir('/scratch/www/wsgi_sites/plotapi')



application = cherrypy.Application(Root(), script_name=None, config = None )
# , config={ '/': {'tools.xmlrpc.on': True }} )


