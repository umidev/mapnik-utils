import mapnik

try:
    spherical_merc = mapnik.Projection('+init=epsg:900913')
except: # you don't have 900913 in /usr/share/proj/epsg
    spherical_merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')

try:
    longlat = mapnik.Projection('+init=epsg:4326')
except: # your proj4 files are broken
    longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

from_srs,to_srs = longlat, spherical_merc

ct = mapnik.ProjTransform(from_srs,to_srs)


longlat_coords = mapnik.Coord(-180, 45)
merc_coords = ct.forward(longlat_coords)
print 'merc_coords:', merc_coords

longlat_coords = ct.backward(merc_coords)
print 'longlat_coords:',longlat_coords