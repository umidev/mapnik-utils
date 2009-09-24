#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mapnik import *
 
#m = Map(800,600,"+proj=latlong +ellps=WGS84")
#m.background = Color(220, 226, 240)
state_lyr = Layer('States')
state_lyr.datasource = Shapefile(file='statesp020')
state_lyr.styles.append('states')
#m.layers.append(state_lyr)
#strict = True
#load_map(m, "style.xml", strict) # Load XML 
ds = state_lyr.datasource
q = Query(state_lyr.envelope(), 1.0)
q.add_property_name('STATE') # Without this call, no properties will be found
extent = Envelope()
featureset = ds.features(q) # Zoom into WA by querying feature geometry

print 

feat = featureset.next()
for item in feat.properties:
   print 'fishy?', item

print 'letting mapnik internally convert to string...\n' 

print feat
