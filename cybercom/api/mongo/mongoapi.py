import cherrypy
import json 
import get 

def mimetype(type):
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.response.headers['Content-Type'] = type
            return func(*args, **kwargs)
        return wrapper
    return decorate

class Root(object):
    @cherrypy.expose
    @mimetype('application/json')
    def db_find( self, db=None, col=None, query=None, callback=None, showids=None, date=None):
        """ 
        Wrapper for underlying pymongo access
        """
        get.select(db, col, query, callback, showids, date)
