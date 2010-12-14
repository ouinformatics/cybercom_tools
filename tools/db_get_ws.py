#!/usr/bin/env python2.7


import cProfile
import cherrypy
import db_get as dg

cherrypy.config.update({'server.socket_host': '129.15.40.57',
                        'server.socket_port': 8080,
                       })


class Root(object):
    @cherrypy.expose
    def db_get(self, columns, table, runid, method):
        cherrypy.response.headers['Content-Type']= 'text/plain'
        query_options = dict(columns = columns, table = table)
        return dg.get_rows(query_options, runid, method)
        
root = Root()

cProfile.run(cherrypy.quickstart(Root()), '/tmp/profile')
