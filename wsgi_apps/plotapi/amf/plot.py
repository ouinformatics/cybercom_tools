import cherrypy
import plotter
from cybercom.data.dataset.ameriflux import ameriflux
from Cheetah.Template import Template

class Plotter():
    def show_locations(self):
        nameSpace = dict(locs=ameriflux.locations())
        templateDef = """<html><body>
            <table>
            #for $loc in $locs
            <tr><td><a href='$loc'>$loc</a></tr></td>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    
    def show_aggregations(self, loc):
        nameSpace = dict(aggs=ameriflux.aggregations(), loc=loc)
        templateDef = """<html><body>
            <table>
            #for $agg in $aggs
            <tr><td><a href='$loc/$agg'>$agg</a></tr></td>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    
    def show_variables(self, loc, agg):
        nameSpace = dict(vars=ameriflux.variables(), loc=loc, agg=agg)
        templateDef = """<html><body>
            <table>
            #for $var in $vars
            <tr><td><a href='$agg/$var'>$var</a></tr></td>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()

    @cherrypy.expose
    def variable(self, loc=None, agg=None, var=None, 
                    sdate=None, edate=None, fname=None):

        if loc is None:
            return self.show_locations()

        if agg is None:
            return self.show_aggregations(loc)
        
        if var is None:
            return self.show_variables(loc,agg)

        cherrypy.response.headers['Content-Type']= 'image/png'
        return plotter.afplot( loc, var, agg, sdate, edate) 
    @cherrypy.expose
    def index(self):
        return "Working!"

if __name__ == '__main__':
    cherrypy.tree.mount(Plotter())
    application = cherrypy.tree
    cherrypy.engine.start()
    cherrypy.engine.block()
