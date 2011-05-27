import site
import socket
 
def activate_virtpy():
    activate_this = '/scratch/www/wsgi_sites/plotapi/virtpy/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    site.addsitedir('/scratch/www/wsgi_sites/plotapi')

if socket.gethostname() == 'fire.rccc.ou.edu':
    activate_virtpy() 

import cherrypy
import amf.plot

class MyApp():
    @cherrypy.expose
    def index(self):
        return "Plotting"

cherrypy.tree.mount(amf.plot.Plotter(), '/plot/amf')
cherrypy.tree.mount(MyApp(), '/plot')
application = cherrypy.tree
#application = cherrypy.Application(amf.plot.Plotter(), '/plot')


if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()

