#!/usr/bin/python
import scipy.io
from osgeo import gdal as gd
from datetime import datetime

def geo2pixel(band,geoloc):
    g0, g1, g2, g3, g4, g5 = band.GetGeoTransform()
    xgeo,  ygeo = geoloc
    if g2 == 0:
        xPixel = (xgeo - g0) / float(g1)
        yPixel = (ygeo - g3 - xPixel*g4) / float(g5)
    else:
        xPixel = (ygeo*g2 - xgeo*g5 + g0*g5 + g2*g3) / float(g2*g4 - g1*g5)
        yPixel = (xgeo - g0 - xPixel*g1)/float(g2)
    return (int(round(xPixel)),int(round(yPixel)))

def window2numpy(band,pixelx,pixely,pixelwidth,pixelheight):
    return band.ReadAsArray(pixelx,pixely,pixelwidth,pixelheight)

def centeredwindow(band,geox,geoy,pixelwidth,pixelheight):
    pixelx,pixely = geo2pixel(band,(geox,geoy))
    cpixelx = pixelx - pixelwidth / 2
    cpixely = pixely - pixelheight / 2
    return window2numpy(band,cpixelx,cpixely,pixelwidth,pixelheight)

def getwindow(timestamp,lon,lat,width=100,height=100,astype='numpy',product='unqc_cref'):
    tstring = timestamp.strftime('%Y%m%d.%H%M%S')
    url = '/vsicurl/http://test.cybercommons.org/bioscatter/getVrt/%s/%s' % (tstring,product)
    band = centeredwindow(gd.Open(url), lon, lat, width, height )
    if astype == 'numpy':
        return band
    if astype == 'mat':
        fname = '%s_%s_%s_%s.mat' % (product,tstring,lon,lat)
        return scipy.io.savemat(fname, {product:band}, oned_as='column')

if __name__ == '__main__':
    import sys
    timestep = datetime.strptime(sys.argv[1],'%Y%m%d.%H%M%S')
    lon = float(sys.argv[2])
    lat = float(sys.argv[3])
    width = int(sys.argv[4])
    height = int(sys.argv[5])
    astype = sys.argv[6]
    product = sys.argv[7]
    getwindow(timestep,lon,lat,width,height,astype,product)

 

