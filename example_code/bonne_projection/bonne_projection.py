#!/usr/bin/env python

from mapnik import *
# modified from: http://spatialreference.org/ref/esri/54024/proj4/
m = Map(600,600,'+proj=bonne +lon_0=0 +lat_1=90 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
m.background = Color('transparent')
s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
s.rules.append(r)
m.append_style('style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='../../data/tm_wgs84_sans_antarctica')
lyr.styles.append('style')
m.layers.append(lyr)
#m.zoom_all()
m.zoom_to_box(Envelope(-10019402,-14558607,3551366,1012161))
render_to_file(m, 'bonne.png')