#!/usr/bin/env python

import cairo
from mapnik import *

format = 'pdf'
filename = 'world.%s' % format

m = Map(600,400,'+proj=latlong +datum=WGS84')
load_map(m,'../../example_code/world_population/population.xml')

# remove text otherwise bus errors in libcairo.dylib...
m.remove_style('countries_label')
m.zoom_all()
m.zoom(.98)

formats = {'svg': cairo.SVGSurface,
                       'pdf':cairo.PDFSurface,
                       'ps':cairo.PSSurface,
                       }

file_output = open(filename, 'w')
surface = formats[format](file_output.name, m.width, m.height)
ctx = cairo.Context(surface)

render(m, ctx,10,10)

def cairo_color(c):
     ctx_c = (c.r/255.0,c.g/255.0,c.b/255.0,c.a/255.0)
     return ctx_c
    
def draw_title(m,ctx,text,size=10,color=Color('black')):
    w,h = m.width, m.height
    map_pts = [[0,0],[w,0],[w,h],[0,h]]
    ctx.select_font_face("DejaVu Sans Book",
                cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    x_bearing, y_bearing, width, height = ctx.text_extents(text)[:4]
    ctx.move_to(w/2 - width / 2 - x_bearing, 20.0 - height / 2 - y_bearing)
    ctx.show_text(text)
        
def draw_neatline(m,ctx,width=10,color=Color('black')):
    w,h = m.width, m.height
    map_pts = [[0,0],[w,0],[w,h],[0,h]]
    ctx.set_line_width(width)
    ctx.set_source_rgba(*cairo_color(color))
    ctx.move_to(*map_pts[-1])
    for pt in map_pts:
        ctx.line_to(*pt)
    ctx.close_path()
    ctx.stroke()

c = Color('darkred')
c.a = 250

draw_neatline(m,ctx,width=5,color=c)
draw_title(m,ctx,'Mapnik Map of the World!',size=15)
surface.finish()

import os
os.system('open %s' % filename)