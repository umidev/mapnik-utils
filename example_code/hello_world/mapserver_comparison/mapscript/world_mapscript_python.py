#!/usr/bin/env python

# http://old-mapserver.gis.umn.edu/doc40/howto-mapscript-python_2.html
# http://trac.osgeo.org/mapserver/browser/trunk/mapserver/mapscript/ruby/examples/shp2img.rb

import mapscript

shapepath = '../../data/'
shapename = 'world_borders.shp'

shp = mapscript.shapefileObj(shapepath+shapename,-1)

m = mapscript.mapObj('')
m.shapepath = shapepath
m.height = 400
m.width = 600
m.extent = shp.bounds

shapetypes = {
	   mapscript.MS_SHAPEFILE_POINT:mapscript.MS_LAYER_POINT,
	   mapscript.MS_SHAPEFILE_ARC:mapscript.MS_LAYER_LINE,
	   mapscript.MS_SHAPEFILE_POLYGON:mapscript.MS_LAYER_POLYGON,
	   mapscript.MS_SHAPEFILE_MULTIPOINT:mapscript.MS_LAYER_LINE
	   }

layer = mapscript.layerObj(m)
layer.name = shapename
layer.type = shapetypes[shp.type]
layer.status = mapscript.MS_ON
layer.data = shapename

cls = mapscript.classObj(layer)
style = mapscript.styleObj()
color = mapscript.colorObj()
color.red = 242
color.green = 239
color.blue = 249
style.color = color
cls.insertStyle(style)

color = mapscript.colorObj()
color.red = 70
color.green = 130
color.blue = 80
m.imagecolor = color

image = m.draw()
image.save('world_mapscript_python.png')