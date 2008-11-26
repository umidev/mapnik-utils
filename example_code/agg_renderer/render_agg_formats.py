#!/usr/bin/env python

from mapnik import *

map_output = 'world'
m = Map(256,256,'+proj=latlong +datum=WGS84')

m.background = Color('steelblue')
s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='../../../data/world_borders')
lyr.styles.append('My Style')
m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())
m.zoom(.2)

agg_formats = {'png':'.png','png256':'.png','jpeg':'.jpg'}

for k,v in agg_formats.items():
    print '// --  Rendering %s -----------------------------' % k
    if k == 'png256':
       render_to_file (m,'%s_%s%s' % (map_output,k,v), k)
    else:
       render_to_file(m, '%s_%s%s' % (map_output,k,v))