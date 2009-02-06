#!/usr/bin/env python

from mapnik import *
# modified from: http://spatialreference.org/ref/esri/54024/proj4/
m = Map(700,600,'+proj=bonne +lon_0=0 +lat_1=90 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
m.background = Color('#D82815')
s,r = Style(),Rule()
r.symbols.append(PolygonSymbolizer(Color('#FC8D59')))
r.symbols.append(LineSymbolizer(Color('#88000F'),.5))
s.rules.append(r)
m.append_style('style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='../../data/tm_wgs84_sans_antarctica')
lyr.styles.append('style')
m.layers.append(lyr)

s,r = Style(),Rule()
r.symbols.append(LineSymbolizer(Color('#F0E5E3'),.5))
s.rules.append(r)
m.append_style('style2',s)
lyr = Layer('graticules')
lyr.datasource = Shapefile(file='graticule')
lyr.styles.append('style2')
m.layers.append(lyr)
#m.zoom_all()
m.zoom_to_box(Envelope(-12816966,-22008607,26348930,11562161))
render_to_file(m, 'bonne.png')