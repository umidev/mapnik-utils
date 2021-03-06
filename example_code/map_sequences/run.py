#!/usr/bin/env python

import os
import mapnik

# create basemap
m = mapnik.Map(800,600)
mapnik.load_map(m,'population.xml')

# grab the countries layer
countries = m.layers[0]
ds = countries.datasource
countries.styles.append('selected')

featureset = ds.all_features()
criteria = mapnik.Filter("[POP2005] > 100000000")

# get features that pass criteria
queryset = [f for f in featureset if criteria.passes(f)]

for feature in queryset:
    m.zoom_to_box(feature.envelope())
    m.zoom(1.05)
    name = str(feature.attributes['NAME'])
    print 'Matched %s...' % name
    feature_filter = mapnik.Filter("[NAME] = '%s'" % name)
    # selected/highlighted style
    s,r = mapnik.Style(),mapnik.Rule()
    r.symbols.append(mapnik.LineSymbolizer(mapnik.Color('darkorange'),3))
    r.symbols.append(mapnik.LineSymbolizer(mapnik.Color('yellow'),2))
    t = mapnik.TextSymbolizer('NAME', 'DejaVu Sans Book', 30, mapnik.Color('rgba(0,0,0,.8)') )
    t.avoid_edges = True
    t.halo_fill = mapnik.Color('rgba(255,255,255,.2)')
    t.halo_radius = 2
    r.symbols.append(t)
    r.filter = feature_filter
    s.rules.append(r)
    m.remove_style('selected')
    m.append_style('selected',s)
    im = mapnik.Image(m.width,m.height)
    mapnik.render(m, im)
    file = name + '.png'
    print 'Rendering %s...' % file
    im.save(file)

os.system('open *.png')