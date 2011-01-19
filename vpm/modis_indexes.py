#!/usr/bin/env python
import urllib
import csv
import sqlite3
from numpy import *

def get_eomf_ts( modis_product, years, lat, lon, scale=False ):
    """ Get MODIS data product from EOMF webservice"""
    modis_product = modis_product.lower()
    url_string = 'http://eomf.ou.edu/visualization/ascii_%s_%s_%s_%s.txt' % (modis_product, years, lat, lon)
    ts = csv.reader(urllib.urlopen(url_string), delimiter='\t')
    metadata = {}
    metadata.update(latitude = ts.next()[1])
    metadata.update(longitude = ts.next()[1])
    metadata.update(product = ts.next()[1])
    metadata.update(tile = ts.next()[1])
    metadata.update(cell = ts.next()[1])
    metadata.update(sfactor = int(ts.next()[0].replace(',','').split(':')[1]))
    ts.next() # Dump blank row
    header = ts.next()
    output = []
    for line in ts:
        output.append(dict(zip(header, line)))
    return output, metadata 

def get_ameriflux_weekly( siteid, year):
    siteid_ = siteid.replace('-','')
    url_string = 'ftp://cdiac.ornl.gov/pub/ameriflux/data/Level4/Sites_ByID/%s/%s%s_L4_w.txt' % (siteid, siteid_, year)  
    try:
        ts_file = urllib.urlopen(url_string)
    except:
        print "Had a problem downloading file...maybe it doesn't exist."
    if ts_file: 
        ts = csv.reader(ts_file)
        header = ts.next()
        output = []
        for line in ts:
            output.append(dict(zip(header, line)))
        return output


def store_sqlite( fname, tname, data ):
    """ Store a simple python dictionary to a sqlite table """
    con = sqlite3.connect(fname)
    header = str(data[0].keys()).replace('[','').replace(']','')
    texist = con.execute("select * from sqlite_master where tbl_name = '%s'" % (tname) )
    con.execute('create table %s (%s)' % (tname, header))
    for row in data:
        if len(row.values()) > 0:
            val = str(row.values()).replace('[','').replace(']','')
            qstring = "insert into %s values (%s)" % (tname, val)
            con.execute(qstring)
    con.commit()

def get_column( dbname, tname, column):
    con = sqlite3.connect(dbname)
    cur = con.execute('select sur_refl_day_of_year, %s from %s' % (column, tname) ) 
    out = []
    for line in cur.fetchall():
        out.append([line])
    descriptor = { 'names': ('sur_refl_day_of_year',column), 'formats': ('int32','int32') }
    return array(out, dtype=descriptor)

def compute_evi( nir_val, red_val, blue_val, G=2.5, L=1, C1=6, C2=7.5 ):
    """ Compute the EVI based on NIR, RED and BLUE Bands """
    # Coefficients are set to standards adopted for MODIS EVI:
    # G = 2.5   gain factor
    # L = 1     Canopy bg adjustment
    # C1 = 6    Coefficient of aerosol resistance 1
    # C2 = 7.5  Coefficient of aerosol resistance 2
    return G * ( nir_val - red_val) / ( nir_val + (C1 * red_val) - (C2 * blue_val) + L)

def compute_ndvi( nir_val, red_val ):
    """ Compute the NDVI based on NIR and RED bands """ 
    return (nir_val - red_val) / (nir_val + red_val)

def compute_lswi( nir_val, swir_val ):
    """ Compute the Land Surface Water Index """
    return ( nir_val - swir_val) / (nir_val + swir_val)

def compute_tscalar( T, T_min, T_max, T_opt ):
    """ Compute T_scalar """
    return (( T - T_min ) * ( T - T_max )) / ( ( ( T - T_min ) * ( T - T_max ) ) - ( ( T - T_opt ) * ( T - T_opt ) ) )

def compute_wscalar( LSWI, LSWI_max ):
    """ Estimate water scalar from LSWI.  LSWI_max is the max across the growing season """
    return (1 + LWSI) / (1 + LSWI_max)
   
def scale( val, factor):
    """ Apply scaling factor """ 
    val = cast['float'](val)
    return (val / factor)


