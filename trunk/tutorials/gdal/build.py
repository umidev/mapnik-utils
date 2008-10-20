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
lyr.datasource = Gdal(file='blake2rgb.tif')
lyr.styles.append('My Style')
m.layers.append(lyr)

m.zoom_to_box(lyr.envelope())
render_to_file(m, 'test.png')
save_map(m, 'test.xml')