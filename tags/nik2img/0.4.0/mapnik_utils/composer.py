import os
import sys
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
        self.extent = None
        self.max_extent = None
        self.bbox_factor = None
        self.srs = None
        self.layers = None
        self.re_render_times = None
        self.post_step_pause = None
        self.max_resolution = None
        self.find_and_replace = None
        self.world_file = None
        self.fonts = []
        self.save_xml = None
        self.app = None
        self.dry_run = False
        self.from_string = False
        
        self.changed = []
        self.font_handler = None
        self.map = None
        self.rendered = False
        self.verbose = False
        
        self.start_time = 0
        self.load_map_time = 0
        
        if kwargs:
            self.handle_options(kwargs)

        if not self.verbose:
            self.msg = self.quiet
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
            self.register_fonts()

    def setup(self):
        pass

    def output_error(self, msg, E=None):
        if E:
            msg += E
        raise sys.exit(msg)

    def msg(self, msg, warn=False):
        sys.stderr.write('%s\n' % msg)

    def quiet(self, msg):
        pass

    def register_fonts(self):
        self.msg('Registering fonts...')
        from fonts import FontHandler
        self.font_handler = FontHandler()
        self.font_handler.add_fonts(self.fonts)
        if self.font_handler.failed:
            self.msg("Failed to register: '%s'" % self.font_handler.failed)

    def build(self):
        self.msg('Loading mapfile...')
        
        builder = Load(self.mapfile,variables={},from_string=self.from_string)
        if not self.from_string:
            self.msg('Loaded %s...' % self.mapfile)
        else:
            self.msg('Loaded XML from string')
        self.map = builder.build_map(self.width,self.height)

        if self.srs:
            self.msg('Setting srs to: %s' % self.srs)
            self.map.set_easy_srs(self.srs)

        if self.layers:
            selected, disactivated = self.map.select_layers(self.layers)
            self.msg('Selected layers: %s' % selected)
            if not selected:
                self.output_error('Layer not found: available layers are: "%s"' % ',  '.join(disactivated))
                
        # handle shifts in pixel dimensions or bbox ratio
        # need to make as an option
        #try:
        #    self.map.aspect_fix_mode = mapnik.aspect_fix_mode.ADJUST_CANVAS_HEIGHT
        #except:
        #    self.msg('aspect_fix_mode not available!')

        
        # zoom to max extent at beginning if we later need to 
        # zoom to a center point
        # or need to zoom to a zoom-level
        self.msg('Setting Map view...')
        if self.center or not self.zoom is None:
            if self.max_extent:
                self.msg('Zooming to max extent: %s' % self.max_extent) 
                self.map.zoom_to_box(mapnik.Envelope(*self.max_extent))
            else:
                self.map.zoom_max()
                self.msg('Zoomed to *estimated* max extent: %s' % self.map.envelope()) 

        if self.center and not self.zoom is None:
            self.msg('Zooming to Center (%s) and Zoom Level "%s"' % (self.center,self.zoom))
            self.map.set_center_and_zoom(self.center[0],self.center[1],self.zoom)
        elif self.center and self.radius:
            self.msg('Zooming to Center (%s) and Radius "%s"' % (self.center,self.radius))
            self.map.set_center_and_radius(self.center[0],self.center[1],self.radius)
        elif not self.zoom is None:
            self.msg('Zooming to Zoom Level "%s"' % (self.zoom))
            self.map.zoom_to_level(self.zoom)
        elif self.zoom_to_layers:
            self.msg('Zooming to Layers: "%s"' % (self.zoom_to_layers))
            self.map.activate_layers(self.zoom_to_layers)
            if len(self.zoom_to_layers) > 1:
                self.map.zoom_to_layers(self.zoom_to_layers)
            else:
                self.map.zoom_to_layer(self.zoom_to_layers[0])
        else:
            if self.extent:
                env = mapnik.Envelope(*self.extent)
                self.msg('Zooming to custom projected extent: "%s"' % env)
                self.map.zoom_to_box(env)
                from_prj = mapnik.Projection(self.map.srs)
                to_prj = mapnik.Projection('+proj=latlong +datum=WGS84')
                bbox = env.transform(from_prj,to_prj)
                self.msg('Custom extent in geographic coordinates: "%s"' % bbox)
            elif self.bbox:
                env = mapnik.Envelope(*self.bbox)
                self.msg('Zooming to custom geographic extent: "%s"' % env)
                from_prj = mapnik.Projection('+proj=latlong +datum=WGS84')
                to_prj = mapnik.Projection(self.map.srs)
                self.map.zoom_to_box(env.transform(from_prj,to_prj))
            else:
                self.map.zoom_all()
                self.msg('Zoom to extent of all layers: "%s"' % self.map.envelope())
        
        if self.bbox_factor:
            if self.bbox_factor > 0:
                bbox = self.map.envelope() * self.bbox_factor
            else:
                bbox = self.map.envelope() / self.bbox_factor
            self.map.zoom_to_box(bbox)
            self.msg('Adjusting final extent by factor of %s: "%s"' % (self.bbox_factor,self.map.envelope()))
            
        self.msg('Finished setting extents...')
        
        if self.save_xml:
            mapnik.save_map(self.map,self.save_xml)
        
        return builder

 
    def render(self):
        if not self.map:
            self.build()
        
        if self.dry_run:
            self.output_error("Dry run completed successfully...")            

        renderer = Render(self.map,self.image,self.format,self.world_file)
        if self.image:
            renderer.render_file()
        else:
            renderer.print_stream()
        self.rendered = True
        return renderer

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
                    self.msg('Overriding default image viewer not yet supported on Win32')
                os.system('start %s' % self.image.replace('/','\\'))
            elif platform.uname()[0] == 'Linux':
                if app:
                    os.system('%s %s' % (app, self.image))
            elif platform.uname()[0] == 'Darwin':
                if app:
                    os.system('open %s -a %s' % (self.image, app))
                else:
                    os.system('open %s' % self.image)
        except Exception:
            pass # this is fluf, so fail quietly if there is a problem