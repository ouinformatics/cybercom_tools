from celery.task import task
import time 
from StringIO import StringIO
#from cybercom.api.catalog import datalayerutils as dl
from urllib2 import urlopen
from cybercom.data.catalog import datalayer
import os


@task(serializer="json")
def add(x, y):
    md= datalayer.Metadata()
    return md.Search('dt_location')
    #return x + y 

@task
def sleep(s):
    time.sleep(s)
    return None

def getfile(url):
    pass    

def dozip(files):
    ''' Takes a list of file locations and returns a zipfile with directories stripped ''' 
    inMemoryOutputFile = StringIO()
    zipFile = ZipFile(inMemoryOutputFile, 'w')
    for filename in files:
        zipFile.writestr(os.path.basename(filename), open(filename, 'r').read() )
    zipFile.close()
    inMemoryOutputFile.seek(0)
    return inMemoryOutputFile

@task
def zipfiles(commons_id, cat_id, start_date, end_date=None, var_id=None):
    outpath = '/data/output'
    urls = dl.event_results_by_time(commons_id, cat_id, start_date, end_date, var_id)
    for url in urls:
        open(os.path.join(outpath,os.path.basename(url)), 'w').write(urlopen(url).read())

