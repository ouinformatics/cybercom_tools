#!/usr/bin/env python
"""
Created: Nov 15, 2010
Author: Jonah Duckles <jduckles@ou.edu>
 
 Tool for databse table extraction based on "RUN_ID" 
 
 Currently will export to following formats:
  - python dictionary
  - json 
  - csv
  - yaml
"""

import sys
import csv
import StringIO
import cx_Oracle as db

try:
    con = db.connect('eco/b00mer@oubcf1')
except:
    print >> sys.stderr, "Can't seem to connect to Database"

cur = con.cursor()


def get_cols(res):
    """ Get the header of column names """ 
    cols = []
    for col in res.description:
        cols.append(col[0])
    return cols

def zip_rows(res):
    """ Zip the header and rows into a python dictionary """
    output = []
    header = get_cols( res )
    for row in res.fetchall():
        output.append(dict(zip(header, row)))
    return output
    
def as_dict(res):
    """ Return res as a python dictionary """
    return zip_rows( res ) 

def as_csv(res):
    """ Return res as a csv complete with headers """
    outfile = StringIO.StringIO()
    cw = csv.writer(outfile)
    cw.writerow( get_cols( res ) )
    cw.writerows( res.fetchall() )
    return outfile.getvalue()

def as_json(res):
    """ Return res as json """
    try:
        import json
    except:
        print >> sys.stderr, "Don't have json"
    return json.dumps( zip_rows( res ) ) 

def as_yaml(res):
    """ return res as yaml """
    try:
        import yaml
    except:
        print >> sys.sderr, "You don't seem to have PyYAML installed"
    return yaml.dump( zip_rows( res ))
    
def get_rows( table, where, as_method='dict' ):
    """ Build query based on options dictionary 
            Example: 
                query_options = dict( columns="to_char(time_index, 'YYYY/MM/DD HH:MM:SS') as time_index,pyear,dayyear,hours,tair,tsoil,vdef,rh,precp,rad_h", table="TECO_INP_RUN_ID" )
                get_rows(query_options, 500, 'json')
         

    """
    query = 'select * from %s where %s' % (query_options['table'], where)
    res = cur.execute(query, dict(run_id=run_id))
    header = get_cols( res )
    if as_method == 'dict':
        return as_dict( res )
    if as_method == 'csv':
        return as_csv( res )    
    if as_method == 'json':
        return as_json(res)
    if as_method == 'yaml':
        return as_yaml(res)
    else:
        return res.fetchall()

def main(argv = None):
    if argv is None:
        argv = sys.argv
    options = {}
    options.update(table=argv[1],where=argv[2],as_method=argv[3])
    return get_rows( options['table'], options['where'], options['as_method'])

if __name__ == "__main__":
    sys.exit(main())
    
    


