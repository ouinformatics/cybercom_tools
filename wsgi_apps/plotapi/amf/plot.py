import cherrypy
import plotter

class Plotter():
    @cherrypy.expose
    def variable(self, loc=None, var=None, agg=None, fname=None):
        #location = 'US-RO1'
        #variable = 'NEE_or_fANN'
        #aggregation = 'monthly'
        cherrypy.response.headers['Content-Type']= 'image/png'
        return plotter.afplot( loc, var, agg) 

cherrypy.tree.mount(Plotter())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()
