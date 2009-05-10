# mapfile from string
cat tests/mapfile_wgs84.xml | nik2img.py /tmp/from_string.png

# redirect image stream
nik2img.py tests/mapfile_wgs84.xml > /tmp/image_stream.png
open /tmp/image_stream.png

# redirect image jpeg stream
nik2img.py tests/mapfile_wgs84.xml -f jpeg > /tmp/image_stream.jpeg
open /tmp/image_stream.jpeg

# worldfile registration
nik2img.py tests/mapfile_lambert.xml /tmp/lambert.png --world-file wld -d 2000 1500 --no-open
# open both in qgis
open tests/data/us_states_lambert.shp -a qgis
open /tmp/lambert.png -a qgis

# zoom to extent using long/lat bbox
nik2img.py tests/mapfile_wgs84.xml --bbox -130 26 -60 50 /tmp/map-latlong1.png

# zoom to extent in coordinates of map
# same as above because map srs is Long/Lat(WGS84)...
nik2img.py tests/mapfile_wgs84.xml -e -130 26 -60 50 /tmp/map-latlong2.png

# zoom to extent in coordinates of reprojected map (in google merc)
nik2img.py tests/mapfile_wgs84.xml --srs 900913 -e -14471533.8031 2125223.60707 -6679169.4476 7320133.17742 /tmp/map-mercator1.png

# zoom to extent using long/lat bbox but still reproject to mercator
nik2img.py tests/mapfile_wgs84.xml --srs 900913 --bbox -130 26 -60 50 /tmp/map-mercator2.png

# let nik2img zoom to extent of data and reproject to mercator
nik2img.py tests/mapfile_wgs84.xml --srs 900913 /tmp/map-mercator-full.png

# zoom to bounding box of california
nik2img.py tests/mapfile_wgs84.xml --bbox -125.5 31.7 -113.3 42.6 -d 500 500 /tmp/cali.png

# zoom to san jose
nik2img.py tests/mapfile_wgs84.xml --bbox -121.945 37.312 -121.886 37.355 -d 500 500 /tmp/san_jose.png