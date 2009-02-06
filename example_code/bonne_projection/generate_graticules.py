# graticule_hack.py
# Credits to Sean Gillies and Matt Perry
# http://zcologia.com/news/16
#
import math
from osgeo import ogr

# Create an ESRI shapefile of parallels and meridians

filename = 'graticule.shp'
driver = ogr.GetDriverByName('ESRI Shapefile')
driver.DeleteDataSource(filename)
ds = driver.CreateDataSource(filename)
layer = ds.CreateLayer('graticule', geom_type=ogr.wkbLineString)
fd = ogr.FieldDefn('TYPE', ogr.OFTInteger)
fd.SetWidth(1)
fd.SetPrecision(0)
layer.CreateField(fd)
fd = ogr.FieldDefn('VALUE', ogr.OFTInteger)
fd.SetWidth(4)
fd.SetPrecision(0)
layer.CreateField(fd)
fd = ogr.FieldDefn('ABS_VALUE', ogr.OFTInteger)
fd.SetWidth(4)
fd.SetPrecision(0)
layer.CreateField(fd)

for j in range(1,18):
    y = 10*float(j-9)
    for i in range(0, 360):
        line = ogr.Geometry(type=ogr.wkbLineString)
        if i == 0:
            x1 = -179.9
            x2 = -179.0
        elif i == 359:
            x1 = 179.0
            x2 = 179.9
        else:
            x1 = float(i-180)
            x2 = x1 + 1.0
        line.AddPoint(x1, y)
        line.AddPoint(x2, y)
        f = ogr.Feature(feature_def=layer.GetLayerDefn())
        f.SetField(0, 0)
        f.SetField(1, y)
        f.SetField(2, math.fabs(y))
        f.SetGeometryDirectly(line)
        layer.CreateFeature(f)
        f.Destroy()

for i in range(0, 37):
    x = 10*float(i-18)
    if i == 0:
        x = -179.9
    if i == 36:
        x = 179.9
    for j in range(1, 180):
        line = ogr.Geometry(type=ogr.wkbLineString)
        y1 = float(j - 90)
        y2 = y1 + 1.0
        line.AddPoint(x, y1)
        line.AddPoint(x, y2)
        f = ogr.Feature(feature_def=layer.GetLayerDefn())
        f.SetField(0, 1)
        f.SetField(1, x)
        f.SetField(2, math.fabs(x))
        f.SetGeometryDirectly(line)
        layer.CreateFeature(f)
        f.Destroy()

ds.Destroy()