#!/usr/bin/python
from datetime import datetime 
from urllib2 import urlopen
import json
import pyproj

data="http://fire.rccc.ou.edu/mongo/db_find/eomf/gps_all/{'limit':100}"

gps_all = json.loads(urlopen(data).read())

t_srs="+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +no_defs +a=6371007.181 +b=6371007.181 +to_meter=1"
s_srs="+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"


def nearest_8d( obs_date ):
    ''' Returns the nearest 8-day composite's julian day '''
    jday = int(obs_date.strftime('%j'))
    for start, stop in zip(range(1,365,8), range(9,365,8)):
        if jday >= start and jday < stop:
            return str(start).zfill(3)
        

for item in gps_all:
    obs_date = datetime.strptime(item['gmt_date'], '%m/%d/%Y')
    modis_date = nearest_8d(obs_date) 
    p1 = pyproj.Proj(s_srs)
    p2 = pyproj.Proj(t_srs)
    x, y = pyproj.transform( p1, p2,  item['longitud'], item['latitude'])
    rast = '%s%s%s%s' % ('input=MOD09A1.A', obs_date.strftime('%Y'), nearest_8d(obs_date), '_ndvi@MOD09A1_global')
    print '%s %s %s=%s,%s' % ('r.what', rast, 'east_north', x, y )


