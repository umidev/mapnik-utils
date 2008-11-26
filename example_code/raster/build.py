#!/usr/bin/env python

from mapnik import *
m = Map(400,500,'+proj=latlong +datum=WGS84')

m.background = Color('transparent')
s = Style()
r=Rule()
r.symbols.append(RasterSymbolizer())
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
# run $gdalinfo blake2rgb.tif to get lox,loy,hix,hiy
lyr.datasource = Raster(file='blake2rgb.tif',lox=-122.8346300,loy=48.6050000,hix=-122.7662967,hiy=48.5272222)
lyr.styles.append('My Style')
m.layers.append(lyr)

m.zoom_to_box(lyr.envelope())
render_to_file(m, 'test.png')
save_map(m, 'test.xml')