#!/usr/bin/env python

from mapnik import *

# register the fonts
from glob import glob
NEW_FONTS_DIR = 'fonts/'
fonts = glob('%s*.ttf' % NEW_FONTS_DIR)

if len( fonts ) == 0:
    print "### WARNING: No ttf files found in '%s'." % NEW_FONTS_DIR
else:
    map(FontEngine.instance().register_font, fonts)

# Then if you are writing your styles in python do:
m = Map(600,800,'+proj=latlong +datum=WGS84')

m.background = Color('transparent')

text = Style()
text_rule=Rule()
t = TextSymbolizer('mr','gargi Medium',30,Color('black'))
t.halo_fill = Color('white')
t.halo_radius = 1
text_rule.symbols.append(t)
text.rules.append(text_rule)
m.append_style('Text',text)

s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('darkorange')))
r.symbols.append(LineSymbolizer(Color('green'),0.5))
s.rules.append(r)
m.append_style('Polygons',s)

lyr = Layer('My Postgis Layer')
lyr.datasource = PostGIS(host='localhost', dbname='test', user='postgres', password='', table='mrdata')
lyr.srs = '+proj=latlong +datum=WGS84'
lyr.styles.append('Polygons')
lyr.styles.append('Text')
m.layers.append(lyr)

bbox = Envelope(73.0020294189453,17.99977684021,73.0031890869141,18.0018711090088)
m.zoom_to_box(bbox)
render_to_file(m, 'test_output.png')
save_map(m, 'mapfile.xml')