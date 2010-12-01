#!/usr/bin/env python2.7


import cProfile
import cherrypy
import db_get as dg

class Root(object):
    @cherrypy.expose
    def db_get(self, columns, table, runid, method):
        query_options = dict(columns = columns, table = table)
        return dg.get_rows(query_options, runid, method)

root = Root()

cProfile.run(cherrypy.quickstart(Root()), '/tmp/profile')
