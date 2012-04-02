import cybercomq.arcgis.nmq as nmq
import os, tempfile, shutil, sys
import logging
from osgeo import gdal
import numpy as np
import numpy.ma as ma
from datetime import datetime, timedelta
from pandas import *
from multiprocessing import Pool
import pymongo


def fiveminute(start_datetime, end_datetime):
    ''' Generator for datetime_ranges at 5 minute intervals '''
    d = start_datetime
    delta = timedelta(minutes=5)
    while d <= end_datetime:
        yield d.strftime('%Y%m%d.%H%M%S')
        d += delta

def splitday(start_datetime, end_datetime):
    d = start_datetime
    delta = timedelta(days=7)
    while d <= end_datetime:
        yield d.strftime('%Y%m%d.%H%M%S')
        d += delta

def tomongo(host,db,col,data):
    con = pymongo.Connection(host)
    db_to = con[db]
    col_to = db_to[col]
    col_to.insert(data)

def parallelwrap(task_id,start_date, stop_date):
    for week in splitday(start_datetime, end_datetime):
        p.apply_async( crefstats, kwargs=dict(location=location, start_date=week, stop_date=week + timedelta(days=7)) )

def crefstats(location='-96.60,33.00', start_date=None, stop_date=None, task_id=None):
    output = []
    for ts in fiveminute(start_date,stop_date):
        outdir = tempfile.mkdtemp(dir='/tmp')
        try:
            fname = nmq.getScene(ts, '-96.60,33.00', outdir)
            raster = gdal.Open(fname)
            band = raster.GetRasterBand(1).ReadAsArray()
            mband = ma.masked_less_equal(band,-99)
            shutil.rmtree(outdir)
            logging.info('Timestep %s' % ts)
            tomongo('fire.rccc.ou.edu','bioscatter','maxrefl', {"task_id": task_id, "loc":location,"ts":datetime.strptime(ts, '%Y%m%d.%H%M%S'),"max":float(ma.max(mband)),"min":float(ma.min(mband)),"mean":float(ma.mean(mband)), "std":float(ma.std(mband))})
        except:
            logging.error('Had problem at timestep %s' % ts)
            logging.error(sys.exc_info())
            tomongo('fire.rccc.ou.edu','bioscatter','maxrefl', {"task_id": task_id, "loc":location,"ts":ts,"max":None,"min":None,"std":None})
    return DataFrame(output)

