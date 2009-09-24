import timeit

# +over variant used by osm
gmerc_a = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'

# +wktext variant at sr.org - http://spatialreference.org/ref/user/6/proj4/
gmerc_b = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs'

# http://trac.openlayers.org/wiki/SphericalMercator
gmerc_c = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs'

srs = gmerc_c

epsg = '+init=epsg:900913'

seattle = [-13672902.7437, 6011007.9035, -13576897.8362, 6081177.0955]
nw_coast = [-14509582.4552, 5623319.2961, -12971057.9501, 6900123.4164]
north_pacific = [14362823.3609, 2935181.8857, -12308196.0409, 11721159.6637]
bbox = nw_coast

iterations = 1


t = timeit.Timer("map_tests.with_python_no_srs(%s)" % bbox,"import map_tests")
try:
    print '-'*70
    print "Pure python no srs:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()

t = timeit.Timer("map_tests.from_xml_no_srs(%s)" % bbox,"import map_tests")
try:
    print '-'*70
    print "Using load_map() no srs:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()

t = timeit.Timer('map_tests.with_python_gmerc_srs(%s,"%s")' % (bbox,srs),"import map_tests")
try:
    print '-'*70
    print "Pure python Google Mercator SRS:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()

t = timeit.Timer('map_tests.from_xml_gmerc_srs(%s,"%s")' % (bbox,srs),"import map_tests")
try:
    print '-'*70
    print "Using load_map() Google Mercator SRS:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()

# for these tests make sure to have:
# <900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over <>
# in your /usr/local/share/proj/epsg file

t = timeit.Timer('map_tests.with_python_epsg_init(%s,"%s")' % (bbox,epsg),"import map_tests")
try:
    print '-'*70
    print "Pure python Google Mercator epsg code:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()

t = timeit.Timer('map_tests.from_xml_gmerc_epsg_init(%s,"%s")' % (bbox,epsg),"import map_tests")
try:
    print '-'*70
    print "Using load_map() Google Mercator epsg code:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()
    
t = timeit.Timer('map_tests.with_python_epsg_init(%s,"%s")' % (bbox,'+init=epsg:32766'),"import map_tests")
try:
    print '-'*70
    print "Pure python with epsg code at the bottom of the epsg file:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()

t = timeit.Timer('map_tests.from_xml_32766_epsg_init(%s,"%s")' % (bbox,'+init=epsg:32766'),"import map_tests")
try:
    print '-'*70
    print "Using load_map() with epsg code at the bottom of the epsg file:", t.timeit(iterations), "sec"
    print '-'*70
except:
    t.print_exc()
        
    