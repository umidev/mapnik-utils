# note: requires mapnik SVN r822 or greater.

# Example of reprojecting the extent for the netherlands in epsg:28992 to google mercator and then back to the original netherlands extent.

import sys

try:
  from mapnik import ProjTransform, Projection, Envelope
except ImportError, E:
  sys.exit('Requires Mapnik SVN r822 or greater:\n%s' % E)

# http://spatialreference.org/ref/epsg/28992/
# http://mapnik.dbsgeo.com/days/2009-01-25
amersfoort_extent = Envelope(13599.999985,306799.999985,277999.999985,619299.999985)
amersfoort_proj = Projection('+init=epsg:28992')

merc_proj = Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs')

transform = ProjTransform(amersfoort_proj,merc_proj)

merc_extent = transform.forward(amersfoort_extent)
if transform.backward(merc_extent).__repr__() == amersfoort_extent.__repr__():
 print 'Transformation successful!'
 print 'Original Dutch Extent: %s' % amersfoort_extent
 print 'Merc Extent: %s' % merc_extent
else:
 print 'Reprojection failure...'