from osgeo import gdal
from netCDF4 import Dataset
import numpy as np


def modisStack(outname,inlist):
    outgrp = Dataset('/data/modists/out2000.nc', 'w')
    
    year = outgrp.createDimention('year',None)
    jd = outgrp.createDimension('jd',None)
    x = outgrp.createDimension('x',2400)
    y = outgrp.createDimension('y',2400)

    years = outgrp.createVariable('year','i4',('year',))
    jds = outgrp.createVariable('jd','i4',('jd',))
    xs = outgrp.createVariable('x','i4',('x',), contiguous = True)
    ys = outgrp.createVariable('y','i4',    


modisStack('/data/modists/out2000.nc','w')
