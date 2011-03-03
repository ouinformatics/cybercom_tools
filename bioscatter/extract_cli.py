#!/usr/bin/env python2.6

import xmlrpclib
import sys

p = xmlrpclib.ServerProxy('http://localhost:8989/')

product = sys.argv[1]
lat = sys.argv[2]
lon = sys.argv[3]
rad = sys.argv[4]
start = sys.argv[5]
stop = sys.argv[6]

outname = '%s_%s_%s_%s.zip' % (start, stop, lat, lon)
output = open(outname, 'w')
output.write(p.extractTimeseries( product, lat, lon, rad, start, stop).data)




