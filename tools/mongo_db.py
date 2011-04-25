from pymongo import Connection
import pymongo.json_util as json_util
import json
import cherrypy

con = Connection()

class Root(object):
    @cherrypy.expose
    def find( db_name, col_name, query=None):
        db = con[db_name]
        col = db[col_name]
        return query
        dump_out = []
        cur = col.find(**query)
        for item in cur:
            dump_out.append(item)
        return json.dumps( dump_out, default=json_util.default, indent=4)

application = cherrypy.Application(Root(), script_name=None, config=None)

