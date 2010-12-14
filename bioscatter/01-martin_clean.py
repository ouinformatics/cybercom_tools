#!/usr/bin/env python2.7
'''
#Data are converted from fixed-width to delimited in bash as follows:
sed 's/ \{1,10\}/|/g' 20100930-123D-output.365088132.txt > 20100930-123D-output.365088132.del
'''
import csv 
import cx_Oracle as db

con = db.connect('eco/b00mer@oubcf1')

def get_latlon(fileloc):
    ''' Helper function to extract just lat, lon for the second file which does not explicitly have it.'''
    f1 = open(fileloc, 'r')
    header1 = f1.readline()
    header2 = f1.readline()
    lat = f1.readline().strip().split('|')[1:] # skip the date format column
    lon = f1.readline().strip().split('|')[2:] # start with 3rd cell due to weirdness of incoming file format
    return lat, lon

def read_rain(fileloc, item):
    ''' read the rainfall data from nexrad radar files of point locations '''
    f1 = open(fileloc, 'r')
    header1 = f1.readline()
    header2 = f1.readline()
    lat = f1.readline().strip().split('|')[1:] # skip the date format column
    lon = f1.readline().strip().split('|')[2:] # start with 3rd cell due to weirdness of incoming file format
    loc_id = range(0,len(lat)) # generate list of location ids.

    blank = f1.readline() # read the blank line

    outfile = open('/tmp/outfile.csv','w')
    output = csv.writer(outfile)
    output.writerow(['timestamp','loc_id','lat','lon','item','value'])

    iteml = [item] * len(lat)
    for line in f1.readlines():
        data = line.strip().split('|')
        timestamp = data[0]
        for loc in zip(loc_id,lat,lon,iteml,data[1:]):
            list_row = list(loc)
            list_row.insert(0,timestamp)
            output.writerow(list_row)
    outfile.close()

def read_reflectivity(fileloc, item):
    f1 = open(fileloc, 'r')
    lat, lon = get_latlon('/Users/jduckles/Downloads/data/20100930-123D-output.365088132.del')
    outfile = open('/tmp/outfile2.csv', 'w')
    output = csv.writer(outfile)
    output.writerow(['timestamp','loc_id','lat','lon','item','value'])
    loc_id = range(0,len(lat))
    iteml = [item] * len(lat)

    for line in f1.readlines():
        data = line.strip().split('|')
        timestamp = data[0]
        for loc in zip(loc_id, lat, lon, iteml, data[1:]):
            list_row = list(loc)
            list_row.insert(0,timestamp)
            output.writerow(list_row)
    outfile.close()



read_reflectivity('/Users/jduckles/Downloads/data/20100930-123D-output.83442912.del', 'reflectivity')
read_rain('/Users/jduckles/Downloads/data/20100930-123D-output.365088132.del', 'rain')


