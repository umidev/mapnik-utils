#!/usr/bin/env python

from mapnik import *
from georeference import render_to_wld

m = Map(10000,5000,'+proj=latlong +datum=WGS84')
m.background = Color('steelblue')
s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='../../../data/world_borders')
lyr.styles.append('My Style')
m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())
filepath = 'georeferenced'
raster = '%s.png' % filepath
world_file = '%s.wld' % filepath
mapfile = '%s.xml' % filepath
render_to_file(m, raster, 'png256')
render_to_wld(m, world_file)
# write out mapfile for a reference of the styles generated
# using the python bindings
save_map(m, mapfile)