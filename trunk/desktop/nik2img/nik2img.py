#!/usr/bin/env python


"""

nik2img.py - In Mapnik xml, out Map image

Summary:
  A command line tool for generating map images by pointing to an XML file.
  Docs: http://code.google.com/p/mapnik-utils/wiki/Nik2Img

  Mirrors and extends the shp2img utility developed by the MapServer project.
  shp2img reference: http://mapserver.gis.umn.edu/docs/reference/utilityreference/shp2img
  shp2img code: http://trac.osgeo.org/mapserver/browser/trunk/mapserver/shp2img.c
  
  Shares simliarities with the OSM scripts: generate_tiles.py / generate_image.py
  http://trac.openstreetmap.org/changeset/1594/utils/mapnik/generate_tiles.py

Source:
  http://code.google.com/p/mapnik-utils/

Dependencies:
  Requires Python and Mapnik installed with the python bindings

Usage:
  Copy the script to your path then:
  $ nik2img.py -h # help on usage
  $ nik2img.py -m mapfile.xml -o yourmap.png

Limitations:
  Paths to file system datasources in the XML files loaded will be relative to your dir.

Wishlist:
  * Allow for setting the path to datasources (will need patch to mapnik core)
  * Support for loading in python styles module/rules
  
Todo:
  * Add ability to load alternative fonts (perhaps do automatically if found in mapfile?)
  * create an --all-formats flag and do away with -i == 'all'
  * accept formats as list
  * turn usage help into a dictionary to be able to reuse
  * add alternative output mode for non-commandline usage
  * coerce all cl args to correct python types before sending to Map()
  * refactor all class methods to accept **kwargs
  * change zoom levels to accept high and low
  * set mapnik_object like layers and proj even if not changed
  * Better url srs support/error checking
     sr_org_responses = {'text/xml': 'gml', 'text/proj4': 'proj4', 'application/proj4': 'proj4', 'application/x-proj4': 'proj4', 'application/x-ogcwkt': 'ogcwkt', } 
  * Set all tabs to 4 spaces
  * Add more mapfile statistics output.

Remaining shp2img features:
  * Refactor debug to shp2img setting of debug type: graphics, zooms, times, mapfile, layers, all, etc.
  * Implement datavalue substitute within mapfile using boost python access to map elements.
      ie. -d <layer/style:datavalue:newvalue>, -d world:file:'/new/path/to/datasource', -d 'my style':fill:green
  * Until datavalue substitution with native objects, perhaps use ElementTree or a 
     regex approach to grab django like variable objects ( {{ shapefile }} )
      ie. -d <currentvalue:newvalue:find/findall>
  * Implement a prepared mapfile substitution ability within the mapfile.
     ie. http://mapserver.gis.umn.edu/docs/reference/mapfile/variable_sub

"""

__author__ = "Dane Springmeyer (dbsgeo [ -a- ] gmail.com)"
__copyright__ = "Copyright 2008, Dane Springmeyer"
__version__ = "0.1.1 $Rev: 2 $"
__license__ = "GPLv2"


import os
import sys
import getopt
import re
import time
import timeit
import tempfile

try:
    import mapnik
except Exception, E:
    print 'Could not load mapnik python bindings'
    sys.exit()

try:
  import cairo
  HAS_CAIRO = True
except Exception, E:
  HAS_CAIRO = False

no_color_global = False


# ==========================================
# Top Level Functions
# ==========================================

def is_int(str):
    """
    Test if a given string is an integer.
    """
    if str == None:
        return False
    try:
        num = int(str)
    except ValueError:
        return False
    return True
    
def pause_for(sec):
    """
    Pauses script execution for n seconds using the time.sleep module.
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

def output_error(msg, E=None, yield_usage=False):
    """
    Prints an error message to stdout, including a Traceback
    error if given (E), and command line usage if requested.
    """
    if yield_usage:
        usage(sys.argv[0])
    if E:
        color_print(1, '// --> %s: \n\n %s' % (msg, E))
    else:
        color_print(1, '\\ --> %s' % msg)    
    sys.exit(1)


# =============================================================================
#
# Program mainline.
#
# =============================================================================

class Map(object):
    def __init__(self, mapfile, image='', width=600, height=400, format='png256', bbox_geographic=None, bbox_projected=None, zoom_to=None, zoom_to_radius=None, zoom_to_layer=None, expand=None, srs=None, layers=None, re_render_times=None, post_map_pause=None, post_step_pause=None, trace_steps=None, levels=None, resolutions=None, max_resolution=None, find_and_replace=None, no_color=False, quiet=False, dry_run=False, verbose=False, debug=False, world_file=None):
        """
        ----

        Initialize a nik2img Map object either from the commandline or as a class import.
        
        Then build() and either provide an output image path and user render_file() or pipe the output of render_stream()
        
        Required argument:
        --> mapfile\t string\t path to the mapnik xml file
        
        Optional **kwargs:
        --> See the commandline usage
        
        Usage:
        
        To save a map to the filesystem and open it with the default viewer:
        >>> from nik2img import Map
        >>> file = Map('/path/to/mapfile.xml','map.png')
        >>> file.open()
        
        To stream an image to a web browser:
        >>> from nik2img import Map
        >>> content = Map('/path/to/mapfile.xml')
        >>> image = content.stream()
        >>> print "Content-Type: %s" % content.mime
        >>> print "Content-Length: %d" % len(image)
        >>> print '' 
        >>> print image


        ----
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
        
        # Non argument class attributes
        self.TIMING_STARTED = False
        self.STEP = 0
        self.MAPFILE_TYPES = {'xml':'XML mapfile','mml':'Cascadenik Cascading Stylesheet', 'py':'Python Styles'}
        self.M_TYPE = None
        self.AGG_FORMATS = {'png':'png','png256':'png','jpeg':'jpg'}
        self.CAIRO_FILE_FORMATS = {'svg':'svg','pdf':'pdf','ps':'ps'}
        self.CAIRO_IMAGE_FORMATS = {'ARGB32':'png','RGB24':'png'}
        self.START = None
        self.TESTS_RUN = False
        self.BUILT = False
        self.RENDERED = False
        
        # collect mapnik objects
        self.mapnik_map = None
        self.mapnik_objects = {}
        self.m_bbox = None
        self.mapnik_layers = {}
        self.mapnik_proj = None
        self.bbox = None


    # ==========================================================
    # Function for handling printed terminal output when verbose = True or a pdb trace is requested
    # ==========================================================

    def output_message(self,msg, warning=False, print_time=True):
        """
        Output a colored message or warning, incrementing the STEP counter
        to enable a pdb trace to be set at any point a verbose message is printed.
        """
        if warning:
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
      
    # =================
    # Functions for script timing
    # =================

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
        return 'Total time: %s | Last step: %s' % (self.get_time(total), self.get_time(last))
    
    def output_time(self, print_time):
        """
        Timing output wrapper to control the start point and verbosity of timing output.
        """
        if self.TIMING_STARTED and print_time:
          color_print(4,self.elapsed(timeit.time.time()))

    # =================
    # Random functions
    # =================
    
    def set_trace(self):
        """
        Routine to set a Python Debugger trace.
        """
        try:
          print ">>> Entering PDB interpreter (press 'c' to leave)"
          print '>>> Print out current mapnik object names? (yes or no)'
          response = raw_input()
          if response == 'yes':
            if self.mapnik_objects:
              color_print(1,'Mapnik objects: %s' % ', '.join(self.mapnik_objects))
            else:
              color_print(1,'No mapnik objects available in namespace yet...')
          import pdb
          pdb.set_trace()
        except KeyboardInterrupt:
          pass
    
    # TODO replace with os.isdir()
    def is_file(self, name):
        """
        Routing to check if a given image name is a file or folder.
        """
        if name.find('.') > -1 and name.count('.') == 1:
            return True
        elif name.rfind('.') - (len(name)+1) == -3:
            return True
        elif name.find('.') > -1 and name.count('.') <> 1:
            output_error("Unknown output type; cannot determine whether it's a file or directory")
        else:
            return False

    def generate_levels(self,N=10):
        """
        Accepts a number of zoom levels and returns a list of zoom resolutions.
        """
        levels = [self.max_resolution / 2 ** i for i in range(int(N))]        
        return levels

  # ================================================
  # Functions involving mapnik objects
  # ================================================
        
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
        transformation_warning = True
        for layer_num in range(len(m.layers)-1, -1, -1):
            check_intersects = True
            l = mapfile_layers[layer_num]
            layer_bbox = l.envelope()
            layer_p = mapnik.Projection("%s" % l.srs)
            map_p = mapnik.Projection("%s" % self.mapnik_map.srs)            
            if map_p.geographic and layer_p.geographic:
                pass # no need to reproject layer envelope
            elif not map_p.geographic and layer_p.geographic:
                layer_bbox = mapnik.forward_(layer_bbox, map_p) # project/forward the layers envelope
            elif map_p.geographic and not layer_p.geographic:
                layer_bbox = mapnik.inverse_(layer_bbox, layer_p) # invert the layers envelope
            elif not map_p.geographic and not layer_p.geographic:
                if layer_p.params() == map_p.params():
                  pass # no need to reproject layer envelope
                else:
                  check_intersects = False
                  if transformation_warning:
                    self.output_message("Mapnik's python bindings do not support transformation between projected coordinates, see http://trac.mapnik.org/ticket/117",print_time=False,warning=True)
                    transformation_warning = False
                  self.output_message("Unable to reliably check for intersection of layer '%s' with map envelope..." % l.name,warning=True)
            if check_intersects:
                if layer_bbox.intersects(map_envelope):
                    self.output_message("Layer '%s' intersects Map envelope" % l.name,print_time=False)
                    self.output_message("Layer envelope was: %s  |  Map envelope is %s" % (layer_bbox, map_envelope),print_time=False)
                    self.output_message("Center point of layer '%s' is %s" % (l.name, layer_bbox.center()),print_time=False)
                    self.output_message("Layer's minzoom = '%s' and maxzoom = '%s'"  % (l.minzoom, l.maxzoom) )
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
        elif args[2] in self.AGG_FORMATS:
            self.render_agg(*args)

    def write_world_file(self, path, x_rotation=0.0, y_rotation=0.0):
        """
        Outputs an ESRI world file that can be used to load the resulting
        image as a georeferenced raster in a variety of gis viewers.
        
        A world file file is a plain ASCII text file consisting of six values separated
        by newlines. The format is: 
            pixel X size
            rotation about the Y axis (usually 0.0)
            rotation about the X axis (usually 0.0)
            negative pixel Y size
            X coordinate of upper left pixel center
            Y coordinate of upper left pixel center
         
        Info from: http://gdal.osgeo.org/frmt_various.html#WLD
        """
        scale = self.mapnik_map.scale()
        extent= self.mapnik_map.envelope()
        upper_left_x_center = extent.minx-(scale/2.0)
        upper_left_y_center = extent.maxy-(scale/2.0)
        wld_string = '%s\n%s\n%s\n-%s\n%s\n%s\n' % (scale,y_rotation,x_rotation,scale,upper_left_x_center,upper_left_y_center)
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

    def call_CAIRO_FORMATS(self, basename):
        """
        Abstraction wrapper to allow for the same call
        to any image and file formats requested from Cairo.
        """
        if not HAS_CAIRO:
          self.output_message('PyCairo is not installed or available, therefore your cannot write to svg, pdf, ps, or cairo-rendered png', warning=True)
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
      if verbose: self.verbose = True
       
      self.format = self.format.lower().replace('image/','')
      self.mime = 'image/%s' % self.format.replace('256','')
    
      # do some validation and special handling for a few arguments
      if not self.max_resolution:
        self.max_resolution = 1.0
      else:
        self.max_resolution = float(self.max_resolution)
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
          
           
      self.TESTS_RUN = True
      if verbose: self.verbose = False

    # =====================================
    # Primary builder of map parameters - needs more refactoring
    # =====================================
    
    def build(self):
      """
      Central routine to compose the map output parameters by setting
      the dimensions, layer(s), bbox, projection, and zoom level(s).
      """    
      if not self.TESTS_RUN:
        self.test()
      
      self.START = timeit.time.time()
      self.TIMING_STARTED = True
      
      try:
        self.mapnik_map = mapnik.Map(self.width,self.height)
        self.output_message('Map object created successfully')
        self.mapnik_objects['self.mapnik_map'] = self.mapnik_map
      except Exception, E:
        output_error("Problem initiating map",E)
    
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
      
      if self.mapfile.endswith('.py'):
        output_error("Support for loading python styles planned but not supported currently")

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
          if self.verbose:
            self.mapfile_validate(self.mapnik_map)
          self.output_message('%s loaded successfully...' % self.M_TYPE)
        except Exception, E:
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
          if self.verbose:
            self.mapfile_validate(self.mapnik_map)
          self.output_message('%s loaded and parsed successfully')
        except Exception, E:
          output_error("Problem loading map from parsed in memory mapfile",E)
    
      if self.layers:
        info = ''
        found_layer = False
        layers = self.layers.split(",")
        mapfile_layers = self.mapnik_map.layers
        self.output_message('Scanning %s layers' % len(self.mapnik_map.layers))
        for layer_num in range(len(self.mapnik_map.layers)-1, -1, -1):
            l = self.mapnik_map.layers[layer_num]
            if l.name not in layers:
                del self.mapnik_map.layers[layer_num]
                if l.active == True:
                  self.output_message("Removed previously ACTIVE layer '%s'" % l.name)
                else:
                  self.output_message("Removed layer '%s'" % l.name)              
            else:
              found_layer = True
              self.output_message("Found layer '%s' out of %s total in mapfile" % (l.name,len(self.mapnik_map.layers)) )
              if not l.active:
                l.active = True
                self.output_message("Made requested layer active") 
              self.mapnik_objects['self.mapnik_map.layers[%s]' % layer_num] = l
              self.mapnik_layers[layer_num] = self.mapnik_map.layers[layer_num]
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
              all = ', '.join([l.name for l in mapfile_layers])
              print all
              output_error("Layer '%s' not found in available layers: %s" % (layers[0], all ))
            else:
              output_error("No requested layers found")    
    
      # TODO: accept <OSGEO:code>
      if self.srs:
        self.output_message('Custom map projection requested')
        if self.srs == "epsg:900913" or self.srs == "epsg:3785":
          self.output_message('Google spherical mercator was selected and proj4 string will be used to initiate projection')
          # TODO: investigate impact of '+over' parameter
          google_proj4 = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
          mapnik_proj = mapnik.Projection(google_proj4)
          self.output_message("Mapnik projection successfully initiated with custom Google Spherical Mercator proj.4 string: '%s'" % mapnik_proj.params())
        elif self.srs.startswith('http://'):
          try:
            # Refactor to use gdal based osr layer or simliar code with handling of response codes.
            # http://trac.osgeo.org/gdal/changeset/11772
            import urllib
            web_proj4 = urllib.urlopen('%sproj4/' % self.srs ).read()
            mapnik_proj = mapnik.Projection(web_proj4)
            self.output_message("Mapnik projection successfully initiated with url-fetched proj.4 string: '%s'" % mapnik_proj.params())
          except Exception, E:
            output_error("Tried to read from www.spatialreference.org, failed to fetch usable proj4 code", E)
        elif re.match('^epsg:\d+$', self.srs.lower()):
          mapnik_proj = mapnik.Projection("+init=%s" % self.srs.lower())
          self.output_message("Mapnik projection successfully initiated with epsg code: '%s'" % mapnik_proj.params())
        elif re.match('^\+proj=.+$', self.srs.lower()):
          mapnik_proj = mapnik.Projection(self.srs.lower())
          self.output_message("Mapnik projection successfully initiated with proj.4 string: '%s'" % mapnik_proj.params())
        else:
          output_error("Could not parse the supplied projection information")
        # attempt to catch a mapnik 'proj_init_error' when espg files are not found
        if not mapnik_proj.params():
          output_error("Requested projection could not be initialized: confirm that mapnik was built with proj support and proj espg files are installed")
        self.output_message("Old map projection: '%s' | New map projection: '%s'" % (self.mapnik_map.srs, mapnik_proj.params()) )
        self.mapnik_map.srs = mapnik_proj.params()
        self.mapnik_objects['mapnik_proj'] = mapnik_proj
    
      if self.post_map_pause:
        self.output_message('Pausing for %s seconds...' % self.post_map_pause)
        pause_for(self.post_map_pause)
    
      if self.bbox_geographic:
        try:
          bbox = map(float,self.bbox_geographic.split(","))
          bbox = mapnik.Envelope(*bbox)
          p = mapnik.Projection("%s" % self.mapnik_map.srs)
          if not p.geographic:
            self.output_message('Initialized projection: %s' % p.params())
            bbox = mapnik.forward_(bbox, p)
            self.mapnik_objects['bbox'] = bbox
            self.output_message('BBOX has been reprojected to: %s' % bbox)
            self.output_message('Scale denominator is: %s' % mapnik.scale_denominator(self.mapnik_map,False) )
          else:
            self.mapnik_objects['bbox'] = bbox
            self.output_message('Map is in unprojected, geographic coordinates, BBOX left unchanged')
            self.output_message('Scale denominator is: %s' % mapnik.scale_denominator(self.mapnik_map,True) )
        except Exception, E:
           output_error("Problem setting geographic bounding box", E)
        self.mapnik_map.zoom_to_box(bbox)
      elif self.bbox_projected:
        try:
          bbox = map(float,self.bbox_projected.split(","))
          bbox = mapnik.Envelope(*bbox)
          p = mapnik.Projection("%s" % self.mapnik_map.srs)
          if not p.geographic:
            self.mapnik_objects['bbox'] = bbox
            self.output_message('Map and bbox in projected coordinates: newly assigned BBOX left untouched',print_time=False)
            self.output_message('BBOX must match mapfile projection',warning=True,print_time=False)            
            self.output_message('Scale denominator is: %s' % mapnik.scale_denominator(self.mapnik_map,False) )
          else:
            self.output_message('Map is in geographic coordinates and you supplied projected coordinates (reprojecting/inversing to lon/lat...)', warning=True)
            bbox = mapnik.inverse_(bbox, p)
            self.mapnik_objects['bbox'] = bbox
        except Exception, E:
           output_error("Problem setting projected bounding box", E)
        
        # Finally, zoom map to bbox
        self.mapnik_map.zoom_to_box(bbox)
        self.m_bbox = self.mapnik_map.envelope()
        self.output_message('Map bbox (after zooming to your input) is now: %s' % self.m_bbox,print_time=False)
        self.output_message('Scale denominator is: %s' % mapnik.scale_denominator(self.mapnik_map,p.geographic))           
        self.mapnik_objects['self.m_bbox'] = self.m_bbox
      
      # http://trac.mapnik.org/browser/trunk/src/map.cpp#L245
      elif self.zoom_to:
        try:
          lon,lat,level = map(float, self.zoom_to.split(","))
        except ValueError:
          lon,lat = map(float, self.zoom_to.split(","))
          level = 1
        if not level >=1:
            output_error("Zoom level must be an integer between 1 and the maximum desired zoom")
        else:
          try:          
            zoom = float(self.generate_levels(int(level))[int(level)-1])
            minx, miny, maxx, maxy = lon+(lon*zoom), lat-(lat*zoom), lon-(lon*zoom), lat+(lat*zoom)
            zoom_to_bbox = mapnik.Envelope(minx, miny, maxx, maxy)
            p = mapnik.Projection("%s" % self.mapnik_map.srs)
            if not p.geographic:
                projected_bbox = mapnik.forward_(zoom_to_bbox, p)
                m_bbox = projected_bbox
            else:
                m_bbox = zoom_to_bbox
            self.mapnik_map.zoom_to_box(m_bbox)
            self.mapnik_map.zoom(level)
            self.m_bbox = self.mapnik_map.envelope()
            self.mapnik_objects['self.m_bbox'] = self.m_bbox
            self.output_message('BBOX resulting from lon,lat,level of %s,%s,%s is: %s' % (lon,lat,level,self.m_bbox),print_time=False)
            self.output_message('Scale denominator is: %s' % mapnik.scale_denominator(self.mapnik_map,p.geographic))
            #print 'scale: %s' % self.mapnik_map.scale()
            #print 'fraction: 1/%s' % int(1/self.mapnik_map.scale())
            #sd = self.mapnik_map.scale()/mapnik.scale_denominator(self.mapnik_map,True)
            #print 'scale/denom: %s' % sd
          except Exception, E:
            output_error("Problem setting lon,lat,level to use for custom BBOX",E)

      elif self.zoom_to_radius:
        try:
          lon,lat,delta = map(float, self.zoom_to_radius.split(","))
          zoom_to_bbox = mapnik.Envelope(lon - delta, lat - delta, lon + delta, lat + delta)
          p = mapnik.Projection("%s" % self.mapnik_map.srs)
          if not p.geographic:
              projected_bbox = mapnik.forward_(zoom_to_bbox, p)
              self.m_bbox = projected_bbox
          else:
              self.m_bbox = zoom_to_bbox
          self.mapnik_map.zoom_to_box(self.m_bbox)
          self.mapnik_objects['self.m_bbox'] = self.m_bbox
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
              projected_bbox = mapnik.forward_(layer_bbox, map_p)
              self.m_bbox = projected_bbox
          elif map_p.geographic and not layer_p.geographic:
              geographic_bbox = mapnik.inverse_(layer_bbox, layer_p)
              self.m_bbox = geographic_bbox
          elif not map_p.geographic and not layer_p.geographic:
              if layer_p.params() == map_p.params():
                self.m_bbox = layer_bbox
              else:
                output_error("Mapnik's python bindings do not support transformation between projected coordinates, see http://trac.mapnik.org/ticket/117")
          self.mapnik_map.zoom_to_box(self.m_bbox)
          self.mapnik_objects['self.m_bbox'] = self.m_bbox
          self.output_message('BBOX resulting from zooming to extent of "%s" layer is now: %s' % (self.zoom_to_layer,self.m_bbox))    

      else:
        try:    
          # If no custom bounding box supplied then zoom to the extent of all layers
          self.mapnik_map.zoom_all()
          self.m_bbox = self.mapnik_map.envelope()
          self.output_message('Map bbox (max extent of all layers) is now: %s' % self.m_bbox)
          p = mapnik.Projection("%s" % self.mapnik_map.srs)
          self.output_message('Scale denominator is: %s' % mapnik.scale_denominator(self.mapnik_map,p.geographic))
          self.mapnik_objects['self.m_bbox'] = self.m_bbox
        except Exception, E:
          output_error("Problem Zooming to all layers",E)
      
      if self.expand:
        if is_int(self.expand):
          self.m_bbox = self.expand_bbox(self.mapnik_map.envelope(), int(self.expand))
          self.mapnik_map.zoom_to_box(self.m_bbox)
          self.mapnik_objects['self.m_bbox'] = self.m_bbox
          # TODO: need to validate that the expanded bbox still makes sense
          self.output_message('BBOX expanded by %s units to: %s' % (int(self.expand), self.m_bbox))
        else:
          output_error("Expanded units must be an integer")

      # Check for which layers intersect with map envelope
      self.layers_in_extent(self.mapnik_map)

      if self.dry_run:
        output_error("Dry run complete")
        # output custom stats here?

        
    # =====================================
    # Render to the desired format to a file
    # =====================================

    def render_file(self): 
        """
        Routine to render the output image(s) for all requested formats and resolutions.
        """
        if not self.BUILT:
          self.build()
        if not self.image:
          output_error("Image output name not defined.")
        else:
          out = self.image
          if not self.is_file(out):
            if not os.path.exists('%s' % out):
              os.mkdir(out)
            out = '%s/%s' % (out,out)
            self.output_message("Directory output requested, will write to: '%s'" % out)
          if not self.debug:
              if self.format == 'all':
                  basename = out.split('.')[0]
                  self.output_message("Beginning rendering loop of all possible formats, this may take a while...")
                  self.call_AGG_FORMATS(basename)
                  self.call_CAIRO_FORMATS(basename)
              else:
                  self.output_message("Beginning rendering, this may take a while...")
                  self.local_render_wrapper(self.mapnik_map, out, self.format)
          else:
            for lev in self.ZOOM_LEVELS:
              self.mapnik_map.zoom(lev)
              self.output_message('Map Scale: %s' % self.mapnik_map.scale(),print_time=False)
              p = mapnik.Projection("%s" % self.mapnik_map.srs)
              self.output_message('Scale denominator is: %s' % mapnik.scale_denominator(self.mapnik_map,p.geographic),print_time=False)
              basename = out.split('.')[0]
              level_name = '%s_level-%s' % (basename,lev)
              if self.format == 'all':
                  self.output_message("Beginning rendering loop of all possible formats and requested zoom levels, this may take a while...")
                  self.call_AGG_FORMATS(level_name)
                  self.call_CAIRO_FORMATS(level_name)
              else:
                  self.output_message("Beginning rendering, this may take a while...")              
                  self.local_render_wrapper(self.mapnik_map,'%s.%s' % (level_name,self.format),self.format)

    # =====================================
    # Render to the desired format to a string
    # =====================================

    def stream(self): 
        """
        Routine to render the an image to a string
        """
        if not self.BUILT:
          self.build()
        im = mapnik.Image(self.width,self.height)
        mapnik.render(self.mapnik_map,im)
        return im.tostring(self.format)

    # ===============================================
    # Open the file or folder - this needs to get much smarter, particularly on linux
    # ===============================================    
    
    def open(self, method='Desktop', app=None):
        """
        Routine to open the rendered image or folder of images from the filesystem.
        """
        if not self.RENDERED:
          self.render_file()
        if not method == 'Desktop':
          output_error("no other method supported at this time")
        else:
          import platform
          if os.name == 'nt':
            os.system('start %s' % self.image)
          elif platform.uname()[0] == 'Linux':
            # TODO figure out how to open a folder on linux
            if app:
              os.system('%s %s' % (app, self.image))
            else:
              os.system('gthumb %s' % self.image) # other apps to try?
          elif platform.uname()[0] == 'Darwin':
            os.system('open %s' % self.image)
          self.output_message("Completed, opening '%s' <%s'" %   (self.image, color_text(3, "%s" % make_line('=',55)),))


# =============================================================================
#
# If run from command line.
#
# =============================================================================

if __name__ == "__main__":  
        
  def usage (name):
    print
    color_print(3, "%s" % make_line('=',75))
    color_print(2,"Usage: %s -m <mapnik.xml> -o <image.png>" % name)
    color_print(4,"Option\t\tDefault\t\tDescription")
    
    print "-m\t\t" + "<required>\t" + "Mapfile input: Set the path for the xml map file."
    print "-o\t\t" + "[stdout]\t" + "Image filename: Set the output filename (or a directory name), otherwise printed to STDOUT."
    print "-i\t\t" + "[png]\t\t" + "Image format: png (32 bit), png256 (8 bit), jpeg, pdf, svg, ps, or all (will loop through all formats)."
    print "-e\t\t" + "[max extent]\t" + "Minx,Miny,Maxx,Maxy: Set map extent in geographic (lon/lat) coordinates."
    print "-r\t\t" + "[max extent]\t" + "Minx,Miny,Maxx,Maxy: Set map extent in the projected coordinates of mapfile."
    print "-s\t\t" + "[600,300]\t" + "Width,Height: Set the image size in pixels."
    print "-p\t\t" + "[mapfile srs]\t" + "Reproject using epsg, proj4 string, or url like 'http://spatialreference.org/ref/user/6/'."
    print "-l\t\t" + "[all enabled]\t" + "Layers: List which to render (quote and comma-separate if several)."  
    print "-v\t\t" + "[off]\t\t" + "Run with verbose output (includes numbered steps and timing output)."
    print "-c\t\t" + "[1]\t\t" + "Draw map n number of times." 
    print "-n\t\t" + "[off]\t\t" + "Turn on dry run mode: no map output."
    print "-t\t\t" + "[0]\t\t" + "Pause n seconds after reading the map."
    print "-d\t\t" + "[None]\t\t" + "Find and replace of mapfile text strings; syntax: find_this:replace_this."
    print "--pause" + "\t\t[0]\t\t" + "Pause n seconds after each step%s." % color_text(4,'*')
    print "--pdb\t\t" + "[none]\t\t" + "Set a python debugger trace at step n or steps n,n,n%s." % color_text(4,'*')
    print "--expand\t[0]\t\tExpand bbox in all directions by a given radius (in map's srs units)%s." % color_text(4,'*')
    print "--zoomto\t[0]\t\tCenter the map at a given lon/lat coordinate and an optional zoom level%s." % color_text(4,'*')
    print "--zoomrad\t[0]\t\tZoom to an extent of the radius (in map units) around a given lon/lat coordinate%s." % color_text(4,'*')
    print "--zoomlyr\t[0]\t\tZoom to the extent of a given layer%s." % color_text(4,'*')
    print "--debug\t\t[0]\t\tLoop through all formats and zoom levels generating map graphics%s" % color_text(4,'*')
    print "--levels\t[10]\t\tN number of zoom levels at which to generate graphics%s" % color_text(4,'*')
    print "--resolutions\t[none]\t\tSet specific rendering resolutions (ie 0.1,0.05,0.025)%s" % color_text(4,'*')
    print "--quiet\t\t[off]\t\tTurn on quiet mode to suppress the mapnik c++ debug printing and all python errors%s." % color_text(4,'*')
    print "--profile\t[off]\t\tOutput a cProfile report on script completion%s." % color_text(4,'*')
    print "--worldfile\t" + "[none]\t\t" + "Generate image georeferencing by specifying a world file output extension (ie wld)%s." % color_text(4,'*')
    print "--noopen\t" + "[opens]\t\t" + "Prevent the automatic opening of the image in the default viewer%s." % color_text(4,'*')
    print "--nocolor\t" + "[colored]\t" + "Turn off colored terminal output%s." % color_text(4,'*')
    print "-h\t\t" + "[off]\t\t" + "Prints this usage/help information."
    
    print "%s\n %s Additional features in nik2img not part of shp2img." % (make_line('-',75), color_text(4,'*'))
    print "%s" % make_line('-',75)
    print " More info: http://code.google.com/p/mapnik-utils/wiki/Nik2Img"
    color_print(3, "%s" % make_line('=',75))
    color_print(7,"Dane Springmeyer, dbsgeo (a-t) gmail.com")
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
    options, arguments = getopt.getopt(sys.argv[1:], "m:o:i:e:s:r:p:t:l:z:d:c:nvh", ['quiet','debug','nocolor','noopen','pause=','pdb=', 'levels=', 'resolutions=', 'expand=','zoomto=','zoomlyr=','zoomrad=','maxres=','profile','worldfile='])
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

    elif option == "--profile":
        mapping['profile'] = True

    elif option == "-h":
        usage(sys.argv[0])
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
        debug=has('debug'), world_file=get('worldfile'),
        )
    if has('o'):
      if has('noopen'):
        nik_map.render_file()
      else:
        nik_map.open()
    else:
      print nik_map.stream()

  if has('profile'):
   import cProfile
   cProfile.run('main()', sort=1)
  else:
   main()
