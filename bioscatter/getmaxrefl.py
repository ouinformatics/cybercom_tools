#!/usr/bin/python
from sys import argv
from osgeo import gdal
import numpy

gdal.UseExceptions()

rast = gdal.Open(sys.argv[1])
geotrans = rast.GetGeoTransform()
projwin = sys.argv[2].split(',')

def projwin2src(projwin,geotrans):
    srcwin = []
    srcwin.append(((projwin[0] - geotrans[0]) / geotrans[1] + 0.001))
    srcwin.append(((projwin[1] - geotrans[3]) / geotrans[5] + 0.001))
    srcwin.append(((projwin[2] - projwin[0])  / geotrans[1] + 0.5))
    srcwin.append(((projwin[3] - projwin[1]) / geotrans[5] + 0.5))
    for w in range(0,len(srcwin)):
        srcwin[w] = int(srcwin[w])
    return srcwin

srcwin = projwin2src(projwin, geotrans)

print '%s %s' % (sys.argv[1], rast.ReadAsArray(srcwin[0], srcwin[1], srcwin[2], srcwin[3] ).max())



    

