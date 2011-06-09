import urllib2
from subprocess import Popen, PIPE
import shlex
from datetime import datetime, timedelta

toget =[    
    ['PRES','surface'],
    ['PRES','max wind'],
    ['UGRD','max wind'],
    #['VGRD','max wind'], # Ugrid and Vgrid are together
    ['CRAIN','surface'],
    ['CFRZR','surface'],
    ['CICEP','surface'],
    ['CSNOW','surface'],
    ['VIS','surface'],
    ['TMP','surface'],
    ['TMP','100 mb'],
    ['TMP','200 mb'],
    ['TMP','300 mb'],
    ['TMP','400 mb'],
    ['TMP','500 mb'],
    ['TMP','600 mb'],
    ['UGRD','100 mb'],
    ['UGRD','200 mb'],
    ['UGRD','300 mb'],
    ['UGRD','400 mb'],
    ['UGRD','500 mb'],
    ['UGRD','600 mb'],
    #['VGRD','100 mb'],  # Ugrid and Vgrid are together
    #['VGRD','200 mb'],  # Ugrid and Vgrid are together
    #['VGRD','300 mb'],  # Ugrid and Vgrid are together
    #['VGRD','400 mb'],  # Ugrid and Vgrid are together
    #['VGRD','500 mb'],  # Ugrid and Vgrid are together
    #['VGRD','600 mb'],  # Ugrid and Vgrid are together
    ['RH','100 mb'],
    ['RH','200 mb'],
    ['RH','300 mb'],
    ['RH','400 mb'],
    ['RH','500 mb'],
    ['RH','600 mb'],
    ['VVEL','100 mb'],
    ['VVEL','200 mb'],
    ['VVEL','300 mb'],
    ['VVEL','400 mb'],
    ['VVEL','500 mb'],
    ['VVEL','600 mb']
]

def getindex(url):
    """
    Get an inventory file.
    """
    try:
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
    except:
        print "Does the URL exist?"
    return [ line.strip().split(':') for line in f.readlines() ]

def computerange(lyrindex):
    """
    Find ranges from inventory file.
    """
    for i in range(len(lyrindex)):
        if i != len(lyrindex) - 1:
            if lyrindex[i][0].find('.') > 0: # special case where inventory files have two records
                lyrindex[i].append( 'range=%s-%s' %( lyrindex[i][1], int(lyrindex[i+2][1]) - 1) )
            else:
                lyrindex[i].append( 'range=%s-%s' %( lyrindex[i][1], int(lyrindex[i+1][1]) - 1) )
        else:
            lyrindex[-1].append( 'range=%s' % ( lyrindex[-1][1] ) )    
    return lyrindex

def selectlayers(lyrindex,selection):
    """
    Select layers from a python list of variable/level
    
    Example selection:
    selection = [['PRES','surface'],['PRES','max wind']]

    """
    return [ [item[2].replace('D=','') ,item[3],item[4],item[-1].replace('range=','') ] 
                for item in lyrindex if [item[3],item[4]] in selection ]

def dateurl(timestamp, urlbase, urlformat):
    """
    Example:
    >>> dateurl(datetime.datetime(2010,07,23,0,0), 'ftp://nomads.ncdc.noaa.gov/', 'RUC/13km/%Y%m/%Y%m%d/ruc2_130_%Y%m%d_%H%M_000.inv')
    """
    target = timestamp.strftime(urlformat)
    return urlbase + target

def getlayers(url,layerselection):
    """
    Grab data from URL for various ranges.
    """
    req = urllib2.Request(url)
    for date,layer,level,getrange in layerselection:
        # Prepare request
        if getrange.find('-') > 0:   # Check to make sure we have an actual range
            start,stop = getrange.split('-')
            req.headers['Range'] = 'bytes=%s-%s' % (start, stop)
            #print req.headers['Range']
        else: # otherwise we're the last record in the file.
            start = getrange
            req.headers['Range'] = 'bytes=%s' % (start)
        
        # Open file
        fi = urllib2.urlopen(req)
        #print fi.headers.get('Content-Range')
        level = level.replace(' ','_')
        date = date.replace('d=','')       
        fname = '%s_%s_%s.grb' % (date, layer, level)
        fo = open(fname, 'w')
        fo.write(fi.read())
        print "Wrote %s" % fname

def date_range(start_datetime, end_datetime):
    ''' Generator for datetime_ranges'''
    d = start_datetime
    delta = timedelta(hours=1)
    while d <= end_datetime:
        yield d
        d += delta


if __name__ == '__main__':
    import sys
    product = sys.argv[1]
    date = sys.argv[2]
    if product.upper() == 'RUC':
        if date.find(',') > 0:
            start,stop = date.split(',')
            start = datetime.strptime(start, '%Y%m%d.%H%M%S')
            stop = datetime.strptime(stop, '%Y%m%d.%H%M%S')
            for modelrun in date_range(start,stop):
                url = dateurl( modelrun, 'http://nomads.ncdc.noaa.gov/', 'data/ruc13/%Y%m/%Y%m%d/ruc2_130_%Y%m%d_%H%M_000.inv')
                print url
                layers = selectlayers(computerange(getindex(url)), toget)
                url = url.replace('.inv','.grb2')
                getlayers(url,layers)
        else:
            date = datetime.strptime(date, '%Y%m%d.%H%M%S')
            url = dateurl( date, 'http://nomads.ncdc.noaa.gov/', 'data/ruc13/%Y%m/%Y%m%d/ruc2_130_%Y%m%d_%H%M_000.inv')
            print url
            computerange(getindex(url))
            layers = selectlayers(computerange(getindex(url)), toget)
            url = url.replace('.inv','.grb2')
            getlayers(url,layers)

    else:
        print "No supported product selected, supported products are: ['RUC']"

