from mapnik import *


def puff_bbox(bbox, unit):
    bbox.expand_to_include(bbox.minx-unit,bbox.miny-unit)
    bbox.expand_to_include(bbox.maxx+unit,bbox.maxy+unit)
    return bbox
    
m = Map(400,400)
load_map(m,"shield_symbolizer_test.xml")
bbox = Envelope(-175694.6612042082,6542691.745898315,-168424.6950525119,6549216.387789081)
m.zoom_to_box(bbox)
render_to_file(m,"shields-1.png","png256")
bbox = Envelope(-173480.9291230377,6544678.523934189,-170638.4271336824,6547229.609753206)

bbox = puff_bbox(bbox,1000)
m.zoom_to_box(bbox)
render_to_file(m,"shields-2.png","png256")

bbox = puff_bbox(bbox,-4000)
m.zoom_to_box(bbox)
render_to_file(m,"shields-3.png","png256")