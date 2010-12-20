import numpy
import subprocess 
from osgeo import gdal
from osgeo.gdalconst import *
import osgeo.osr as osr

EXEC_PATH='/home/bcremeans/nmq/NMQ_CartBinaryReader/read_nmq'
FILE_PATH='/scratch/data/nws/nexrad/tile6/unqc_cref/'
OUT_FILE='/home/bcremeans/nmq/NMQ_CartBinaryReader/out.gtiff'
format='GTiff'

cline=[EXEC_PATH,FILE_PATH+'UNQC_CREF.20090728.112000','0']
cmd=subprocess.Popen(cline,stdout=subprocess.PIPE)
oput=cmd.communicate()[0].strip().split('\n')
headers=oput[:24]
data=oput[25:]
data.reverse()
for i in range(0,len(data)):
	data[i]=data[i].split('\t')

npdata=numpy.array(data)
npdata=numpy.cast['float'](npdata)
npdata=numpy.rot90(npdata,3)

driver = gdal.GetDriverByName( format )
dst_ds = driver.Create( OUT_FILE, 2001, 2001, 1, gdal.GDT_Float32)
dst_ds.SetGeoTransform( [ 40.005, 0.01, 0, -110.005, 0, 0.01 ] )
srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection( srs.ExportToWkt() )
dst_ds.GetRasterBand(1).WriteArray(npdata)
dst_ds=None
