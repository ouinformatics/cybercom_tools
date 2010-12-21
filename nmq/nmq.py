import numpy
import subprocess
import sys 
from osgeo import gdal
from osgeo.gdalconst import *
import osgeo.osr as osr

filein = sys.argv[1]
fileout = sys.argv[2]
EXEC_PATH='/home/jduckles/cybercom/nmq/read_nmq'
FILE_PATH='/scratch/data/nws/nexrad/tile6/unqc_cref/'
format='GTiff'


# Run read_nmq to read custom binary file format
cline=[EXEC_PATH,filein,'0']
cmd=subprocess.Popen(cline,stdout=subprocess.PIPE)
oput=cmd.communicate()[0].strip().split('\n')

headers=oput[:24]
data=oput[25:]
#data.reverse()
for i in range(0,len(data)):
	data[i]=data[i].split('\t')

npdata=numpy.array(data)
npdata=numpy.cast['float'](npdata)
npdata=numpy.rot90(npdata)

driver = gdal.GetDriverByName( format )
dst_ds = driver.Create( fileout, 2001, 2001, 1, gdal.GDT_Float32)
dst_ds.SetGeoTransform( [ -110.005, 0.01, 0, 40.005, 0, -0.01 ] )
srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection( srs.ExportToWkt() )
dst_ds.GetRasterBand(1).WriteArray(npdata)
dst_ds=None

