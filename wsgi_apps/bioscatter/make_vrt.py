import httplib
from urlparse import urlparse
import UNQC_CREF
import cherrypy

def url_exists(url):
    o = urlparse(url)
    site = o.netloc
    path = o.path
    conn = httplib.HTTPConnection(site)
    conn.request('HEAD', path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200

def check_timestep(timestep, template=None):
    """ 
    Check if all bioscatter tiles exists on the LDM server
    """
    if not template:
        template = 'http://ldm.cybercommons.org/tile%s/unqc_cref/UNQC_CREF.%s.gtiff'
    return all([ url_exists( template % (tile,timestep) ) for tile in range(1,9) ])






    

