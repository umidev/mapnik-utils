#!/usr/bin/env python

import cairo
import mapnik
import platform

surfaces = {'svg': cairo.SVGSurface,
           'pdf':cairo.PDFSurface,
           'ps':cairo.PSSurface,
           }
           
def cairo_color(c):
    """ Return a Cairo color tuple from a Mapnik Color."""
    ctx_c = (c.r/255.0,c.g/255.0,c.b/255.0,c.a/255.0)
    return ctx_c

class CairoMap(object):
    def __init__(self,mapnik_map,map_output):
        self.m = mapnik_map
        self.map_output = map_output
        self.surface = self.create_surface()

    def draw_title(self,text,size=10,color=mapnik.Color('black')):
        """ Draw a Map Title near the top of a page."""
        middle = self.m.width/2.0
        ctx = cairo.Context(self.surface)
        ctx.set_source_rgba(*cairo_color(color))
        ctx.select_font_face("DejaVu Sans Book", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(size)
        x_bearing, y_bearing, width, height = ctx.text_extents(text)[:4]
        ctx.move_to(middle - width / 2 - x_bearing, 20.0 - height / 2 - y_bearing)
        ctx.show_text(text)
    
    def draw_neatline(self,width=10,color=mapnik.Color('black')):
        ctx = cairo.Context(self.surface)
        w,h = self.m.width, self.m.height
        map_pts = [[0,0],[w,0],[w,h],[0,h]]
        ctx.set_line_width(width)
        ctx.set_source_rgba(*cairo_color(color))
        ctx.move_to(*map_pts[0])
        for pt in map_pts:
            ctx.line_to(*pt)
        ctx.close_path()
        ctx.stroke()

    def create_surface(self):
        self.format = self.map_output.split('.')[1]
        file_output = open(self.map_output, 'w')
        surface = surfaces[self.format](file_output.name, self.m.width, self.m.height)
        return surface
        
    def render(self):
        mapnik.render(m, cairo.Context(self.surface))
    
    def close(self):
        self.surface.finish()
    

if __name__ == '__main__':
    m = mapnik.Map(600,400)
    mapnik.load_map(m,'../../example_code/world_population/population.xml')
    out = 'world.svg'
    c_map = CairoMap(m,out)
    # zoom map...
    c_map.m.zoom_all()
    c_map.m.zoom(.98)
    # render map onto surface, leave active...
    c_map.render()
    # draw other items on top...
    border = mapnik.Color('black')
    c_map.draw_neatline(width=5,color=border)
    text = mapnik.Color('darkred')
    c_map.draw_title('Mapnik Map of the World',size=15,color=text)
    c_map.close()

    if platform.system() == 'Darwin':
        import os
        os.system('open %s' % out)
