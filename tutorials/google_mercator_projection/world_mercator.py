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
lower_left_xy = p.forward(Coord(-180.0, -45.0))
upper_right_xy = p.forward(Coord(180.0, 80.0))
bbox = Envelope(lower_left_xy,upper_right_xy)

# Or you can set a bbox by reprojecting a Long/Lat envelope
# wgs84_bbox = Envelope(-180.0,-60.0,180.0, 60.0)
# alt_bbox = forward_(wgs84_bbox, p)
# print alt_bbox

m.zoom_to_box(bbox)
render_to_file(m, map_output)