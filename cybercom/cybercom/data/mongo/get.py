from pymongo import Connection
from datetime import datetime
from json_handler import handler
import ast
import iso8601
import json
def select( db=None, col=None, query=None, callback=None, showids=None, date=None):
    con = Connection()
    # if db is set create db object, else show db names
    if db:
        db = con[db]
    else:
        return json.dumps(con.database_names())
    # If collection is set return records, else show collection names
    if col:
        col = db[col]
    else:
        return json.dumps(db.collection_names())

    dump_out = []

    if date:
        try:
            column, start, stop = date.split(',')
        except:
            pass
        start = iso8601.parse_date(start)
        stop = iso8601.parse_date(stop)
        date_spec = { column : { "$gte": start, "$lte": stop } }
        return date_spec

    # If query set, run query options through pymongo find, else show all records
    if query:
        query = ast.literal_eval(query)
        if date:
            query.update( { 'spec' : date_spec })
        cur = col.find(**query)
    else:
        cur = col.find()

    for item in cur:
        if showids:
            dump_out.append(item)
        else:
            item.pop('_id')
            dump_out.append(item)
    serialized = json.dumps(dump_out, default = handler, sort_keys=True, indent=4)
    if callback is not None:
        return str(callback) + '(' + serialized + ')'
    else:
        return serialized
