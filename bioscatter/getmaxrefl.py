#!/home/jduckles/bin/python
import sys
from osgeo import gdal
from datetime import timedelta, datetime
import numpy
import os
import pymongo

gdal.UseExceptions()

product = 'unqc_cref'
path = '/scratch/data/nws/ldm/tiles/mosaic/unqc_cref/'
timefmt = '%Y%m%d.%H%M%S'
filename = 'UNQC_CREF.%s.vrt' # %s filled in raster_file function

def mkwin(x, y, radius):
    ''' Make a window around a given point location.  Radius is in map units'''
    ulx = x - radius
    uly = y + radius
    llx = x + radius
    lly = y - radius
    return (ulx, uly, llx, lly)

def date_range(start_datetime, end_datetime):
    ''' Generator for datetime_ranges at 5 minute intervals '''
    d = start_datetime
    delta = timedelta(minutes=5)
    while d <= end_datetime:
        yield d
        d += delta

def projwin2src(projwin,geotrans):
    ''' compute the source window (srcwin) from Projection Window projwin using same method as gdal_translate CPP source '''
    srcwin = []
    srcwin.append(((projwin[0] - geotrans[0]) / geotrans[1] + 0.001))
    srcwin.append(((projwin[1] - geotrans[3]) / geotrans[5] + 0.001))
    srcwin.append(((projwin[2] - projwin[0])  / geotrans[1] + 0.5))
    srcwin.append(((projwin[3] - projwin[1]) / geotrans[5] + 0.5))
    for w in range(0,len(srcwin)):
        srcwin[w] = int(srcwin[w])
    return srcwin

def raster_file(timestamp):
    ''' Take a datetime timestamp and convert it to full path based on global variables '''
    timestring = datetime.strftime(timestamp, timefmt)
    fstring = filename % timestring
    if os.path.exists( path + fstring ):
        return path + fstring

def readRasterMax(window, timestart, timestop, store=False):
    ''' Compute maximum value within window '''
    ids = []
    for time in date_range(timestart,timestop):
        filename = raster_file(time)
        if filename:
            rast = gdal.Open(filename)
            geotrans = rast.GetGeoTransform()
            projwin = mkwin(float(window['x']), float(window['y']), float(window['radius']))
            srcwin = projwin2src(projwin, geotrans)
            maxval = float(rast.ReadAsArray(srcwin[0], srcwin[1], srcwin[2], srcwin[3] ).max())
            output =  {"product": product, "projwin": list(projwin), "timestamp": time, "maxval": maxval, "location": window}
            if store:
                con = pymongo.Connection()
                db = con.bioscatter
                col = db.unqc_cref
                ids.append(col.insert(output))
            else:
                ids.append(output)
    return ids

if __name__ == '__main__':
    from sys import argv
    from datetime import datetime
    import time
    window = {}
    window['x'], window['y'], window['radius'] = argv[1].split(',')
    timestart = datetime(*time.strptime(argv[2], timefmt)[:6])
    timestop = datetime(*time.strptime(argv[3], timefmt)[:6])
    store = False
    if len(argv) > 4:
        store = argv[4]
    print readRasterMax(window, timestart, timestop, store)


