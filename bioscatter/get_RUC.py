# Rquires owslib to be installed
# Install pip
# easy_install pip
# Install OWSLib
# pip install svn+http://svn.gispython.org/svn/gispy/OWSLib/trunk

# Based on guidance from: http://trac.gispython.org/lab/browser/OWSLib/trunk/tests/wcs_thredds.txt?rev=1213
from owslib.wcs import WebCoverageService
from datetime import datetime, timedelta
import os, sys

fcast='000' # We only want the zero hour forecasts
outpath = '/scratch/data/nws/ruc/' # destination for output files
model = 'RUC' # Model to use a prefix for filenames

products = ['Pressure_surface', 
            'Pressure_maximum_wind', 
            'U-component_of_wind_maximum_wind', 
            'V-component_of_wind_maximum_wind', 
            'Categorical_Rain', 
            'Categorical_Freezing_Rain', 
            'Categorical_Ice_Pellets', 
            'Categorical_Snow', 
            'Visibility', 
            'Precipitation_rate', 
            'Temperature', 
            'Relative_humidity', 
            'U-component_of_wind_height_above_ground', 
            'V-component_of_wind_height_above_ground',
            'Vertical_velocity_pressure' ]

def date_range( start_datetime, end_datetime, minutes=60):
    ''' Generator for datetime_ranges at 60 minute intervals '''
    d = start_datetime
    delta = timedelta(minutes=minutes)
    while d <= end_datetime:
        yield d
        d += delta

def reproject(s_srs, t_srs):
    ''' Reproject a raster using gdalwarp ''' 
    pass

def get_products(products, dt, bbox=None):
    ''' Get a list of products for a given date and time 
        Example:
        >> get_products(['Temperature'], datetime(2010,10,10,12,0))
    ''' 
    saved_files = []
    url_params = (dt.strftime('%Y%m'), dt.strftime('%Y%m%d'), dt.strftime('%Y%m%d'), dt.strftime('%H%M'), fcast)
    server_url = 'http://nomads.ncdc.noaa.gov/thredds/wcs/ruc13/%s/%s/ruc2_130_%s_%s_%s.grb2' % url_params
    try:
        wcs = WebCoverageService(server_url,version='1.0.0')
    except:
        print >> sys.stderr, "Bad URL!"
    else:
        if set(products).issubset(wcs.contents.keys()):
            print >> sys.stderr, 'Requested products are a subset of available products'
        else:
            print >> sys.stderr, 'Some product(s) selected do not exist'
        if bbox is None:
            bbox = (-139, -57.995, 16, 55) # CONUS
        date_time = dt.isoformat() + 'Z'
        for product in products:
            filename = outpath + model + '_' + date_time.replace(':','') + '_' + product + '.tif'
            if os.path.exists(filename): # Check if file exists so we don't download duplicates
               pass
            else: 
                try:
                    output = wcs.getCoverage(identifier = product, time = [date_time], bbox= bbox, format='GeoTiff_float')
                except urllib2.HTTPError:
                    print "Bad URL"
                f = open(filename, 'wb')
                f.write(output.read())
                f.close() 
                saved_files.append(filename)
                print >> sys.stderr, 'Saved: ' + filename
    return saved_files

# Command-line access
if __name__ == '__main__':
    start = datetime.strptime(sys.argv[1], '%Y%m%d.%H%M%S')
    stop = datetime.strptime(sys.argv[2], '%Y%m%d.%H%M%S')
    for time in date_range(start, stop):
        files_out = {}
        files_out[time.isoformat()] = get_products(products, time)

 

# Grids download as .tif files in native Conical projection.  They can be reprojected with: gdalwarp -t_srs WGS84 source.tif target.tif


