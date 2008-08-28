#!/usr/bin/env python

from mapnik import *

# EPSG:3031
m = Map(600,500, '+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')

m.background = Color('steelblue')
s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='data/world_borders')
lyr.styles.append('My Style')
m.layers.append(lyr)

# full extent
#bbox = Envelope(-196813697.178490, -100120989.481879, 160561884.749931,191038283.027071)
# 	Antarctica extent from ogrinfo
# (-2508600.864368, -2135351.687055) - (2639590.084551, 2161107.600173)

# lower left x/y, upper right x/y
bbox = Envelope(-2600000, -2200000, 2700000, 2200000)
m.zoom_to_box(bbox)
render_to_file(m, 'map/reprojected_antarctica.png')
save_map(m, 'map/reprojected_antarctica.xml')