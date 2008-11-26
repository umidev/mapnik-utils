#!/usr/bin/env python

from mapnik import *
from random import *

UNIQUE = True

m = Map(1000,550)
m.background = Color('transparent')

# http://spatialreference.org/ref/user/north-pacific-albers-conic-equal-area/
north_pacific_albers = '+proj=aea +lat_1=30 +lat_2=70 +lat_0=52 +lon_0=-170 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs'
m.srs = north_pacific_albers

def random_rgb():
  return int(random() * 255)

def generate_unique_values(features):
  s = Style()
  if UNIQUE:
      for feat in range(1,features+1):
        r=Rule('%s' % feat)
        condition = '[ID]=%s' % (feat)
        r.filter = Filter(condition)
        rgb = '%s%s,%s%s,%s%s' % (random_rgb(),'%',random_rgb(),'%',random_rgb(),'%')
        r.symbols.append(PolygonSymbolizer(Color('rgb(%s)' % rgb)))
        r.symbols.append(LineSymbolizer(Color('black'),.1))
        # should eventually break this out so that the text is always on top
        t = TextSymbolizer('ECOREGION', 'DejaVu Sans Bold', 10, Color('rgb(%s)' % rgb))
        t.halo_fill = Color('white')
        t.halo_radius = 1
        r.symbols.append(t)
        s.rules.append(r)
  else:
      r=Rule()
      r.symbols.append(PolygonSymbolizer(Color('steelblue')))
      r.symbols.append(LineSymbolizer(Color('black'),.1))
      # should eventually break this out so that the text is always on top
      t = TextSymbolizer('ECOREGION', 'DejaVu Sans Bold', 10, Color('black'))
      t.halo_fill = Color('white')
      t.halo_radius = 1
      r.symbols.append(t)
      s.rules.append(r)  
  return s

# Fetch feature count from ogrinfo
# $ ogrinfo -so -al ../../../data/north_pacific_ecoregions.shp | grep 'Feature Count:'
# Feature Count: 37
features = 37 # Mapnik will need to expose datasource properties to be able to read this dynamically

# Attach random RGB values to PolygonSymbolizer rule and return the style
unique_style = generate_unique_values(features)

m.append_style('Random RGB values',unique_style)
lyr = Layer('shape')
lyr.datasource = Shapefile(file='../../sample_data/north_pacific_ecoregions')
lyr.srs = north_pacific_albers
lyr.styles.append('Random RGB values')
m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())

if UNIQUE:
    render_to_file(m,'map/unique_values.png')
else:
    render_to_file(m,'map/single_value.png')