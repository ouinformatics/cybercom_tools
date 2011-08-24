#!/usr/bin/env python2.6
from radar_wms import radar_wms
from datetime import datetime, timedelta
from os.path import join

outbase = '/scratch/www/map/radar_wms/'

def days(start_date):
    delta = timedelta(days=1)
    current_date = start_date
    while current_date < datetime.now():
        current_date += delta
        yield current_date

dates = [ {'date_iso': date.isoformat(), 
            'date_short_str': str(date)[0:10].replace('-','_'), 
            'date_short': str(date)[0:10],
            'date_end': str(date + timedelta(days=1))[0:10], 
           } for date in days(datetime(2008,01,01)) 
        ]

for date in dates: 
    fname = date['date_short_str'] + '.map'
    fileout = open(join(outbase, fname), 'w')
    outstring = str(radar_wms( searchList=[date] ))
    fileout.write(outstring)
    fileout.close()



