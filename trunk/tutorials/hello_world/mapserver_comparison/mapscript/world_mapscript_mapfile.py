#!/usr/bin/env python

# TODO - figure out how to add styles and layers in python...
# mapscript.styleObj
# mapscript.layerObj

from mapscript import mapObj, OWSRequest
m = mapObj('../mapfile_config/world.map')
e = m.extent
bbox = '%s,%s,%s,%s' % (e.minx,e.miny,e.maxx,e.maxy)
req = OWSRequest()
# The OWSRequest only wants strings...
req.setParameter("request", 'GetMap')
req.setParameter("bbox", bbox)
req.setParameter("width", '600')
req.setParameter("height", '300')
req.setParameter("srs", 'epsg:4326')
req.setParameter("format", 'image/png')
req.setParameter("layers", 'world')
m.loadOWSParameters(req)
image = m.draw()
image.save('world_mapscript_mapfile.png')
legend = m.drawLegend()
legend.save('world_mapscript_legend.png')
scalebar = m.drawScalebar()
scalebar.save('world_mapscript_scalebar.png')
sld = open('world_mapscipt_sld.xml','w')
sld.write(m.generateSLD())
sld.close()
# will save relative to mapfile by default
m.saveMapContext('../mapscript/world_mapscript_mapcontext.xml')