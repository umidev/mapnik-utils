# mapfile from string
cat tests/mapfile_wgs84.xml | nik2img.py /tmp/from_string.png

# worldfile registration
nik2img.py tests/mapfile_lambert.xml /tmp/lambert.png --world-file wld -d 2000 1500 --no-open
# open both in qgis
open tests/data/us_states_lambert.shp -a qgis
open /tmp/lambert.png -a qgis