import cherrypy
import json 

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
    def environment(self):
        return json.dumps({'login': cherrypy.request.login, 'response': cherrypy.response.headers, 'request': cherrypy.request.headers }, indent=2)

cherrypy.tree.mount(Root())
application = cherrypy.tree

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()
