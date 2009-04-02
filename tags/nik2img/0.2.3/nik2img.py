#!/usr/bin/env python

__author__ = "Dane Springmeyer (dbsgeo [ -a- ] gmail.com)"
__copyright__ = "Copyright 2008, Dane Springmeyer"
__version__ = "0.2.3"
__license__ = "GPLv2"

import os
import sys
import getopt
import re
import tempfile
import platform
from timeit import time

try:
    import mapnik
    HAS_MAPNIK_PYTHON = True
    if not hasattr(mapnik,'mapnik_version'):
        PRE_6_SERIES = True
    else:
        PRE_6_SERIES = False
        from mapnik import ProjTransform
except ImportError, E:
    HAS_MAPNIK_PYTHON = False
    PRE_6_SERIES = False
    print
    print "WARNING: Mapnik's python bindings not found..."
    print E

try:
    import cairo
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False

no_color_global = False

MERC_PROJ4 = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'

class Nik2imgError(Exception): pass

if PRE_6_SERIES:

    BoostPythonMetaclass = mapnik.Coord.__class__
    
    class _injector(object):
        class __metaclass__(BoostPythonMetaclass):
            def __init__(self, name, bases, dict):
                for b in bases:
                    if type(b) not in (self, type):
                        for k,v in dict.items():
                            setattr(b,k,v)
                return type.__init__(self, name, bases, dict)

    class ProjTransform(object):
        def __init__(self,*args):
            try:
                output_error("Only Mapnik version 0.6.0 or > supports transformations: see http://trac.mapnik.org/ticket/117")
            except: pass
        
        def forward(self,bbox):
            return bbox
            
        def backward(self,bbox):
            return bbox

    class _Map(mapnik.Map,_injector):

        @property
        def scale_denominator(self):
            srs = mapnik.Projection(self.srs)
            return mapnik.scale_denominator(self,srs.geographic)

    class _Coord(mapnik.Coord,_injector):
        def forward(self,obj):
            return mapnik.forward_(self,obj)
        def inverse(self,obj):
            return mapnik.inverse_(self,obj)

    class _Envelope(mapnik.Envelope,_injector):
        def forward(self,obj):
            return mapnik.forward_(self,obj)
        def inverse(self,obj):
            return mapnik.inverse_(self,obj)

def is_int(str):
    """
    Test if a given string is an integer.
    """
    if str == None:
        return False
    try:
        int(str)
    except ValueError:
        return False
    return True
    
def pause_for(sec):
    """
    Pauses script execution for n seconds using the timeit.time.sleep module.
    """
    if is_int(sec):
        for second in range(1, (int(sec)+1)):
            print color_text(5,second),
            time.sleep(1)
            sys.stdout.flush()
    else:
        output_error("Time in seconds must be integer value")

def make_line(character, n):
    line = character*n
    return line

def color_print(color, text):
    """
    Accepts an integer key for one of several color choices along with the text string to color
      keys = 1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    Prints a colored string of text.
    """
    if not os.name == 'nt' and not no_color_global:
        print "\033[9%sm%s\033[0m" % (color,text)
    else:
        print text

def color_text(color, text):
    """
    Accepts an integer key for one of several color choices along with the text string to color
      keys = 1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    Returns a colored string of text.
    """
    if not os.name == 'nt' and not no_color_global:
        return "\033[9%sm%s\033[0m" % (color,text)
    else:
        return text

# Win32 workaround graciously provided by crschmidt
# from http://svn.tilecache.org/trunk/tilecache/TileCache/Service.py
def binaryPrint(binary_data):
    """This function is designed to work around the fact that Python
       in Windows does not handle binary output correctly. This function
       will set the output to binary, and then write to stdout directly
       rather than using print."""
    try:
        import msvcrt
        msvcrt.setmode(sys.__stdout__.fileno(), os.O_BINARY)
    except:
        pass
    sys.stdout.write(binary_data)

def output_error(msg, E=None, yield_usage=False):
    """
    Prints an error message to stdout, including a Traceback
    error if given (E), and command line usage if requested.
    """
    if __name__ == "__main__": 
        if yield_usage:
            usage(sys.argv[0])
        if E:
            color_print(1, '// --> %s: \n\n %s' % (msg, E))
        else:
            color_print(1, '\\ --> %s' % msg)
        sys.exit(1)
    else:
        if E:
            error = color_text(1, '// --> %s: \n\n %s' % (msg, E))
        else:
            error = color_text(1, '\\ --> %s' % msg)
        raise Nik2imgError(error)

class Map(object):
    """ The Map class instantiates a Mapnik map graphic with a path to an xml or mml mapfile.
         
        But it also accepts a variety of keyword arguments to customize output.
        
        After creating a Map class either call open() to open the image from the filesystem
        using the default image reader or call stream() to print the image to STDOUT. 
        
        Required argument:
        --> mapfile\t string\t path to a mapnik xml or cascadenik mml file
        
        Optional **kwargs:
        --> See the commandline usage
        
        Basic example usage:

        To save a image to the filesystem and open it with the default viewer:
        >>> from nik2img import Map
        >>> file = Map('/path/to/mapfile.xml','map.png')
        >>> file.open()
        
        To stream an image to a web browser:
        >>> from nik2img import Map
        >>> nikmap = Map('/path/to/mapfile.xml',width=256,height=256)
        >>> image = nikmap.stream()
        >>> print "Content-Type: %s" % nikmap.mime
        >>> print "Content-Length: %d" % len(image)
        >>> print '' 
        >>> print image
    """
    def __init__(self, mapfile, image='', width=600, height=400, format='png', bbox_geographic=None, bbox_projected=None, zoom_to=None, zoom_to_radius=None, zoom_to_layer=None, expand=None, srs=None, layers=None, re_render_times=None, post_map_pause=None, post_step_pause=None, trace_steps=None, levels=None, resolutions=None, max_resolution=None, find_and_replace=None, no_color=False, quiet=False, dry_run=False, verbose=False, debug=False, world_file=None, fonts=None, save_map=False,app=None):
        """Initialize the Map() class with the path to a mapfile.
        
        See the commandline usage for optional keyword arguments.
        """
        # Required
        self.mapfile = mapfile
        self.image = image
        
        # Defaults
        self.format = format
        if not self.format:
            self.format = 'png'
        self.width = width
        self.height = height
        
        # Optional arguments
        self.bbox_geographic = bbox_geographic
        self.bbox_projected = bbox_projected
        self.zoom_to = zoom_to
        self.zoom_to_radius = zoom_to_radius
        self.zoom_to_layer = zoom_to_layer
        self.expand = expand
        self.srs = srs
        self.layers = layers
        self.re_render_times = re_render_times
        self.post_map_pause = post_map_pause
        self.post_step_pause = post_step_pause
        self.trace_steps = trace_steps
        self.levels = levels
        self.resolutions = resolutions
        self.max_resolution = max_resolution
        self.find_and_replace = find_and_replace
        self.no_color = no_color      
        self.quiet = quiet
        self.dry_run = dry_run
        self.verbose = verbose
        self.debug = debug
        self.world_file = world_file
        self.mime = None
        self.fonts = fonts
        self.save_map = save_map
        self.app = app
         
        # Non argument class attributes
        self.TIMING_STARTED = False
        self.STEP = 0
        self.MAPFILE_TYPES = {'xml':'XML mapfile','mml':'Cascadenik Cascading Stylesheet', 'py':'Python Styles'}
        self.M_TYPE = None
        self.ALL_FORMATS = {}
        self.AGG_FORMATS = {'png':'png','png256':'png','jpeg':'jpg'}
        self.ALL_FORMATS.update(self.AGG_FORMATS)
        self.CAIRO_FILE_FORMATS = {'svg':'svg','pdf':'pdf','ps':'ps'}
        self.ALL_FORMATS.update(self.CAIRO_FILE_FORMATS)
        self.CAIRO_IMAGE_FORMATS = {'ARGB32':'png','RGB24':'png'}
        self.ALL_FORMATS.update(self.CAIRO_IMAGE_FORMATS)
        self.START = None
        self.TESTS_RUN = False
        self.BUILT = False
        self.RENDERED = False
        
        self.mapnik_map = None
        self.m_bbox = None

    def output_message(self,msg, warning=False, print_time=True):
        """
        Output a colored message or warning, incrementing the STEP counter
        to enable a pdb trace to be set at any point a verbose message is printed.
        """
        if warning and self.verbose:
            color_print(1, 'STEP: %s | --> WARNING: %s' % (self.STEP, msg)) 
        elif self.verbose:      
            color_print(2, 'STEP: %s // --> %s' % (self.STEP, msg))
            self.output_time(print_time)
        if self.post_step_pause:
            pause_for(self.post_step_pause)
        if self.trace_steps:
            if self.STEP in self.trace_steps:
              self.set_trace()
        self.STEP += 1

    def get_time(self, time):
        """
        Get the time and either seconds or minutes format.
        """
        if time/60 < 1:
            seconds = '%s seconds' % str(time)
            return seconds
        else:
            minutes = '%s minutes' % str(time/60)
            return minutes
    
    def elapsed(self, last_step):
        """
        Return the full and incremental elasped time.
        """
        total = (time.time() - self.START)
        last = (time.time() - last_step)
        return 'Total time: %s | Last step: %s' % (self.get_time(round(total,4)), self.get_time(round(last,8)))
    
    def output_time(self, print_time):
        """
        Timing output wrapper to control the start point and verbosity of timing output.
        """
        if self.TIMING_STARTED and print_time:
            color_print(4,self.elapsed(time.time()))
    
    def set_trace(self):
        """
        Routine to set a Python Debugger trace.
        """
        try:
            print ">>> Entering PDB interpreter (press 'c' to leave)"
            #print '>>> Print out current mapnik object names? (yes or no)'
            #response = raw_input()
            #if response == 'yes':
                #if self.mapnik_objects:
                #    color_print(1,'Mapnik objects: %s' % ', '.join(self.mapnik_objects))
            #else:
            #    color_print(1,'No mapnik objects available in namespace yet...')
            import pdb
            pdb.set_trace()
        except KeyboardInterrupt:
            pass
 
    def generate_levels(self,N=10):
        """
        Accepts a number of zoom levels and returns a list of zoom resolutions.
        """
        max_res = 360.0/int(self.width)

        if not self.max_resolution:
            if self.mapnik_map:
                max_res = self.mapnik_map.envelope().width()/int(self.width)

        levels = [max_res / 2 ** i for i in range(int(N))]        
        return levels

    def zoom_max(self):
        # todo: allow user determined max_extent
        e = mapnik.Envelope(-179.99999694572804,-85.0511285163245,179.99999694572804,85.0511287798066)
        p = mapnik.Projection('%s' % self.mapnik_map.srs)
        e = e.forward(p)
        self.mapnik_map.zoom_to_box(e)

    def load_pymap(self,path):
        """
        Instanciate a Mapnik Map object from an external python script.
        """
        py_path = os.path.dirname(path)
         
        sys.path.append(py_path)
        py_module = os.path.basename(path).split('.')[0]
        module = __import__(py_module)
        py_map = getattr(module,'m')
        if not py_map:
            output_error("Could not find variable named 'm' in python module for loading map object.")
        return py_map
        
    def mapfile_validate(self, m):
        """
        Routine to check for the existance of each datasource
        specified for the layers of a mapfile xml.
        """
        for layer in m.layers:
            if not layer.datasource:
                self.output_message("Datasource not found for layer '%s' -  Hint: check permissions and if using a shapefile remove the .shp ext" % layer.name, warning=True)
            else:
                self.output_message("Datasource successfully found for layer '%s'" % layer.name)

    def get_mapfile_type(self,m):
        if m.endswith('xml'):
            return self.MAPFILE_TYPES['xml']
        elif m.endswith('mml'):
            return self.MAPFILE_TYPES['mml']
        elif self.mapfile.endswith('py'):
            return self.MAPFILE_TYPES['py']
        else:
            return None
        
    def layers_in_extent(self, m):
        """
        Routine to validate which layers intersect the current map extent.
        """
        mapfile_layers = m.layers
        map_envelope = m.envelope()
        for layer_num in range(len(m.layers)-1, -1, -1):
            check_intersects = True
            l = mapfile_layers[layer_num]
            layer_bbox = l.envelope()
            layer_p = mapnik.Projection("%s" % l.srs)
            map_p = mapnik.Projection("%s" % self.mapnik_map.srs)            
            if map_p.geographic and layer_p.geographic:
                pass # no need to reproject layer envelope
            elif not map_p.geographic and layer_p.geographic:
                layer_bbox = layer_bbox.forward(map_p) # project/forward the layers envelope
            elif map_p.geographic and not layer_p.geographic:
                layer_bbox = layer_bbox.inverse(layer_p) # invert the layers envelope
            elif not map_p.geographic and not layer_p.geographic:
                if layer_p.params() == map_p.params():
                    pass # no need to reproject layer envelope
                else:
                    # set up a proj4 transform as (from,to)
                    # we need to project the layer bbox to a new layer bbox that matches the map bbox
                    # so we go from -> to (forward)
                    transform = ProjTransform(layer_p,map_p)
                    layer_bbox = transform.forward(layer_bbox)
            if check_intersects:
                if layer_bbox.intersects(map_envelope):
                    self.output_message("Layer '%s' intersects Map envelope" % l.name,print_time=False)
                    self.output_message("Layer envelope was: %s  |  Map envelope is %s" % (layer_bbox, map_envelope),print_time=False)
                    self.output_message("Center point of layer '%s' is %s" % (l.name, layer_bbox.center()),print_time=False)
                    self.output_message("Layer's minzoom = '%s' and maxzoom = '%s'"  % (l.minzoom, l.maxzoom) )
                    if l.visible(self.mapnik_map.scale()):
                        self.output_message("At current scale of '%s': this layer '%s' is visible" % (self.mapnik_map.scale(),l.name))
                    else:
                        self.output_message("At current scale of '%s': this layer '%s' NOT visible" % (self.mapnik_map.scale(),l.name),warning=True)
                    for sty_name in l.styles:
                        try:
                            sty_obj = self.mapnik_map.find_style(sty_name)
                        except KeyError, E:
                            output_error("Could not find style '%s':\n%s" % (sty_name, E))
                        for rule in sty_obj.rules:
                            if rule.active(self.mapnik_map.scale()):
                                self.output_message("ACTIVE: %s:%s... --> Max scale: '%s' | Min scale: '%s'" % (sty_name,str(rule.filter)[:10],rule.max_scale, rule.min_scale))
                            else:
                                self.output_message("NOT ACTIVE: %s:%s... --> Max scale: '%s' | Min scale: '%s'" % (sty_name,str(rule.filter)[:10],rule.max_scale, rule.min_scale),warning=True)                    
                else:
                    self.output_message("Layer '%s' does not intersect with Map envelope" % l.name, warning=True,print_time=False)
                    self.output_message("Layer envelope was: %s  |  Map envelope is %s" % (layer_bbox, map_envelope), warning=True)

    def get_layer_extent_and_srs(self, m, layer_name):
        """
        Fetch the extent for a given layer by name.
        """
        layer_obj = [l for l in m.layers if l.name.lower() == layer_name.lower()]
        if layer_obj:
            return layer_obj[0].envelope(), layer_obj[0].srs
        else:
            layers = ', '.join([l.name for l in m.layers])
            output_error("Could not find a layer named '%s', in these map layers: %s" % (layer_name, layers))
        

    def expand_bbox(self, bbox, delta):
        """
        Expand the bbox by a given radius in map units.
        """
        bbox.expand_to_include(bbox.minx-delta, bbox.miny-delta)
        bbox.expand_to_include(bbox.maxx+delta, bbox.maxy+delta)
        #bbox = mapnik.Envelope(bbox.minx - delta, bbox.miny + delta, bbox.maxx - delta, bbox.maxy + delta)
        return bbox

    def local_render_wrapper(self,*args):
        """
        Abstraction wrapper for calling for map images rendered with either AGG or Cairo.
        """
        if args[2] in self.CAIRO_FILE_FORMATS:
            self.render_cairo(*args)
        # todo: support rendering to image formats with cairo
        #elif args[2] in self.CAIRO_IMAGE_FORMATS:
            #self.render_cairo(*args)
        elif args[2] in self.AGG_FORMATS:
            self.render_agg(*args)

    def write_world_file(self, path, x_rotation=0.0, y_rotation=0.0):
        """
        Outputs an ESRI world file that can be used to load the resulting
        image as a georeferenced raster in a variety of gis viewers.
        
        '.wld' is the most common extension used, but format-specific extensions
        are also looked for by some software, such as '.tfw' for tiff and '.pgw' for png
        
        A world file file is a plain ASCII text file consisting of six values separated
        by newlines. The format is: 
            pixel X size
            rotation about the Y axis (usually 0.0)
            rotation about the X axis (usually 0.0)
            pixel Y size (negative when using North-Up data)
            X coordinate of upper left pixel center
            Y coordinate of upper left pixel center
         
        Info from: http://gdal.osgeo.org/frmt_various.html#WLD
        """
        extent= self.mapnik_map.envelope()
        USE_PIXEL_SIZE = True
        USE_FLOATS = True
        if USE_PIXEL_SIZE:
            pixel_x_size = (extent.maxx - extent.minx)/self.mapnik_map.width
            pixel_y_size = (extent.maxy - extent.miny)/self.mapnik_map.height
            upper_left_x_center = extent.minx + 0.5 * pixel_x_size + 0.5 * x_rotation
            upper_left_y_center = extent.maxy + 0.5 * (-1*pixel_y_size) + 0.5 * y_rotation
            #upper_left_x_center = extent.minx+(pixel_x_size/2.0)
            #upper_left_y_center = extent.maxy-(pixel_y_size/2.0)
            if USE_FLOATS:
                # http://trac.osgeo.org/gdal/browser/trunk/gdal/gcore/gdal_misc.cpp#L1296
                wld_string = '''%.10f\n%.10f\n%.10f\n-%.10f\n%.10f\n%.10f\n''' % (
                    pixel_x_size, # geotransform[1] - width of pixel
                    y_rotation, # geotransform[4] - rotational coefficient, zero for north up images.
                    x_rotation, # geotransform[2] - rotational coefficient, zero for north up images.
                    pixel_y_size, # geotransform[5] - height of pixel (but negative)
                    upper_left_x_center, # geotransform[0] - x offset to center of top left pixel
                    upper_left_y_center # geotransform[3] - y offset to center of top left pixel.
                )
            else:
                wld_string = '''%s\n%s\n%s\n-%s\n%s\n%s\n''' % (pixel_x_size,y_rotation,x_rotation,pixel_y_size,upper_left_x_center,upper_left_y_center)
        else:
            scale = self.mapnik_map.scale()        
            upper_left_x_center = extent.minx-(scale/2.0)
            upper_left_y_center = extent.maxy-(scale/2.0)
            wld_string = '''%s\n%s\n%s\n-%s\n%s\n%s\n''' % (scale,y_rotation,x_rotation,scale,upper_left_x_center,upper_left_y_center)
        basename = path.split('.')[0]
        f_ptr = '%s.%s' % (basename, self.world_file)
        wld_file = open(f_ptr, 'w')
        wld_file.write(wld_string)
        wld_file.close()
        self.output_message('World file output written to %s:' % (f_ptr))

    def render_cairo(self,*args):
        """
        Routine to render the requested Cairo format.
        """
        if not HAS_CAIRO:
            output_error('PyCairo is not installed or available, therefore you cannot write to svg, pdf, ps, or cairo-rendered png')
        else:
            context = [args[1], self.mapnik_map.width, self.mapnik_map.height]
            if args[2] == 'svg':
                surface = cairo.SVGSurface(*context)
            elif args[2] == 'pdf':
                surface = cairo.PDFSurface(*context)
            elif args[2] == 'ps':
                surface = cairo.PSSurface(*context)
            elif args[2] == 'ARGB32':
                surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *context[1:])
            elif args[2] == 'RGB24':
                surface = cairo.ImageSurface(cairo.FORMAT_RGB24, *context[1:])
            if self.re_render_times:
                for n in range(1, int(self.re_render_times)):
                    mapnik.render(args[0],surface)
                    if args[2] in self.CAIRO_IMAGE_FORMATS:
                        surface.write_to_png(args[1])
                surface.finish()
                self.output_message("Map rendered to '%s', %s times" % (args[1], n))
            else:
                mapnik.render(args[0],surface)
                if args[2] in self.CAIRO_IMAGE_FORMATS:
                    surface.write_to_png(args[1])
                surface.finish()
                self.output_message("Map rendered to '%s'" % args[1])
            if self.world_file:
                self.write_world_file(args[1])
            if self.save_map:
                mapnik.save_map(self.mapnik_map,self.save_map)

    def call_CAIRO_FORMATS(self, basename):
        """
        Abstraction wrapper to allow for the same call
        to any image and file formats requested from Cairo.
        """
        if not HAS_CAIRO:
            output_error('PyCairo is not installed or available, therefore you cannot write to svg, pdf, ps, or cairo-rendered png')
        else:
            for k, v in self.CAIRO_FILE_FORMATS.iteritems():
                path = '%s_%s.%s' % (basename,k,v)
                self.render_cairo(self.mapnik_map,path,k)
            for k, v in self.CAIRO_IMAGE_FORMATS.iteritems():
                path = '%s_%s.%s' % (basename,k,v)
                self.render_cairo(self.mapnik_map,path,k)

    def render_agg(self,*args):
        """
        Routine to render the requested AGG format.
        """
        if self.re_render_times:
            for n in range(1, int(self.re_render_times)):
                mapnik.render_to_file(*args)
                self.output_message("Map rendered to '%s', %s times" % (args[1], n))
        else:
            mapnik.render_to_file(*args)
            self.output_message("Map rendered to '%s'" % args[1])
        if self.world_file:
            self.write_world_file(args[1])
        if self.save_map:
            mapnik.save_map(self.mapnik_map,self.save_map)

    def call_AGG_FORMATS(self, basename):
        """
        Abstraction wrapper to allow for calling 
        any requested AGG Formats.
        """
        for k, v in self.AGG_FORMATS.iteritems():
            path = '%s_%s.%s' % (basename,k,v)
            self.render_agg(self.mapnik_map,path,k)


    # ==============================================
    # Tests of variable inputs, run once from build(), but can be called separately
    # ==============================================

    def test(self, verbose=False):
        """
        Routine to do some basic tests and set default values.
        Can be run indepedently or will be automatically called during build()
        """
        if verbose:
            self.verbose = True
        
        if not HAS_MAPNIK_PYTHON:
            output_error("Error: 'import mapnik' failed - confirm that mapnik is installed and in your PYTHONPATH.")
        
        self.format = self.format.lower().replace('image/','')
        self.mime = 'image/%s' % self.format.replace('256','')
        
        if self.fonts:
            self.fonts = self.fonts.split(',')  
            engine = mapnik.FontEngine.instance()
            for font in self.fonts:
                if engine.register_font(font):
                    self.output_message("'%s' registered successfully" % font)
                else:
                    self.output_message("'%s' not found or able to be registered, try placing font in: '%s'" % (font,mapnik.paths.fontscollectionpath),warning=True)
                    self.output_message("Available fonts are: [%s]" % ', '.join([f for f in mapnik.FontEngine.face_names()]),warning=True)
        
        self.ZOOM_LEVELS = self.generate_levels(10)
        
        if is_int(self.width):
            self.width = int(self.width)
        else:
            print self.width.__repr__
            output_error("Width must be an integer")
        
        if is_int(self.height):
            self.height = int(self.height)
        else:
            output_error("Height must be an integer")
        
        if self.trace_steps:
            self.trace_steps = [int(step) for step in self.trace_steps.split(",")]
        if self.no_color:
            global no_color_global
            no_color_global = True
        
        if self.levels and not self.debug:
            self.debug = True
        
        if self.resolutions and not self.debug:
            self.debug = True
        
        if self.trace_steps and not self.verbose:
            self.verbose = True
            self.output_message('PDB trace requested, automatically entering verbose mode')
            if self.quiet:
                self.quiet = False
                self.output_message('Quiet mode requested but disabled as it is not possible (nor smart) when using PDB', warning=True)
        
        if self.quiet:
            self.verbose = False
            errors = sys.__stderr__.fileno()
            os.close(errors) # suppress the errors, mostly mapnik debug but unfortunately also tracebacks
            printed = sys.__stdout__.fileno() # suppress all stdout (includes mapnik XML printing)
            os.close(printed)
        
        self.M_TYPE = self.get_mapfile_type(self.mapfile)
        if not os.path.isfile(self.mapfile):
            if self.M_TYPE:
                output_error("Cannot open %s: '%s'" % (self.M_TYPE, self.mapfile))
            else:
                output_error("Cannot open mapfile of unknown type: '%s'" % self.mapfile) 
        else:
            if self.M_TYPE:
                self.output_message("Confirmed path to %s: '%s'" % (self.M_TYPE, os.path.abspath(self.mapfile)))
            else:
                self.output_message("Found mapfile, but cannot determine type: assuming XML format", warning=True)
                self.M_TYPE = 'XML Mapfile'

        if self.resolutions and self.levels:
            output_error("Only accepts one of either --resolutions or --levels options")
        elif self.resolutions:
            self.ZOOM_LEVELS = map(float, self.resolutions.split(','))
            self.output_message('Using custom zoom levels: %s' % self.ZOOM_LEVELS)
        elif self.levels:
            if is_int(self.levels):
                self.ZOOM_LEVELS = self.generate_levels(int(self.levels))
                self.output_message('Using %s zoom levels: %s' % (self.levels, self.ZOOM_LEVELS))
            else:
                output_error("Zoom level number must be an integer")
    
        self.TESTS_RUN = True
        if verbose: self.verbose = False

    def handle_mapfile(self):
        
        if self.mapfile.endswith('.py'):
            if self.find_and_replace:
                output_error("Find and replace not supported when loading map from python module")
            self.mapnik_map = self.load_pymap(self.mapfile)
            self.mapnik_map.width = self.width
            self.mapnik_map.height = self.height
            self.output_message('%s loaded successfully...' % self.M_TYPE)
        else:
            try:
                self.mapnik_map = mapnik.Map(self.width,self.height)
                self.output_message('Map object created successfully')
            except Exception, E:
                output_error("Problem initiating map",E)
  
            if self.mapfile.endswith('.mml'):
                try:
                    import cascadenik
                except ImportError, E:
                    output_error("%s" % E)
                xml_mapfile = cascadenik.compile(self.mapfile)
                tmp = tempfile.NamedTemporaryFile(suffix='.xml', mode = 'w')
                tmp.write(xml_mapfile)
                tmp.flush()
                self.mapfile = tmp.name
                
            if not self.find_and_replace:
                self.output_message('Attempting to load %s...' % self.M_TYPE)
                try:
                    mapnik.load_map(self.mapnik_map, self.mapfile)
                    self.output_message('%s loaded successfully...' % self.M_TYPE)
                except UserWarning, E:
                    output_error("Problem loading %s" % self.M_TYPE,E)
            else:
                # TODO: implement elementtree option for name:value control
                #try:
                #  from xml.etree import ElementTree
                #except:
                #  print 'ElementTree needed for XML find and replace approach'
                find_replace_list = self.find_and_replace.split(':')
                find_this, replace_this = find_replace_list[0], find_replace_list[1]
                mapfile_string = open(self.mapfile).read().replace(find_this,replace_this)
                tmp = tempfile.NamedTemporaryFile(suffix='.xml', mode = 'w')
                tmp.write(mapfile_string)
                tmp.flush()
                try:
                    mapnik.load_map(self.mapnik_map, tmp.name)
                    self.output_message('%s loaded and parsed successfully')
                except Exception, E:
                    output_error("Problem loading map from parsed in memory mapfile",E)

    def handle_layers(self):
        info = ''
        found_layer = False
        layers = self.layers.split(",")
        mapfile_layers = self.mapnik_map.layers
        self.output_message('Scanning %s layers' % len(self.mapnik_map.layers))
        for layer_num in range(len(self.mapnik_map.layers)-1, -1, -1):
            l = self.mapnik_map.layers[layer_num]
            if l.name not in layers:
                #for sty in l.styles:
                    #self.mapnik_map.remove_style(sty) 
                if l.active:
                    self.output_message("Removed previously ACTIVE layer '%s'" % l.name)
                else:
                    self.output_message("Removed layer '%s'" % l.name)              
                # Deleting layers seems to cause errant bounding box shifts for rendered postgis layers
                # Commenting this out for now and instead we'll make inactive
                #del self.mapnik_map.layers[layer_num]
                l.active = False
            else:
                found_layer = True
                self.output_message("Found layer '%s' out of %s total in mapfile" % (l.name,len(self.mapnik_map.layers)) )
                if not l.active:
                    l.active = True
                    self.output_message("Made requested layer active") 
                # should control this in debug settings...
                if self.verbose:
                    for group in l.datasource.describe().split('\n\n'):
                        for item in group.split('\n'):
                            if item.find('name')> -1:
                                info += '\n%s\t' % item
                            else:
                                info += '%s\t' % item 
                    self.output_message("'%s' Datasource:\n %s\n" % (l.name, info))
        if not found_layer:
            if len(layers) == 1:
                all_layers = ', '.join([l.name for l in mapfile_layers])
                print all_layers
                output_error("Layer '%s' not found in available layers: %s" % (layers[0], all ))
            else:
                output_error("No requested layers found")   

    def handle_srs(self):
        # TODO: accept <OSGEO:code>        
        self.output_message('Custom map projection requested')
        if self.srs == "epsg:900913" or self.srs == "epsg:3785":
            self.output_message('Google spherical mercator was selected and proj4 string will be used to initiate projection')
            mapnik_proj = mapnik.Projection(MERC_PROJ4)
            self.output_message("Mapnik projection successfully initiated with custom Google Spherical Mercator proj.4 string: '%s'" % mapnik_proj.params())
        elif self.srs.startswith('http://'):
            try:
                # Refactor to use gdal based osr layer or simliar code with handling of response codes.
                # http://trac.osgeo.org/gdal/changeset/11772
                import urllib
                import socket
                socket.setdefaulttimeout(10)
                try:
                    web_proj4 = urllib.urlopen('%sproj4/' % self.srs ).read()
                except IOError, E:
                    output_error('%s is not responding after 10 seconds' % self.srs,E)
                mapnik_proj = mapnik.Projection(web_proj4)
                self.output_message("Mapnik projection successfully initiated with url-fetched proj.4 string: '%s'" % mapnik_proj.params())
            except Exception, E:
                output_error("Tried to read from www.spatialreference.org, failed to fetch usable proj4 code", E)
        elif re.match('^\+init=epsg:\d+$', self.srs.lower()):
            mapnik_proj = mapnik.Projection("%s" % self.srs)
            self.output_message("Mapnik projection successfully initiated with epsg code: '%s'" % mapnik_proj.params())
        elif re.match('^epsg:\d+$', self.srs.lower()):
            mapnik_proj = mapnik.Projection("+init=%s" % self.srs)
            self.output_message("Mapnik projection successfully initiated with epsg code: '%s'" % mapnik_proj.params())
        elif re.match('^\+proj=.+$', self.srs):
            mapnik_proj = mapnik.Projection(self.srs)
            self.output_message("Mapnik projection successfully initiated with proj.4 string: '%s'" % mapnik_proj.params())
        else:
            output_error("Could not parse the supplied projection information: %s" % self.srs)
        # attempt to catch a mapnik 'proj_init_error' when espg files are not found
        if not mapnik_proj.params():
            output_error("Requested projection could not be initialized: confirm that mapnik was built with proj support and proj espg files are installed")
        self.output_message("Old map projection: '%s' | New map projection: '%s'" % (self.mapnik_map.srs, mapnik_proj.params()) )
        self.mapnik_map.srs = mapnik_proj.params()

    def handle_bbox(self):
        if self.bbox_geographic:
            try:
                bbox = map(float,self.bbox_geographic.split(","))
                bbox = mapnik.Envelope(*bbox)
                p = mapnik.Projection("%s" % self.mapnik_map.srs)
                if not p.geographic:
                    self.output_message('Initialized projection: %s' % p.params())
                    bbox = bbox.forward(p)
                    self.output_message('BBOX has been reprojected to: %s' % bbox)
                    self.output_message('Scale denominator is: %s' % self.mapnik_map.scale_denominator )
                else:
                    self.output_message('Map is in unprojected, geographic coordinates, BBOX left unchanged')
                    self.output_message('Scale denominator is: %s' % self.mapnik_map.scale_denominator )
            except Exception, E:
                output_error("Problem setting geographic bounding box", E)
            self.mapnik_map.zoom_to_box(bbox)
    
        elif self.bbox_projected:
            try:
                bbox = map(float,self.bbox_projected.split(","))
                bbox = mapnik.Envelope(*bbox)
                p = mapnik.Projection("%s" % self.mapnik_map.srs)
                if not p.geographic:
                    self.output_message('Map and bbox in projected coordinates: newly assigned BBOX left untouched',print_time=False)
                    self.output_message('BBOX must match mapfile projection',warning=True,print_time=False)            
                    self.output_message('Scale denominator is: %s' % self.mapnik_map.scale_denominator )
                else:
                    self.output_message('Map is in geographic coordinates and you supplied projected coordinates (reprojecting/inversing to lon/lat...)', warning=True)
                    bbox = mapnik.inverse_(bbox, p)
            except Exception, E:
                output_error("Problem setting projected bounding box", E)
            
            self.mapnik_map.zoom_to_box(bbox)
            self.m_bbox = self.mapnik_map.envelope()
            self.output_message('Map bbox (after zooming to your input) is now: %s' % self.m_bbox,print_time=False)
            self.output_message('Scale denominator is: %s' % self.mapnik_map.scale_denominator )           

    def handle_zooming(self):
        # http://trac.mapnik.org/browser/trunk/src/map.cpp#L245
        if self.zoom_to:
            try:
                lon,lat,level = map(float, self.zoom_to.split(","))
            except ValueError:
                lon,lat = map(float, self.zoom_to.split(","))
                level = 0
            try:
                self.zoom_max()
                res = float(self.generate_levels(int(level)+1)[int(level)])
                pt = mapnik.Coord(lon,lat)
                p = mapnik.Projection("%s" % self.mapnik_map.srs)
                if not p.geographic:
                    pt = pt.forward(p)
                width = self.mapnik_map.width
                height = self.mapnik_map.height
                box = mapnik.Envelope(pt.x - 0.5 * width * res,
                    pt.y - 0.5 * height * res, 
                    pt.x + 0.5 * width * res, 
                    pt.y + 0.5 * height * res
                    )
                self.mapnik_map.zoom_to_box(box)
                self.m_bbox = self.mapnik_map.envelope()
                self.output_message('BBOX resulting from lon,lat,level of %s,%s,%s is: %s' % (lon,lat,level,self.m_bbox),print_time=False)
                self.output_message('Scale denominator is: %s' % self.mapnik_map.scale_denominator )
            except Exception, E:
                output_error("Problem setting lon,lat,level to use for custom BBOX",E)
  
        elif self.zoom_to_radius:
            try:
                lon,lat,delta = map(float, self.zoom_to_radius.split(","))
                zoom_to_bbox = mapnik.Envelope(lon - delta, lat - delta, lon + delta, lat + delta)
                p = mapnik.Projection("%s" % self.mapnik_map.srs)
                if not p.geographic:
                    projected_bbox = zoom_to_bbox.forward(p)
                    self.m_bbox = projected_bbox
                else:
                    self.m_bbox = zoom_to_bbox
                self.mapnik_map.zoom_to_box(self.m_bbox)
                self.output_message('BBOX resulting from lon,lat,delta of %s,%s,%s is: %s' % (lon,lat,delta,self.m_bbox))
            except Exception, E:
                output_error("Problem setting lon,lat,delta to use for custom BBOX",E)
  
        elif self.zoom_to_layer:
            layer_bbox, layer_srs = self.get_layer_extent_and_srs(self.mapnik_map, self.zoom_to_layer)
            layer_p = mapnik.Projection("%s" % layer_srs)
            map_p = mapnik.Projection("%s" % self.mapnik_map.srs)
            if map_p.geographic and layer_p.geographic:
                self.m_bbox = layer_bbox
            elif not map_p.geographic and layer_p.geographic:
                projected_bbox = layer_bbox.forward(map_p)
                self.m_bbox = projected_bbox
            elif map_p.geographic and not layer_p.geographic:
                geographic_bbox = layer_bbox.inverse(layer_p)
                self.m_bbox = geographic_bbox
            elif not map_p.geographic and not layer_p.geographic:
                if layer_p.params() == map_p.params():
                    self.m_bbox = layer_bbox
                else:
                    # set up a proj4 transform as (from,to)
                    # we need to project the layer bbox to the map bbox
                    # so we go from -> to (forward)
                    transform = ProjTransform(layer_p,map_p)
                    self.m_bbox = transform.forward(layer_bbox)
            self.mapnik_map.zoom_to_box(self.m_bbox)
            self.output_message('BBOX resulting from zooming to extent of "%s" layer is now: %s' % (self.zoom_to_layer,self.m_bbox))

    def handle_expansion(self):
        if is_int(self.expand):
            self.m_bbox = self.expand_bbox(self.mapnik_map.envelope(), int(self.expand))
            self.mapnik_map.zoom_to_box(self.m_bbox)
            # TODO: need to validate that the expanded bbox still makes sense
            self.output_message('BBOX expanded by %s units to: %s' % (int(self.expand), self.m_bbox))
        else:
            output_error("Expanded units must be an integer")
           
    def build(self):
        """
        Central routine to compose the map output parameters by setting
        the dimensions, layer(s), bbox, projection, and zoom level(s).
        """    
        if not self.TESTS_RUN:
            self.test()
        self.START = time.time()
        self.TIMING_STARTED = True
        
        self.handle_mapfile()
        if self.verbose:
            self.mapfile_validate(self.mapnik_map)
      
        if self.layers:
            self.handle_layers() 
      
        if self.srs:
            self.handle_srs()

        if self.post_map_pause:
            self.output_message('Pausing for %s seconds...' % self.post_map_pause)
            pause_for(self.post_map_pause)
      
        if self.bbox_geographic or self.bbox_projected:
            self.handle_bbox()
        elif self.zoom_to or self.zoom_to_radius or self.zoom_to_layer:
            self.handle_zooming()
        else:
            self.mapnik_map.zoom_all()
            self.m_bbox = self.mapnik_map.envelope()
            self.output_message('Map bbox (max extent of all layers) is now: %s' % self.m_bbox)
            self.output_message('Scale denominator is: %s' % self.mapnik_map.scale_denominator )
        
        if self.expand:
            self.handle_expansion()
  
        if self.verbose:
            self.layers_in_extent(self.mapnik_map)
  
        if self.dry_run:
            output_error("Dry run complete")

    def render_file(self): 
        """
        Routine to render the output image(s) for all requested formats and resolutions.
        """
        if not self.BUILT:
            self.build()
        if not self.image:
            output_error("Image output name not defined.")
        else:
            dirname, basename = os.path.dirname(self.image),os.path.basename(self.image)
            if basename:
                if not True in [self.image.split('.')[-1].lower() == ext for ext in self.ALL_FORMATS]:
                    output_error("Unrecognized format (needs .ext) or directory (needs trailing /).")
            else:
                basename_from_dir = dirname.split('/')[-1]
                if not basename_from_dir: 
                    basename_from_dir = 'nik2img_output'
                if dirname == '':
                    output_error("Must write to either file or directory")
            if not os.path.exists(dirname) and dirname != '':
                try:
                    os.mkdir(dirname)
                except OSError:
                    os.makedirs(dirname)
                self.output_message("Directory output requested, will create: '%s'" % dirname)
            if not dirname.endswith('/'):
                dirname = dirname + '/'
            if not self.debug:
                if self.format == 'all':
                    if basename:
                        output_error("Must write to a directory/ to produce all formats")
                    else:                    
                        self.output_message("Beginning rendering loop of all possible formats, this may take a while...")
                        self.call_AGG_FORMATS(dirname + basename_from_dir)
                        if HAS_CAIRO:
                            self.call_CAIRO_FORMATS(dirname + basename_from_dir)
                else:
                    self.output_message("Beginning rendering, this may take a while...")
                    if not basename:
                        self.local_render_wrapper(self.mapnik_map, dirname + basename_from_dir + '.' + self.format.rstrip('256'), self.format)
                    else:
                        self.local_render_wrapper(self.mapnik_map, self.image, self.format)
            else:
                for lev in self.ZOOM_LEVELS:
                    self.mapnik_map.zoom(lev)
                    self.output_message('Map Scale: %s' % self.mapnik_map.scale(),print_time=False)
                    self.output_message('Scale denominator is: %s' % self.mapnik_map.scale_denominator,print_time=False)
                    level_name = '%slevel-%s' % (dirname,lev)
                    if self.format == 'all':
                        self.output_message("Beginning rendering loop of all possible formats and requested zoom levels, this may take a while...")
                        self.call_AGG_FORMATS(level_name)
                        if HAS_CAIRO:
                            self.call_CAIRO_FORMATS(level_name)
                    else:
                        self.output_message("Beginning rendering, this may take a while...")              
                        self.local_render_wrapper(self.mapnik_map,'%s.%s' % (level_name,self.format),self.format)

    def stream(self): 
        """
        Routine to render the an image to a string
        """
        if not self.BUILT:
          self.build()
        im = mapnik.Image(self.width,self.height)
        mapnik.render(self.mapnik_map,im)
        return im.tostring(self.format)
    
    def open(self, app=None):
        """
        Routine to open the rendered image or folder of images from the filesystem.
        """
        if not app and self.app:
            app = self.app
        if not self.RENDERED:
            self.render_file()
        try:
            if os.name == 'nt':
                if app:
                    self.output_message('Overriding default image viewer not yet supported on Win32')
                os.system('start %s' % self.image.replace('/','\\'))
            elif platform.uname()[0] == 'Linux':
                if app:
                    os.system('%s %s' % (app, self.image))
            elif platform.uname()[0] == 'Darwin':
                if app:
                    os.system('open %s -a %s' % (self.image, app))
                else:
                    os.system('open %s' % self.image)
        except:
            pass # this is fluf, so fail quietly if there is a problem

if __name__ == "__main__":
        
  def usage (name):
    print
    color_print(3, "%s" % make_line('=',75))
    color_print(4,"Usage: %s -m <mapfile.xml> -o <image.png>" % name)
    color_print(7,"Option\t\tDefault\t\tDescription")
    
    print "-m\t\t" + "<required>\t" + "Mapfile input: Set the path for the xml mapfile or mml cascading style."
    print "-o\t\t" + "[stdout]\t" + "Image filename: Set the output filename (or a directory name), otherwise printed to STDOUT."
    print "-i\t\t" + "[png]\t\t" + "Image format: png (32 bit), png256 (8 bit), jpeg, pdf, svg, ps, or all (will loop through all formats)."
    print "-e\t\t" + "[max extent]\t" + "Minx,Miny,Maxx,Maxy: Set map extent in geographic coordinates (forwarded if mapfile is projected)."
    print "-r\t\t" + "[max extent]\t" + "Minx,Miny,Maxx,Maxy: Set map extent in projected coordinates (inversed if mapfile is geographic)."
    print "-s\t\t" + "[600,300]\t" + "Width,Height: Set the image size in pixels."
    print "-p\t\t" + "[mapfile srs]\t" + "Reproject using <epsg:code>, <proj4 literal>, or a url like 'http://spatialreference.org/ref/user/6/'."
    print "-l\t\t" + "[all enabled]\t" + "Layers: List which to render (quote and comma-separate if several)."  
    print "-v\t\t" + "[off]\t\t" + "Run with verbose output including numbered steps and timing output."
    print "-c\t\t" + "[1]\t\t" + "Draw map n number of times." 
    print "-n\t\t" + "[off]\t\t" + "Turn on dry run mode: construct map but do not render output."
    print "-t\t\t" + "[0]\t\t" + "Pause n seconds after reading the map."
    print "-d\t\t" + "[None]\t\t" + "Find and replace, using a <find_this:replace_this> syntax, any value within the mapfile."
    print "--pause" + "\t\t[0]\t\t" + "Pause n seconds after each step%s." % color_text(4,'*')
    print "--pdb\t\t" + "[none]\t\t" + "Set a python debugger trace at step n or steps n,n,n%s." % color_text(4,'*')
    # --expand is alpha code
    #print "--expand\t[0]\t\tExpand bbox in all directions by a given radius (in map's srs units)%s." % color_text(4,'*')
    print "--zoomto\t[0]\t\tCenter the map at a given lon/lat coordinate and an optional zoom level%s." % color_text(4,'*')
    print "--zoomrad\t[0]\t\tZoom to an extent of the radius (in map units) around a given lon/lat coordinate%s." % color_text(4,'*')
    print "--zoomlyr\t[0]\t\tZoom to the extent of a given layer%s." % color_text(4,'*')
    # debug does nothing yet...
    #print "--debug\t\t[0]\t\tLoop through all formats and zoom levels generating map graphics%s" % color_text(4,'*')
    print "--levels\t[10]\t\tN number of zoom levels at which to generate graphics%s" % color_text(4,'*')
    print "--resolutions\t[none]\t\tGenerate outputs at a specific set of zoom levels (ie. 0.1,0.05,0.025)%s" % color_text(4,'*')
    print "--worldfile\t" + "[none]\t\t" + "Generate image georeferencing by specifying a world file output extension (ie. wld)%s." % color_text(4,'*')
    print "--fonts\t\t" + "[none]\t\t" + "Path(s) to .ttf font to register (ie. '../fonts/Verdana.ttf,../fonts/Arial.ttf')%s." % color_text(4,'*')
    print "--savemap\t" + "[none]\t\t" + "Output the processed mapfile as xml with the specified name%s." % color_text(4,'*')
    print "--app\t\t" + "[none]\t\t" + "Specify the desired application for opening the image result%s." % color_text(4,'*')
    print "--quiet\t\t[off]\t\tTurn on quiet mode to suppress the mapnik c++ debug printing and all python errors%s." % color_text(4,'*')
    print "--profile\t[off]\t\tOutput a cProfile report on script completion%s." % color_text(4,'*')
    print "--noopen\t" + "[opens]\t\t" + "Prevent the automatic opening of the image in the default viewer%s." % color_text(4,'*')
    print "--nocolor\t" + "[colored]\t" + "Turn off colored terminal output%s." % color_text(4,'*')
    print "--version\t" + "[off]\t\t" + "Prints the nik2img version."
    print "-h\t\t" + "[off]\t\t" + "Prints this usage/help information."

    
    print "%s\n %s Additional features in nik2img not part of shp2img." % (make_line('-',75), color_text(4,'*'))
    print "%s" % make_line('-',75)
    print " More info: http://code.google.com/p/mapnik-utils/wiki/Nik2Img"
    color_print(3, "%s" % make_line('=',75))
    color_print(7,__author__)
    color_print(7,"Version: %s" % __version__)
    print

  def get(key):
      ''' Get the dictionary key or return None '''
      if has(key): return mapping[key]
      else: return None
  
  def has(key):
      ''' Tiny wrapper to test for a key '''
      if mapping.has_key(key): return True
      else: return False

  try:
      options, arguments = getopt.getopt(sys.argv[1:], "m:o:i:e:s:r:p:t:l:z:d:c:nvh", ['quiet','debug','nocolor','noopen','pause=','pdb=', 'levels=', 'resolutions=', 'expand=','zoomto=','zoomlyr=','zoomrad=','maxres=','profile','worldfile=','fonts=','savemap=','app=','version','test'])
  except getopt.GetoptError, err:
      output_error(err,yield_usage=True)

  if len(sys.argv) <= 1:
      usage(sys.argv[0])
      sys.exit(1)

  # Create a dictionary to map options to values
  mapping = {}

  for option, argument in options:
      if argument.find('--') > -1:
          output_error("argumentuments can't have a '--' characters within them, did you forget to specify a value for an optionion %s?" % option)
      if option == "-m":
          mapping['m'] = argument
  
      elif option == "-o":
          mapping['o'] = argument
          
      elif option == "-i":
          mapping['i'] = argument
          
      elif option == "-e":
          mapping['e'] = argument
          
      elif option == "-p":
          mapping['p'] = argument
          
      elif option == "-r":
          mapping['r'] = argument
          
      elif option == "-t":
          mapping['t'] = argument
                  
      elif option == "-s":
          mapping['s'] = argument
          
      elif option == "-l":
          mapping['l'] = argument
  
      elif option == "-c":
          mapping['c'] = argument
          
      elif option == "-d":
          mapping['d'] = argument
          
      elif option == "-n":
          mapping['n'] = True
          dry_run = True
          
      elif option == "-v":
          mapping['v'] = True
          verbose = True
          
      elif option == "--pause":
          mapping['pause'] = argument
  
      elif option == "--quiet":
          mapping['quiet'] = True
          
      elif option == "--nocolor":
          mapping['nocolor'] = True
          no_color_global = True
  
      elif option == "--noopen":
          mapping['noopen'] = True
          
      elif option == "--expand":
          mapping['expand'] = argument
  
      elif option == "--maxres":
          mapping['maxres'] = argument
  
      elif option == "--zoomto":
          mapping['zoomto'] = argument
  
      elif option == "--zoomrad":
          mapping['zoomrad'] = argument
  
      elif option == "--zoomlyr":
          mapping['zoomlyr'] = argument
        
      elif option == "--debug":
          mapping['debug'] = True
          
      elif option == "--levels":
          mapping['levels'] = argument
          
      elif option == "--resolutions":
          mapping['resolutions'] = argument
          
      elif option == "--pdb":
          mapping['pdb'] = argument
  
      elif option == "--worldfile":
          mapping['worldfile'] = argument
  
      elif option == "--fonts":
          mapping['fonts'] = argument
  
      elif option == "--savemap":
          mapping['savemap'] = argument
  
      elif option == "--app":
          mapping['app'] = argument
  
      elif option == "--profile":
          mapping['profile'] = True
  
      elif option == "-h":
          usage(sys.argv[0])
          sys.exit(1)
  
      elif option == "--version":
          print __version__
          sys.exit(1)
          
      else:
          usage(sys.argv[0])
          sys.exit(1)
    
  if len(mapping) < 1:
      color_print(1, 'Make sure to specify the -m <input mapfile.xml>')
      usage(sys.argv[0])
      sys.exit(1)

  if has('s'):
      mapping['width'],mapping['height'] = mapping['s'].split(',')
  else:
      mapping['width'],mapping['height'] = 600, 400

  if not HAS_MAPNIK_PYTHON:
      print "Error: 'import mapnik' failed - confirm that mapnik is installed and on your PYTHONPATH."
      sys.exit(1)

  def main():
      """
      Utility function called when run from the command line.
      Will initiate a map, then build, render, and open the resulting image.
      """
      nik_map = Map( mapping['m'],
          image=get('o'), format=get('i'), width=get('width'), height=get('height'),
          bbox_geographic=get('e'), bbox_projected=get('r'), zoom_to=get('zoomto'),
          zoom_to_radius=get('zoomrad'), zoom_to_layer=get('zoomlyr'), srs=get('p'),
          layers=get('l'), expand=get('expand'), re_render_times=get('c'), post_map_pause=get('t'),
          post_step_pause=get('pause'), trace_steps=get('pdb'), levels=get('levels'), resolutions=get('resolutions'), 
          find_and_replace=get('d'), no_color=has('nocolor'), quiet=has('quiet'), dry_run=has('n'), verbose=has('v'),
          debug=has('debug'), world_file=get('worldfile'), fonts=get('fonts'), save_map=get('savemap'), app=get('app'),
          )
      if has('o'):
          if has('noopen'):
              nik_map.render_file()
          else:
              nik_map.open()
      else:
          if sys.platform == 'win32':
              binaryPrint(nik_map.stream())
          else:
              print nik_map.stream()
  
  if has('profile'):
      import cProfile
      cProfile.run('main()', sort=1)
  else:
      main()
# 1358