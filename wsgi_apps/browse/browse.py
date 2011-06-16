import cherrypy
import portal
#from cybercom.data.dataset.ameriflux import ameriflux
from cybercom.data.catalog import datalayer
from Cheetah.Template import Template


class DataBrowse():
    def show_commons(self):
        nameSpace = dict(locs=portal.datacommons())
        templateDef = """<html><body>
            <title>Cybercom Data Repository</title>
            <div style="font-size:20px;">Cybercom Data Repository</div></br>
            <table>
            #for $loc in $locs
            <tr><td><a href="./$loc['commons_id']/">$loc['commons_code']</a></tr></td>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    
    def show_location(self, commons):
        nameSpace = dict(locs=portal.locations(commons), commons=commons)
        templateDef = """<html><body>
            <title>Cybercom Data Repository</title>
            <div style="font-size:20px;">Cybercom Locations</div></br>
            #if len($locs) < 1
            <div>NO Data Available</div>
            #end if
            <table cellpadding="4">
            #for $loc in $locs
            <tr><td>  State: $loc['loc_state'] ( $loc['lat'], $loc['lon'] ) </td><td><a href='$loc['loc_id']'/>$loc['loc_name']</a></td><td></tr>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    def show_product(self, commons):
        nameSpace = dict(prods=portal.products(commons), commons=commons)
        templateDef = """<html><body>
            <title>Cybercom Data Repository</title>
            <div style="font-size:20px;">Cybercom Products</div></br>
            #if len($prods) < 1
            <div>NO Data Available</div>
            #end if            
            <table>
            #for $prod in $prods
            <tr><td><a href='./$prod['product']'/>$prod['product']</a></tr></td>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    def show_year(self,commons, loc):
        if commons == str(401):
            nameSpace = dict(yrs=portal.prodyear(commons,loc),commons=commons, loc=loc)
        else:
            nameSpace = dict(yrs=portal.locyear(commons,loc),commons=commons, loc=loc)
        templateDef = """<html><body>
            <title>Cybercom Data Repository</title>
            <div style="font-size:20px;">Cybercom Years Cataloged</div></br>
            #if len($yrs) < 1
            <div>NO Data Available</div>
            #end if
            <table>
            #for $yr in $yrs
            <tr><td><a href='$loc/$yr['observed_year']'> $yr['observed_year']</a></tr></td>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    def show_catalog(self,commons,loc,year):
        nameSpace = dict(cats=portal.catalog(commons,loc,year), commons=commons,loc=loc,year=year)
        templateDef = """<html><body>
            <title>Cybercom Data Repository</title>
            <div style="font-size:20px;">Cybercom Catalog Items</div></br>
            #if len($cats) < 1
            <div>NO Data Available</div>
            #end if
            <table>
            #for $cat in $cats
            <tr><td><a href='./$year/$cat['cat_id']'/>$cat['cat_name']</a></td></tr>
            #end for
            </table>
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    def show_metadata(self,cat_id):
        nameSpace = dict(metas=portal.metadata(cat_id), cat_id=cat_id)
        templateDef = """<html><body>
            #if len($metas) < 1
            <div>NO Events Cataloged</div>
            #else
            Catalog ID: $cat_id    </br> 
            Catalog Name: $metas[0]['cat_name']</br>
            Location ID: $metas[0]['loc_id'] ($metas[0]['lat'],$metas[0]['lon'])</br>
            Location Name: $metas[0]['loc_name']</br>
            </br>
            <table border="1" cellpadding="5">
            <tr><th>Event method</th><th>Variable</th><th>Result</th></tr>
            #for $meta in $metas
            #if $meta.var_id != 'URL'
            <tr><td> $meta.event_method</td><td> $meta.var_id </td><td>$meta.result_text</td></tr>
            #else
            <tr><td> $meta.event_method</td><td> $meta.var_id </td><td><a href="$meta.result_text">$meta.result_text</a></td></tr>
            #end if
            #end for
            </table>
            #end if
        </body></html>
        """
        t = Template(templateDef, searchList=[nameSpace])
        return t.respond()
    @cherrypy.expose
    def catalog(self, commons=None, loc=None, year=None, 
                    cat_id=None, edate=None, fname=None):

        if commons is None:
            return self.show_commons()

        if loc is None:
            if commons == str(401):
                return self.show_product(commons)
            else:
                return self.show_location(commons)
        
        if year is None:
            return self.show_year(commons,loc)
        if cat_id is None:
            return self.show_catalog(commons,loc,year)
        #cherrypy.response.headers['Content-Type']= 'image/png'
        return self.show_metadata(cat_id)#"var worked"#plotter.afplot( loc, var, agg, sdate, edate) 
    

if __name__ == '__main__':
    cherrypy.tree.mount(DataBrowse())
    application = cherrypy.tree
    cherrypy.engine.start()
    cherrypy.engine.block()
