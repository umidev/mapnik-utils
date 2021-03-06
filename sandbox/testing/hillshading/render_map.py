#!/usr/bin/env python

from mapnik import *

m = Map(400,400)
load_map(m,"hillshading_test.xml")
bbox = Envelope(-298300.666958,6446250.25958,-35624.9164577,6621367.42658)
m.zoom_to_box(bbox)
im = Image(m.width,m.height)
render(m,im)
im.save("hillshading.png","png256")

### getting the lat/lon from the Envelope:
#from mapnik import *
#env = Envelope(-175694.6612042082,6542691.745898315,-168424.6950525119,6549216.387789081)
#env.inverse(Projection('+proj=merc +datum=WGS84 +k=1.0 +units=m +over +no_defs'))
##Envelope(-1.57829199498,50.7420815096,-1.51298477789,50.7792570692)
### 'inverse' because we are going from a projected system to geographic/platte caree
