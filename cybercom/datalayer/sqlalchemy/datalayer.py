import simplejson, json, datetime, StringIO, csv, sys
from sqlalchemy import Table
from sqlalchemy.sql import select
import db_create as dl
conn = dl.engine.connect()

def search(tablename,column=None,where=None,as_method='dict'):
    #****setup up mapped table

    tab = Table(tablename,dl.Base.metadata,autoload=True)

    #****Add Specific columns to query    
    cols=[]
    if column==None:
        saObj = select([tab],where)
    else:
        for col in tab.c:
            try:
                if column.index(col.name)>=0:
                    cols.append(col)
            except:
                pass
        saObj = select(cols,where)

    res = saObj

    if as_method == 'dict':
        return as_dict( res )
    if as_method == 'csv':
        return as_csv( res )    
    if as_method == 'json':
        return as_json(res)
    if as_method == 'yaml':
        return as_yaml(res)
    else:
        return conn.execute(res) 

#**************functions***********

def get_cols(res):
    """ Get the header of column names """ 
    cols = []
    for col in res.c:
        cols.append(col.name)
    return cols

def zip_rows(res):
    """ Zip the header and rows into a python dictionary """
    output = []
    header = get_cols( res )
    res1=conn.execute(res)
    for row in res1:
        output.append(dict(zip(header, row)))
    return output
    
def as_dict(res):
    """ Return res as a python dictionary """
    return zip_rows( res ) 

def as_csv(res):
    """ Return res as a csv complete with headers """
    outfile = StringIO.StringIO()
    cw = csv.writer(outfile, quotechar = '"', quoting=csv.QUOTE_MINIMAL,skipinitialspace=True)
    cw.writerow( get_cols( res ) )
    cw.writerows( conn.execute(res).fetchall())
    return outfile.getvalue()

def as_json(res):
    """ Return res as json """
    try:
        import json
    except:
        print >> sys.stderr, "Don't have json"
    return json.dumps( zip_rows( res ), indent=2, default=handler ) 

def as_yaml(res):
    """ return res as yaml """
    try:
        import yaml
    except:
        print >> sys.stderr, "You don't seem to have PyYAML installed"
    return yaml.dump( zip_rows( res ))

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj))
def getprimarykeys(tablename=None):
    keys = []
    dict = {}
    for t in dl.Base.metadata.sorted_tables:
        if tablename==None:
            for key in t.primary_key:
                keys.append(key.name)
            dict[t.name]=keys
            keys=[]
        else:
            if t.name == tablename:
                for key in t.primary_key:
                    keys.append(key.name)
                dict[t.name]=keys 
    return simplejson.dumps(dict, sort_keys=True, indent=2)
def listcolumns(tablename):
    keys = []
    for t in dl.Base.metadata.sorted_tables:
        if t.name == tablename:
            for key in t.c:
                keys.append(key.name)
    return keys
def getcolumns(tablename=None):
    keys = []
    dict = {}
    for t in dl.Base.metadata.sorted_tables:
        if tablename==None:
            for key in t.c:
                keys.append(key.name)
            dict[t.name]=keys
            keys=[]
        else:
            if t.name == tablename:
                for key in t.c:
                    keys.append(key.name)
                dict[t.name]=keys
    return simplejson.dumps(dict, sort_keys=True, indent=2)
def gettables():
    keys = []
    dict = {}
    for t in dl.Base.metadata.sorted_tables:
        #print t.name
        keys.append(t.name)
    dict['metadata tables']=sorted(set(keys))
    return simplejson.dumps(dict, indent=2)

