#!/usr/bin/env python

# http://spatialreference.org/ref/user/mollweide-on-greenwich/proj4/

from mapnik import *
mapfile = 'mapfile.xml'
map_output = 'map/world_mollweide.png'
m = Map(700, 400)
load_map(m, mapfile)
mollweide = '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs '

# Override projection in mapfile, setting rendered map projection
m.srs = mollweide

# Set a bbox by reprojection Long/Lat coordinates
p = Projection(mollweide)
lower_left_xy = p.forward(Coord(70.0, -60.0))
upper_right_xy = p.forward(Coord(180.0, 90.0))
bbox = Envelope(lower_left_xy,upper_right_xy)

# Or you can set a bbox by reprojecting a Long/Lat envelope
# wgs84_bbox = Envelope(-180.0,-60.0,180.0, 60.0)
# alt_bbox = forward_(wgs84_bbox, p)
# print alt_bbox

m.zoom_to_box(bbox)
render_to_file(m, map_output)