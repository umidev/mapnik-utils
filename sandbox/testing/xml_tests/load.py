#!/usr/bin/env python

from mapnik import *
import os

m = Map(45,45)
m.background = Color('steelblue')
m.srs = 'joke'
load_map(m,'mapfile.xml',True)
#m.layers[0].maxzoom = 2
os.system('rm mapfile_out.xml')
save_map(m,'mapfile_out.xml')
os.system('open mapfile_out.xml -a bbedit')