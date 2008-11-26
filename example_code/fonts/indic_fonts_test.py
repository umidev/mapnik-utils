#!/usr/bin/env python

from mapnik import *

# register path to new true type fonts...
from glob import glob
NEW_FONTS_DIR = '/usr/share/fonts/truetype/ttf-devanagari-fonts/'
fonts = glob('%s/*.ttf' % NEW_FONTS_DIR)
if len( fonts ) == 0:
    print "### WARNING: No ttf files found in '%s'." % NEW_FONTS_DIR
else:
    map(FontEngine.instance().register_font, fonts)

# Then if you are writing your styles in python do:
m = Map(600,800,'+proj=latlong +datum=WGS84')

m.background = Color('transparent')

s2 = Style()
r2=Rule()
t2 = TextSymbolizer('MR','gargi Medium',30,Color('black'))
t2.halo_fill = Color('white')
t2.halo_radius = 1
r2.symbols.append(t2)
s2.rules.append(r2)
m.append_style('Text',s2)

s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('darkorange')))
r.symbols.append(LineSymbolizer(Color('green'),0.5))
s.rules.append(r)

m.append_style('Polys',s)

'''
lyr = Layer('My Postgis Layer')
lyr.datasource = PostGIS(host='localhost', dbname='test', user='postgres', password='', table='mrdata')
lyr.styles.append('My Style')
m.layers.append(lyr)
'''
lyr = Layer('Polygon Layer')
lyr.datasource = Shapefile(file='mrdata')
lyr.styles.append('Polys')
lyr.clear_label_cache = True
m.layers.append(lyr)

lyr2 = Layer('Text Layer')
lyr2.datasource = Shapefile(file='mrdata')
lyr2.styles.append('Text')
lyr2.clear_label_cache = True
m.layers.append(lyr2)

bbox = Envelope(73.0020294189453,17.99977684021,73.0031890869141,18.0018711090088)
m.zoom_to_box(bbox)
render_to_file(m, 'indic_fonts_test.png')
save_map(m, 'indic_fonts_test.xml')