#!/usr/bin/env python


# Example of reading geometry from a PostGIS table
# Add the sample data in quotes below to a database and then modify the default settings as needed

# Create and enter the database
"""
createdb -U postgres -T template_postgis mapnik
psql -U postgres mapnik

// Create the test geometry
DROP TABLE IF EXISTS polygon;
CREATE TABLE polygon (oid serial);
SELECT AddGeometryColumn( 'polygon', 'geometry', 4326, 'POLYGON', 2 );
INSERT INTO polygon (geometry)
SELECT ST_GeomFromEWKT('SRID=4326;POLYGON((100 0,101 0,101 1,100 1,100 0))') AS geometry;

"""

from mapnik import *

# Database settings
DBNAME = 'mapnik'
USER= 'postgres'
TABLE = 'polygon'
PASSWORD = ''
HOST = 'localhost'


m = Map(600,300,"+proj=latlong +datum=WGS84")
m.background = Color('transparent')

s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('green')))
r.symbols.append(LineSymbolizer(Color('darkorange'),2))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('shape')
lyr.datasource = PostGIS(host=HOST,user=USER,password=PASSWORD,dbname=DBNAME,table=TABLE)
lyr.styles.append('My Style')


# Buffer the same table to create a different background layer
s2 = Style()
r2=Rule()
r2.symbols.append(PolygonSymbolizer(Color('steelblue')))
r2.symbols.append(LineSymbolizer(Color('darkblue'),3))
s2.rules.append(r2)
m.append_style('My Style2',s2)
lyr2 = Layer('shape_buffer')
BUFFERED_TABLE = '(select ST_Buffer(geometry, 1) as geometry from %s) polygon' % TABLE
lyr2.datasource = PostGIS(host=HOST,user=USER,password=PASSWORD,dbname=DBNAME,table=BUFFERED_TABLE)
lyr2.styles.append('My Style2')

# Append the second, background layer first, since Mapnik uses the painter's model
m.layers.append(lyr2)
m.layers.append(lyr)

m.zoom_to_box(lyr2.envelope())
# We have to manually zoom out since the buffered layer's envelope is not properly read by Mapnik
m.zoom(-5)
render_to_file(m,'postgis_geometry.png')