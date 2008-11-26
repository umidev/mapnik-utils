#!/usr/bin/env python

from mapnik import *
m = Map(500,400)
m.background = Color('steelblue')
load_map(m, 'mapfile.xml')

# Override the EPSG:4326 projection in the mapfile
m.srs = '+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'

# full extent
#bbox = Envelope(-196813697.178490, -100120989.481879, 160561884.749931,191038283.027071)
# 	Antarctica extent from ogrinfo
# (-2508600.864368, -2135351.687055) - (2639590.084551, 2161107.600173)

# lower left x/y, upper right x/y
bbox = Envelope(-2600000, -2200000, 2700000, 2200000)
m.zoom_to_box(bbox)
render_to_file(m, 'map/reprojected_antarctica_from_xml.png')
save_map(m, 'map/reprojected_antarctica_from_xml.xml')