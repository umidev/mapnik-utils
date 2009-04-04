#!/usr/bin/env python

from mapnik import *

m = Map(600,300,'+proj=latlong +datum=WGS84')
m.background = Color('white')

s,r = Style(), Rule()
r.symbols.append(LineSymbolizer(Color('black'),1))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Ogr(file='fells_loop.gpx',layer='routes')

# tracks
# routes
# waypoints
# route_points
# track_points

lyr.styles.append('My Style')
m.layers.append(lyr)

m.zoom_to_box(lyr.envelope())
render_to_file(m, 'gps_tracks.png')
