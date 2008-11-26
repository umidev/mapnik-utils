#!/usr/bin/env python

from mapnik import *

mapfile = 'world_styles.xml'
map_output = 'map/hello_world_using_xml_config.png'
projection = '+proj=latlong +datum=WGS84'

m = Map(600, 300)
load_map(m, mapfile)
bbox = Envelope(Coord(-180.0, -90.0), Coord(180.0, 90.0))
m.zoom_to_box(bbox) 
render_to_file(m, map_output) 
