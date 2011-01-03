#!/usr/bin/env python
import urllib
import csv

def get_eomf_ts( modis_product, years, lat, lon, scale=False ):
    """ Get MODIS data product from EOMF webservice"""
    modis_product = modis_product.lower()
    url_string = 'http://eomf.ou.edu/visualization/ascii_%s_%s_%s_%s.txt' % (modis_product, years, lat, lon)
    ts = csv.reader(urllib.urlopen(url_string), delimiter='\t')
    latitude = ts.next()
    longitude = ts.next()
    product = ts.next()
    tile = ts.next()
    cell = ts.next()
    comment = ts.next()
    ts.next() # Dump blank row
    header = ts.next()
    output = []
    for line in ts:
        output.append(dict(zip(header, line)))
    return output 

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
    return (val / factor)


