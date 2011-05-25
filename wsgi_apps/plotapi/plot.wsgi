
import socket
if socket.gethostname() == 'fire.rccc.ou.edu':
    activate_this = '/scratch/www/wsgi_sites/plotapi/virtpy/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    site.addsitedir('/scratch/www/wsgi_sites/plotapi')

import cherrypy
import amf.plot

class MyApp():
    @cherrypy.expose
    def index(self):
        return "Sometext"


cherrypy.tree.mount(amf.plot.Plotter(), '/amf')
cherrypy.tree.mount(MyApp())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()



