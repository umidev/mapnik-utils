#!/usr/bin/env python

from mapnik import *

# Map
m = Map(600,300,'+proj=latlong +datum=WGS84')
m.background = Color('steelblue')

# Styles
poly = PolygonSymbolizer(Color('lavender'))
line = LineSymbolizer(Color('slategray'),.3)
s,r = Style(),Rule()
r.symbols.extend([poly,line])
s.rules.append(r)
m.append_style('My Style',s)

# Layer
lyr = Layer('world')
lyr.datasource = Shapefile(file='../data/world_borders')
lyr.srs = '+proj=latlong +datum=WGS84'
lyr.styles.append('My Style')
m.layers.append(lyr)

# Render
m.zoom_to_box(lyr.envelope())
render_to_file(m, 'map/hello_world_in_pure_python.png')