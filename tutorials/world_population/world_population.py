#!/usr/bin/env python

from mapnik import *

mapfile = "population.xml"
m = Map(1400, 600)
load_map(m, mapfile)
bbox = Envelope(Coord(-180.0, -75.0), Coord(180.0, 90.0))
m.zoom_to_box(bbox) 
render_to_file(m, 'map/world_population.png', 'png')