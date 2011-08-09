#!/bin/python2.6
from osgeo import gdal
import numpy
import os

OUTPATH='/static/data/ncep/reanalysis/aggregation'

def unpack_band( band, add_offset, scale_factor):
    '''Unpack band by applying offset and scaling factors
    
        Method per: http://www.esrl.noaa.gov/psd/data/gridded/faq.html#2
    '''
    return band * scale_factor + add_offset

def count_bands(rast):
    ''' Count the number of raster bands in a GDAL raster object'''
    band = 1 # have to start at 1 as band 0 does not exist
    while rast.GetRasterBand(band): 
        band += 1
    return band - 1 # back off the extra 1 count

def aggregate_ncep(filename,aggregation,method='sum'):
    ''' Computes band aggregations across time for NCEP reanalysis '''
    rast = gdal.Open(filename)

    # extract offset and scaling factor to unpack data
    flist = os.path.basename(filename).split('.') # get filename to grab variable name
    add_offset = float(rast.GetMetadata()[flist[0]+'#add_offset'])
    scale_factor = float(rast.GetMetadata()[flist[0]+'#scale_factor'])
    
    # Leap years have 1464 bands, current year has less than total so interrogate.
    bands = count_bands(rast)

    # aggregation 4 = Daily, 28 = Weekly, 32 = 8-day, 120 = monthly etc.
    if aggregation == 'daily':
        days = 1
        agg = 4
    elif aggregation == 'week':
        days = 7
        agg = 28
    elif aggregation == '8day':
        days = 8
        agg = 32
    elif aggregation == 'month':
        days = 30
        agg = 120
    elif aggregation == 'annual':
        days = 360
        agg = bands
    steps = bands - (bands % agg)

    slices = numpy.arange(steps).reshape(steps/agg,agg) + 1 # Slice the timesteps to daily vectors
    for aggnum, cslice in enumerate(slices):
        bands = numpy.zeros((rast.RasterYSize,rast.RasterXSize))
        try:
            for ind, band in enumerate(cslice):
                bands += unpack_band(rast.GetRasterBand(int(band)).ReadAsArray(),add_offset,scale_factor)
                #import pdb; pdb.set_trace()
                if ind + 1 == agg: # Write out the aggregation at the last step.
                    if method == 'avg':
                        bands = bands / len(cslice)
                    driver = gdal.GetDriverByName('GTiff')
                    fout = os.path.join(OUTPATH, aggregation, os.path.basename(filename.replace('.nc','')) + '.' + aggregation +'.'+ str(aggnum + 1) + '.tif')
                    dst_ds = driver.Create(fout, rast.RasterXSize , rast.RasterYSize, 1, gdal.GDT_Float32, ['COMPRESS=LZW'])
                    # Should add some appropriate metadata to files here

                    dst_ds.SetGeoTransform( rast.GetGeoTransform() )
                    dst_ds.GetRasterBand(1).WriteArray(bands)
        except:
            print "Move along, nothing to see here"



