#!/usr/bin/env python

from mapnik import *
m = Map(600,300,'+proj=latlong +datum=WGS84')

m.background = Color('steelblue')
s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='../data/world_borders')
lyr.styles.append('My Style')
m.layers.append(lyr)

m.zoom_to_box(lyr.envelope())
render_to_file(m, 'map/hello_world_in_pure_python.png')
render_to_file(m, 'map/hello_world_in_pure_python_small.png','png256')
save_map(m, 'map/hello_world_in_pure_python.xml')