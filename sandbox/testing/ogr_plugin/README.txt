Tests against the new ogr input plugin in trunk.

Requires a Mapnik svn build.

Selected sample data was from here: http://svn.osgeo.org/gdal/trunk/autotest/ogr/data/

If you add more test data to the data folder it either needs 'poly,'line', or 'point' in the filename (for the script to guess at how to symbolize), or it will fall back to assuming a polygon type.

Hack the script to test different formats (by extension).
