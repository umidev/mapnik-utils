#!/usr/bin/env python

import cairo
from mapnik import *

mapfile = '../world_population/population.xml'
map_output = 'population'
projection = '+proj=latlong +datum=WGS84'
mapnik_map = Map(1000, 500)
load_map(mapnik_map, mapfile)
bbox = Envelope(-180.0,-90.0,180.0,90.0)
mapnik_map.zoom_to_box(bbox)

svg_file = open('%s.svg' % map_output, 'w')
svg_surface = cairo.SVGSurface(svg_file.name, mapnik_map.width, mapnik_map.height)
render(mapnik_map, svg_surface)
svg_surface.finish()

pdf_file = open('%s.pdf' % map_output, 'w')
pdf_surface = cairo.PDFSurface(pdf_file.name, mapnik_map.width, mapnik_map.height)
render(mapnik_map, pdf_surface)
pdf_surface.finish()
