#!/usr/bin/env python
import struct

from mapnik2 import *
m = Map(7001,3501,'+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

def rgb2hex(r,g,b):
    ''' Converts rgb triplicates to hex '''
    rgb = (r,g,b)
    return "#" + struct.pack('BBB',*rgb).encode('hex')

colorizer = RasterColorizer()
bands = [(value, Color(color) ) for value, color in [ 
# This color map copies exactly the color map at:
#   http://www.weather.gov/radar_tab.php
(-30, rgb2hex(204,255,255)),
(-25, rgb2hex(206,154,206)),
(-20, rgb2hex(153,102,153)),
(-15, rgb2hex(102,51,102)),
(-10, rgb2hex(206,206,154)),
(-5, rgb2hex(154,154,103)),
#(0, rgb2hex(100,100,100)),  # Color map at 0 is causing rendering problems.
(5, rgb2hex(4,233,231)),
(10, rgb2hex(1,161,246)),
(15, rgb2hex(3,0,244)),
(20, rgb2hex(2,252,2)),
(25, rgb2hex(1,199,1)),
(30, rgb2hex(0,142,0)),
(35, rgb2hex(253,248,2)),
(40, rgb2hex(229,188,0)),
(45, rgb2hex(253,149,0)),
(50, rgb2hex(253,0,0)),
(55, rgb2hex(214,0,0)),
(60, rgb2hex(188,0,0)),
(65, rgb2hex(248,0,253)),
(70, rgb2hex(153,85,200)),
(75, rgb2hex(253,253,253))
]]
 
for value, color in bands:
    colorizer.append_band(value,color)

m.background = Color('transparent')
s = Style()
r=Rule()
sym = RasterSymbolizer()
sym.colorizer = colorizer
r.symbols.append(sym)
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Gdal(file='/Users/jduckles/out_tmp.tif', band=1)
lyr.styles.append('My Style')
m.layers.append(lyr)

m.zoom_to_box(lyr.envelope())
render_to_file(m, 'test.png')
save_map(m, 'test.xml')



