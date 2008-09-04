#!/usr/bin/env python
#
# Leslie Wu
#
# sea.py has code portions adapted from rundemo.py (part of Artem's Mapnik/demo) and cali.cpp
 
try:
    from mapnik import *
except:
    print "Couldn't import mapnik libraries!"
    raise
 
m = Map(800,600,"+proj=latlong +ellps=WGS84")
m.background = Color(220, 226, 240)
 
# Layers are added in stacking order (i.e. bottom layer first)
 
state_lyr = Layer('States')
state_lyr.datasource = Shapefile(file='../data/statesp020')
state_lyr.styles.append('states')
m.layers.append(state_lyr)
 
strict = True
load_map(m, "style.xml", strict) # Load XML
 
ds = state_lyr.datasource
q = Query(state_lyr.envelope(), 1.0)
q.add_property_name('STATE') # Without this call, no properties will be found
 
extent = Envelope()
featureset = ds.features(q) # Zoom into WA by querying feature geometry
 
feat = featureset.next()
filt = Filter("[STATE] = 'Washington'")
 
extent = Envelope()
while (feat):
    if filt.passes(feat): # note 'pass' is a reserved word in Python
        for i in range(feat.num_geometries()):
            geom = feat.get_geometry(i)
            if (extent.width() < 0 and extent.height() < 0):
                extent = geom.envelope()
            extent.expand_to_include(geom.envelope())
 
    feat = featureset.next()
 
print extent
 
# Add map points!
pds = PointDatasource()
pds.add_point(-121.76, 46.85, "name", "Mount Rainier") # via Wikipedia
pds.add_point(-121.49, 46.20, "name", "Mount Adams")
pds.add_point(-121.81, 48.78, "name", "Mount Baker")
# ...
 
mtn_layer = Layer('Mountains')
mtn_layer.datasource = pds
mtn_layer.styles.append('mountains')
mtn_layer.styles.append('mountain_labels')
m.layers.append(mtn_layer)
 
# Set the initial extent of the map.
 
m.zoom_to_box(extent)
m.zoom(1.05)
# Render
 
im = Image(m.width,m.height)
render(m, im)
 
# Save image to files
im.save('sea.png', 'png') # true-colour RGBA