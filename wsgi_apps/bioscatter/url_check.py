#!/usr/bin/env python
import httplib
from urlparse import urlparse
from UNQC_CREF import UNQC_CREF
import cherrypy
import simplejson as json

def urlExists(url):
    o = urlparse(url)
    site = o.netloc
    path = o.path
    conn = httplib.HTTPConnection(site)
    conn.request('HEAD', path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200

def checkTimestep(timestep, product, template=None):
    """ 
    Check if all bioscatter tiles exists on the LDM server
    """
    if not template:
        template = 'http://ldm.cybercommons.org/tile%s/%s/%s.%s.gtiff'
    return all([ urlExists( template % (tile,product,product.upper(),timestep) ) for tile in range(1,9) ])

class Root(object):
    @cherrypy.expose
    @cherrypy.tools.response_headers(headers=[('Content-Type', 'text/html')])
    def index(self):
        return "<html><a href='checkTimestep/20100101.000000/unqc_cref'>checkTimestep</a><br><a href='getVrt/20100101.000000/unqc_cref'>getVrt</a></html>"
    @cherrypy.expose
    @cherrypy.tools.response_headers(headers=[('Content-Type', 'application/json')])
    def checkTimestep(self,timestep,product):
        retval = dict(timestep=timestep,exists=checkTimestep(timestep,product))
        return json.dumps(retval, indent=2 )
    @cherrypy.expose
    @cherrypy.tools.response_headers(headers=[('Content-Type', 'text/xml')])
    def getVrt(self,timestep,product):
        if checkTimestep(timestep,product):
            fname = 'UNQC_CREF.%s.gtiff' % timestep
            return str(UNQC_CREF(searchList={'FNAME': fname}))
        else:
            return "<ERROR>Data missing</ERROR>"

application = cherrypy.Application(Root(), script_name=None, config=None)

if __name__ == '__main__':
    cherrypy.quickstart(Root()) 

