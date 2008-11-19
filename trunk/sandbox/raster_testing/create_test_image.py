#!/usr/bin/env python

from osgeo import gdal
import numpy
from subprocess import call

tiff = 'world_black_tiff.tif'
tiff_wgs84 = 'world_black_tiff_wgs84.tif'
tiff_gmerc = 'world_black_tiff_gmercator.tif'
tiff_width = 14400
tiff_height = 7200

# Create new raster layer with 3 bands
raster = gdal.GetDriverByName('GTiff')
dst_ds = raster.Create(tiff,tiff_width,tiff_height,3,gdal.GDT_Byte)

# Create blank raster with fully opaque alpha band
zeros = numpy.zeros((tiff_height, tiff_width),numpy.uint8)
dst_ds.GetRasterBand(1).WriteArray(zeros)
dst_ds.GetRasterBand(2).WriteArray(zeros)
dst_ds.GetRasterBand(3).WriteArray(zeros)

# Assign projection and extents (geotransform)
project = 'gdal_translate -a_ullr -180 90 180 -90 -a_srs "EPSG:4326" %s %s' % (tiff,tiff_wgs84)
call(project,shell=True)

# Reproject to google mercator since mapnik cannot do this on the fly for raster data
reproject = 'gdalwarp -t_srs EPSG:900913 %s %s' % (tiff_wgs84,tiff_gmerc)
call(reproject,shell=True)