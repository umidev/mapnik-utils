#!/usr/bin/env python

from mapnik import *
m = Map(600,300,'+proj=latlong +datum=WGS84')

def print_features(fs):
    if hasattr(fs,'next'):        # mapnik 0.5.x
        feat = fs.next()
        while feat:
            print feat
            feat = fs.next()
    else:                         # mapnik 0.6.x
        for feat in fs.features:
            print feat

m.background = Color('steelblue')
s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='../../../data/tm_wgs84_sans_antarctica')
lyr.styles.append('My Style')
m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())

#render_to_file(m, 'test.png')

f_set = m.query_point(0,-122,48)
print 'Queried Layer #%s, at longitude: %s, Latitude: %s' % (0,-122,48)
print_features(f_set)

f_set = m.query_map_point(0,200,175)
print 'Queried Layer #%s using pixel coodinates from upper left 0,0 origin -> distance right: %s, distance from top: %s' % (0,200,175)
print_features(f_set)
