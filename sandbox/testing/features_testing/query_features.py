#!/usr/bin/env python

import time
from mapnik import *

def print_features(fs):
    if hasattr(fs,'next'):
        feat = fs.next()
        while feat:
            print feat
            extent = Envelope()
            for i in range(feat.num_geometries()):
                geom = feat.get_geometry(i)
                if (extent.width() < 0 and extent.height() < 0):
                    extent = geom.envelope()
                extent.expand_to_include(geom.envelope())
            print extent
            print '-'*75
            feat = fs.next()
    else:
        # https://trac.mapnik.org/ticket/280
        for feat in fs:
            print feat.attributes.items()
            print feat.envelope()          

lyr = Layer('world')
lyr.datasource = Shapefile(file='../../data/tm_wgs84_sans_antarctica')
bbox = lyr.envelope()
resolution = 1.0

# set the extent of the datasource to query
query = Query(bbox,resolution)

# which field to display for each feature
query.add_property_name('NAME')

ds = lyr.datasource
# grab the features from the layers datasource
if hasattr(ds, 'all_features'):
    f_set =  ds.all_features()
else:
    f_set = ds.features(query)

print 'Querying all Features in %s... ' % lyr.name
time.sleep(2)
print_features(f_set)
