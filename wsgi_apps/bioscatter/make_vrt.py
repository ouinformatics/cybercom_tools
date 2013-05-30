import httplib
from urlparse import urlparse
import UNQC_CREF

def url_exists(url):
    o = urlparse(url)
    site = o.netloc
    path = o.path
    conn = httplib.HTTPConnection(site)
    conn.request('HEAD', path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200

def check_timestep(timestep, product='unqc_cref' ,template=None):
    """ 
    Check if all bioscatter tiles exists on the LDM server
    """
    products = { 'unqc_cref': ('unqc_cref', 'UNQC_CREF'),
      'compref_mosaic': ('compref_mosaic', 'CREF')
    }
    if not template:
        template = 'http://ldm.cybercommons.org/tile%s/%s/%s.%s.gtiff'
    fillin = products[product] + (timestep,)
    return all([ url_exists( template % ((tile,) + (fillin)) ) for tile in range(1,9) ])






    

