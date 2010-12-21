import numpy
import sys
import subprocess 
import re
from osgeo import gdal
from osgeo.gdalconst import *
import osgeo.osr as osr

EXEC_PATH='/home/bcremeans/nmq/NMQ_CartBinaryReader/read_nmq'
#FILE_PATH='/scratch/data/nws/nexrad/tile6/unqc_cref/'
#OUT_FILE='/home/bcremeans/nmq/NMQ_CartBinaryReader/out.gtiff'

def usage():
	print "usage: python read_nmq inputfile outputfile"

try:
	FILE_PATH=sys.argv[1]
	OUT_FILE=sys.argv[2]
except:
	usage()
	sys.exit(2)

format='GTiff'

#cline=[EXEC_PATH,FILE_PATH+'UNQC_CREF.20090728.112000','0']
cline=[EXEC_PATH,FILE_PATH,'0']
cmd=subprocess.Popen(cline,stdout=subprocess.PIPE)
oput=cmd.communicate()[0].strip().split('\n')
headers=oput[:24]
data=oput[25:]
headers=headers[9:]
lat=float(re.findall('-?\d.+',headers[6])[0])
lon=float(re.findall('-?\d.+',headers[7])[0])
col=int(re.findall('\d.+',headers[8])[0])
row=int(re.findall('\d.+',headers[9])[0])
lat_size=float(re.findall('-?\d.+',headers[10])[0])
lon_size=float(re.findall('-?\d.+',headers[11])[0])
time=headers[14]
data.reverse()
for i in range(0,len(data)):
	data[i]=data[i].split('\t')

npdata=numpy.array(data)
npdata=numpy.cast['float'](npdata)
npdata=numpy.rot90(npdata)

driver = gdal.GetDriverByName( format )
dst_ds = driver.Create( OUT_FILE, col, row, 1, gdal.GDT_Float32)
dst_ds.SetGeoTransform( [ lon, lon_size, 0, lat, 0, lat_size ] )
srs = osr.SpatialReference()
srs.SetWellKnownGeogCS("WGS84")
dst_ds.SetProjection( srs.ExportToWkt() )
dst_ds.GetRasterBand(1).WriteArray(npdata)
dst_ds=None


