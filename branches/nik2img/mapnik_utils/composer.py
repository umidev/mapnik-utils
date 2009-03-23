#!/usr/bin/env python

import os
import mapnik
import platform
from renderer import Render
from mapfile import Load

# extend native mapnik objects
import metaclass_injectors

# bring 0.5.x series python bindings up to 0.6.x
if not hasattr(mapnik,'mapnik_version'):
    import compatibility 

class Compose(object):
    """
    """
    def __init__(self,mapfile,**kwargs):
        """
        """
        self.mapfile = mapfile

        self.image = None
        self.format = 'png'
        self.width = 600
        self.height = 400
        self.bbox = None
        self.zoom = None
        self.center = None
        self.radius = None
        self.zoom_to_layers = None
        #self.extent = None
        self.max_extent = None
        self.srs = None
        self.layers = None
        self.re_render_times = None
        self.post_step_pause = None
        self.trace = None
        self.max_resolution = None
        self.find_and_replace = None
        self.world_file = None
        self.fonts = None
        self.save_map = None
        self.app = None
        self.dry_run = False

        self.changed = []
        self.font_handler = None
        self.map = None
        self.verbose = False
        self.rendered = False
              
        if kwargs:
            self.handle_options(kwargs)

        self.prepare()
        self.setup()
        self.build()

    def handle_options(self,options):
        for opt in options.items():
            if opt[1] is not None and hasattr(self,opt[0]):
                setattr(self,opt[0],opt[1])
                self.changed.append(opt[0])

    def prepare(self):
        self.format = self.format.lower().replace('image/','')
        self.mime = 'image/%s' % self.format.replace('256','')
        if self.fonts:
            self.register_fonts(self.fonts)

    def setup(self):
        pass

    def output_error(msg, E=None):
        if E:
            msg = E
        raise sys.exit(msg)

    def msg(msg):
        sys.stderr.write('%s\n' % msg)

    def register_fonts(self,fonts):
        from fonts import FontHandler
        self.font_handler = FontHandler()
        self.font_handler.add_fonts(self.fonts)
        if self.font_handler.failed:
            self.mapsg("Failed to register: '%s'" % self.font_handler.failed)

    def build(self):
        loader = Load(self.mapfile)
        self.map = loader.build_map(self.width,self.height)

        if self.srs:
            self.map.set_easy_srs(self.srs)

        if self.layers:
            selected, disactivated = self.map.select_layers(self.layers)
            if not selected:
                self.output_error('Layer not found: available layers are: "%s"' % ', '.join(disactivated))
                
        if self.center or not self.zoom is None:
            if self.max_extent:
                self.map.zoom_to_box(mapnik.Envelope(*self.max_extent))
            else:
                self.map.zoom_max()

        if self.center and not self.zoom is None:
            self.map.set_center_and_zoom(self.center[0],self.center[1],self.zoom)
        elif self.center and self.radius:
            self.map.set_center_and_radius(self.center[0],self.center[1],self.radius)
        elif not self.zoom is None:
            self.map.zoom_to_level(self.zoom)
        elif self.zoom_to_layers:
            self.map.select_layers(self.zoom_to_layers)
            if len(self.zoom_to_layers) > 1:
                self.map.zoom_to_layers(self.zoom_to_layers)
            else:
                self.map.zoom_to_layer(self.zoom_to_layers)
        else:
            if self.max_extent:
                self.map.zoom_to_box(mapnik.Envelope(*self.max_extent))
            else:
                self.map.zoom_all()
          
        #if self.verbose:
        #    self.layers_in_extent(self.map)
  
    def render(self):
        if not self.map:
            self.build()
        
        if self.dry_run:
            self.output_error("Dry run complete")

        renderer = Render(self.map,self.image,self.format) #render_times/loops
        if self.world_file:
            renderer.world_file = self.world_file
        if self.save_map:
            renderer.save_map = self.save_map
        if self.image:
            renderer.render_file()
        else:
            renderer.print_stream()
        self.rendered = True

    def open(self, app=None):
        """
        Routine to open the rendered image or folder of images from the filesystem.
        """
        self.render()
        if not app and self.app:
            app = self.app
        try:
            if os.name == 'nt':
                if app:
                    self.mapsg('Overriding default image viewer not yet supported on Win32')
                os.system('start %s' % self.image.replace('/','\\'))
            elif platform.uname()[0] == 'Linux':
                if app:
                    os.system('%s %s' % (app, self.image))
            elif platform.uname()[0] == 'Darwin':
                if app:
                    os.system('open %s -a %s' % (self.image, app))
                else:
                    os.system('open %s' % self.image)
        except Exception, E:
            pass # this is fluf, so fail quietly if there is a problem