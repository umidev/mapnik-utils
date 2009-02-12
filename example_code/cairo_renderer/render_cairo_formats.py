#!/usr/bin/env python

import cairo
from mapnik import *

map_output = 'world'
m = Map(256,256,'+proj=latlong +datum=WGS84')

m.background = Color('steelblue')
s = Style()
r=Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
s.rules.append(r)
m.append_style('My Style',s)
lyr = Layer('world')
lyr.datasource = Shapefile(file='../../data/world_borders')
lyr.styles.append('My Style')
m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())
m.zoom(.2)

file_formats = {'svg': cairo.SVGSurface,
                       'pdf':cairo.PDFSurface,
                       'ps':cairo.PSSurface,
                       }

for format in file_formats:
    print '// --  Rendering %s -----------------------------' % format
    file = open('%s.%s' % (map_output, format), 'w')
    surface = file_formats[format](file.name, m.width, m.height)
    render(m, surface)
    surface.finish()

image_formats = {'FORMAT_A1': cairo.FORMAT_A1,
                            'FORMAT_A8': cairo.FORMAT_A8,
                            'FORMAT_ARGB32': cairo.FORMAT_ARGB32,
                            #'FORMAT_RGB16_565': cairo.FORMAT_RGB16_565,
                            'FORMAT_RGB24': cairo.FORMAT_RGB24,
                            }

for format in image_formats:
    print '// --  Rendering %s -----------------------------' % format
    surface = cairo.ImageSurface(image_formats[format], m.width, m.height)
    render(m, surface)
    surface.write_to_png('%s_%s.png' % (map_output, format))
    surface.finish()