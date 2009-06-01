#!/usr/bin/env python

from mapnik import *
mapfile = 'mapfile.xml'
map_output = 'map/spherical_mercator.png'
m = Map(600, 400)
load_map(m, mapfile)
spherical_mercator = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'

# Override projection in mapfile, setting rendered map projection
m.srs = spherical_mercator

# Set a bbox by reprojection Long/Lat coordinates
p = Projection(spherical_mercator)
merc = p.forward(Envelope(-180.0,-45.0,180.0,80.0))

m.zoom_to_box(merc)
render_to_file(m, map_output)