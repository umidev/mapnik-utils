#!/usr/bin/env python


"""

nik2img.py - In Mapnik xml, out Map image

Summary:
  A command line tool for generating map images by pointing to an XML file.
  Docs: http://code.google.com/p/mapnik-utils/wiki/Nik2Img

  Mirrors and extends the shp2img utility developed by the MapServer project.
  shp2img reference: http://mapserver.gis.umn.edu/docs/reference/utilityreference/shp2img
  shp2img code: http://trac.osgeo.org/mapserver/browser/trunk/mapserver/shp2img.c
  
  Shares simliarities with the OSM script generate_tiles.py / generate_image.py
  http://trac.openstreetmap.org/changeset/1594/utils/mapnik/generate_tiles.py

Source:
  http://code.google.com/p/mapnik-utils/

Dependencies:
  Requires Python and Mapnik installed with the python bindings

Usage:
  # Copy the script to your path then:
  $ nik2img.py -h # help on usage
  $ nik2img.py -m mapfile.xml -o yourmap.png
  $ nik2img.py -m mapfile.xml -o yourmapsfolder -i all --debug -p epsg:900913 -r 1003750,-1706377,10037508,2810502 -t 2

Limitations:
  Paths to file system datasources in the XML files loaded will be relative to your dir.

Wishlist:
  * Cascadenik integration | ability to read in css.mml or css.mss.
  * Allow for setting the path to datasources (will need patch to mapnik core)
  * Support for loading in python styles module/rules

Debugging:
  * Cairo xml crashes with floating point exception: http://mail.python.org/pipermail/c++-sig/2002-May/001023.html
  * http://www.python.org/doc/2.5.2/lib/module-fpectl.html
  
Todo:
  * extended help output
  * change zoom levels to accept high and low
  * debug the custom resolutions input (set mapnik's starting scale)
  * refactor all class methods to accept **kwargs
  * read format from file extension
  * set mapnik_object like layers and proj even if not changed
  * make mapnik_objects available as class attributes
  * move mapnik and cairo imports into class or otherwise only imported once needed
  * create an --all-formats flag and do away with -i == 'all'
  * Ability to render to images and pipe to stdout
  * Better url srs support/error checking
  * Add docstrings and code comments.
  * Set all tabs to 4 spaces
  * Add more mapfile statistics output.
  * Add ability to load alternative fonts (perhaps do automatically if found in mapfile?)
  * Debug the zoom levels/resolutions feature

Remaining shp2img features:
  * Pipe to stdout?
  * Refactor debug to shp2img setting of debug type: graphics, zooms, times, mapfile, layers, all, etc.
  * Implement datavalue substitute within mapfile using boost python access to map elements.
      ie. -d <layer/style:datavalue:newvalue>, -d world:file:'/new/path/to/datasource', -d 'my style':fill:green
  * Until datavalue substitution with native objects, perhaps using ElementTree or a 
     regex approach to grab django like variable objects ( {{ shapefile }} )
      ie. -d <currentvalue:newvalue:find/findall>
  * Implement a prepared mapfile substitution ability within the mapfile.
     ie. http://mapserver.gis.umn.edu/docs/reference/mapfile/variable_sub

formats = {'text/xml': 'gml', 'text/proj4': 'proj4', 'application/proj4': 'proj4', 'application/x-proj4': 'proj4', 'application/x-ogcwkt': 'ogcwkt', } 



for y in range(tile_count_y):
  for x in range(tile_count_x):
    if not os.path.exists("tiles/%d/%d/" % (map_scale, y)):
      os.makedirs("tiles/%d/%d/" % (map_scale, y))
      render_tile_to_file(m, x*tile_size, y*tile_size, tile_size, tile_size,'tiles/%d/%d/%d.png' % (map_scale,y,x), 'png')

im = Image(512, 512)
render(m, im)
view = im.view(128,128,256,256) # x,y,width,height
view.save(tile_uri,'png')

def generate_image(self, format):
  image = mapnik.Image(mapnik_map.width, mapnik_map.height)
  image.background = mapnik.Color("green")
  mapnik.render(mapnik_map, image)
  image_string = image.tostring("%s" % format)
  if format == "png256":
    output_headers("image/png", "map.png", len(image_string))  
  else:
    output_headers("image/%s" % (format), "map.%s" % (format), len(image_string))
  print image_string

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
    """Test given string is an integer
    """
    if str == None:
        return False
    try:
        num = int(str)
    except ValueError:
        return False
    return True
    
def pause_for(sec):
    if is_int(sec):
        for second in range(1, (int(sec)+1)):
            print color_text(5,second),
            time.sleep(1)
            sys.stdout.flush()
    else:
        output_error('Time in seconds must be integer value')

def make_line(character, n):
    line = character*n
    return line

def color_print(color, text):
    """
    Accepts an integer key for one of several color choices along with the text string to color
      keys = 1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    Returns a colored string of text.
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

class nik2img(object):
    def __init__(self, mapfile_in, map_out, format=None, bbox_geographic=None, bbox_projected=None, radius=None, width=None, height=None, srs=None, layers=None, re_render_times=None, post_map_pause=None, post_step_pause=None, trace_steps=None, levels=None, resolutions=None, find_and_replace=None, no_color=False, quiet=False, dry_run=False, verbose=False, debug=False):
      
      # Required
      self.mapfile_in = mapfile_in
      self.map_out = map_out
            
      # Defaults
      self.format = format
      self.width = width
      self.height = height
      
      # Optional arguments
      self.bbox_geographic = bbox_geographic
      self.bbox_projected = bbox_projected
      self.radius = radius
      self.srs = srs
      self.layers = layers
      self.re_render_times = re_render_times
      self.post_map_pause = post_map_pause
      self.post_step_pause = post_step_pause
      self.trace_steps = trace_steps
      self.levels = levels
      self.resolutions = resolutions
      self.find_and_replace = find_and_replace
      self.no_color = no_color      
      self.quiet = quiet
      self.dry_run = dry_run
      self.verbose = verbose
      self.debug = debug
      self.TIMING_STARTED = False
      self.STEP = 0
      self.AGG_FORMATS = {'png':'.png','png256':'.png','jpeg':'.jpg'}
      self.CAIRO_FILE_FORMATS = {'svg':'.svg','pdf':'.pdf','ps':'.ps'}
      self.CAIRO_IMAGE_FORMATS = {'ARGB32':'.png','RGB24':'.png'}
      self.start = None
      self.TESTS_RUN = False

      
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

    def output_message(self,msg, warning=False):
      if warning:
          color_print(1, 'STEP: %s | --> WARNING: %s' % (self.STEP, msg)) 
      elif self.verbose:      
          color_print(2, 'STEP: %s // --> %s' % (self.STEP, msg))
          self.output_time()
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
        if time/60 < 1:
          seconds = '%s seconds' % str(time)
          return seconds
        else:
          minutes = '%s minutes' % str(time/60)
          return minutes
    
    def elapsed(self, last_step):
        total = (time.time() - self.start)
        last = (time.time() - last_step)
        return 'Total time: %s | Last step: %s' % (self.get_time(total), self.get_time(last))
    
    def output_time(self):
        if self.TIMING_STARTED:
          color_print(4,self.elapsed(timeit.time.time()))

    # =================
    # Random functions
    # =================
    
    def set_trace(self):
        try:
          print '>>> Entering PDB interpreter'
          print '>>> Do you want to print out all mapnik map object names? (yes or no)'
          response = raw_input()
          if response == 'yes':
            if self.mapnik_objects:
              color_print(1,'Mapnik objects: %s' % ', '.join(self.mapnik_objects))
            else:
              color_print(1,'No mapnik objects available in namespace yet...')
          color_print(1,'Usage: http://docs.python.org/lib/module-pdb.html')
          color_print(1,"Type 'continue' or 'c' to leave pdb") 
          import pdb
          pdb.set_trace()
        except KeyboardInterrupt:
          pass
    
    # TODO replace with os.isdir()
    def is_file(self, name):
        if name.find('.') > -1 and name.count('.') == 1:
            return True
        elif name.rfind('.') - (len(name)+1) == -3:
            return True
        elif name.find('.') > -1 and name.count('.') <> 1:
            output_error("Unknown output type; cannot determine whether it's a file or directory")
        else:
            return False

    def generate_levels(self,N=10):
        levels = [x*.1 for x in range(1,N)]
        levels.reverse()
        return levels

  # ================================================
  # Functions involving mapnik objects
  # ================================================

    def mapfile_validate(self, m):
        for layer in m.layers:
            if not layer.datasource:
              self.output_message("Datasource not found for layer '%s': hint check permissions and if using a shapefile remove the .shp ext" % layer.name, warning=True)
            if not layer.srs:
              self.output_message('Layer has no projection, assumed to be WGS84 (epsg:4326)', warning=True)
        
    def layers_in_extent(self, m):
        mapfile_layers = m.layers
        map_envelope = m.envelope()
        for layer_num in range(len(m.layers)-1, -1, -1):
            l = mapfile_layers[layer_num]
            layer_envelope = l.envelope()
            if map_envelope.intersects(layer_envelope):
                self.output_message("Map layer '%s' intersects Map envelope" % l.name)
            else:
                self.output_message("Map layer '%s' does not intersect with Map envelope" % l.name, warning=True)
                self.output_message("Map layer envelope is: %s  |  Map envelope is %s" % (layer_envelope, map_envelope), warning=True)

    def puff_bbox(self, bbox, delta):
        bbox.expand_to_include(bbox.minx-delta, bbox.miny-delta)
        bbox.expand_to_include(bbox.maxx+delta, bbox.maxy+delta)
        #bbox = (bbox.minx - delta, bbox.miny - delta, bbox.maxx + delta, bbox.maxy + delta)
        return bbox

    def local_render_wrapper(self,*args): #modifed mapnik.render_to_file to accept cairo formats
        if args[2] in self.CAIRO_FILE_FORMATS:
            self.render_cairo(*args)
        elif args[2] in self.AGG_FORMATS:
            self.render_agg(*args)
        
    def render_cairo(self,*args):
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
            

    def call_CAIRO_FORMATS(self, basename):
        if not HAS_CAIRO:
          self.output_message('PyCairo is not installed or available, therefore your cannot write to svg, pdf, ps, or cairo-rendered png', warning=True)
        else:
          for k, v in self.CAIRO_FILE_FORMATS.iteritems():
              path = '%s_%s%s' % (basename,k,v)
              self.render_cairo(self.mapnik_map,path,k)
          for k, v in self.CAIRO_IMAGE_FORMATS.iteritems():
              path = '%s_%s%s' % (basename,k,v)
              self.render_cairo(self.mapnik_map,path,k)

      
    def render_agg(self,*args):
        if self.re_render_times:
          for n in range(1, int(self.re_render_times)):
            mapnik.render_to_file(*args)
            self.output_message("Map rendered to '%s', %s times" % (args[1], n))
        else:
          mapnik.render_to_file(*args)
          self.output_message("Map rendered to '%s'" % args[1])
        
    def call_AGG_FORMATS(self, basename):
        for k, v in self.AGG_FORMATS.iteritems():
            path = '%s_%s%s' % (basename,k,v)
            self.render_agg(self.mapnik_map,path,k)


    # ==============================================
    # Tests of variable inputs, run once from build(), but can be called separately
    # ==============================================

    def test(self, verbose=False):
      if verbose: self.verbose = True
      
      self.ZOOM_LEVELS = self.generate_levels(10)
      
      # do some validation and special handling for a few arguments
      if not self.format:
        self.format = 'png'

      if self.width:
        if is_int(self.width):
          self.width = int(self.width)
        else:
          output_error('width must be an integer',E)
      else:
        self.width = 600
      
      if self.height:
        if is_int(self.height):
            self.height = int(self.height)
        else:
            output_error("height must be an integer",E)
      else:
        self.height = 400

      if self.trace_steps:
        self.trace_steps = [int(step) for step in self.trace_steps.split(",")]
      if self.no_color:
        global no_color_global
        no_color_global = True

      if self.levels and not self.debug:
        self.debug = True

      if self.resolutions and not self.debug:
        self.debug = True

      #if self.post_step_pause and not self.verbose:
        #self.verbose = True
      
      if self.trace_steps and not self.verbose:
        self.verbose = True
        self.output_message('PDB trace requested, automatically entering verbose mode')
        if self.quiet:
          self.quiet = False
          self.output_message('Quiet mode requested but disabled as it is not possible (nor smart) when using PDB', warning=True)
    
      if self.quiet:
        self.output_message('Quite mode requested: no output (stdout) or errors(sterr) will be printed')
        errors = sys.__stderr__.fileno()
        os.close(errors) # suppress the errors, mostly mapnik debug but unfortunately also tracebacks
        printed = sys.__stdout__.fileno() # suppress all stdout (includes mapnik XML printing)
        os.close(printed)
        
      if not os.path.isfile(self.mapfile_in):
        output_error("Cannot open XML mapfile: '%s'" % self.mapfile_in)
      else:
        self.output_message("Confirmed path to XML mapfile: %s" % self.mapfile_in)
  

      
      self.TESTS_RUN = True
      if verbose: self.verbose = False

    # =====================================
    # Primary builder of map parameters - needs more refactoring
    # =====================================
    
    def build(self):
      
      if not self.TESTS_RUN:
        self.test()
      
      self.start = timeit.time.time()
      self.TIMING_STARTED = True
      
      try:
        self.mapnik_map = mapnik.Map(self.width,self.height)
        self.output_message('Map object created successfully')
        self.mapnik_objects['self.mapnik_map'] = self.mapnik_map
      except Exception, E:
        output_error("Problem initiating map",E)
    
      if self.resolutions and self.levels:
        output_error('Only accepts one of either --resolutions or --levels options')
      elif self.resolutions:
        self.ZOOM_LEVELS = [float(r) for r in self.resolutions.split(',')]
        self.output_message('Using custom zoom levels: %s' % self.ZOOM_LEVELS)
      elif self.levels:
        if is_int(self.levels):
          levels= int(self.levels) + 1
          self.ZOOM_LEVELS = self.generate_levels(levels)
          self.output_message('Using %s zoom levels: %s' % (self.levels, self.ZOOM_LEVELS))
        else:
          output_error("Zoom level number must be an integer")
          
      if not self.find_and_replace:
        try:    
          mapnik.load_map(self.mapnik_map, self.mapfile_in)
          self.output_message('XML mapfile loaded successfully')
        except Exception, E:
          output_error("Problem loading map",E)
      else:
        # TODO: implement elementtree optionion for name:value control
        #try:
        #  from xml.etree import ElementTree
        #except:
        #  print 'ElementTree needed for XML find and replace approach'
        import tempfile
        find_replace_list = self.find_and_replace.split(':')
        find_this, replace_this = find_replace_list[0], find_replace_list[1]
        mapfile_string = open(self.mapfile_in).read().replace(find_this,replace_this)
        tmp = tempfile.NamedTemporaryFile(suffix='.xml', mode = 'w')
        tmp.write(mapfile_string)
        tmp.flush()
        try:
          mapnik.load_map(self.mapnik_map, tmp.name)
          self.mapfile_validate(self.mapnik_map)
          self.output_message('XML mapfile loaded and parsed successfully')
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
              self.mapnik_objects['self.mapnik_map.layers[%s]' % layer_num] = l
              self.mapnik_layers[layer_num] = self.mapnik_map.layers[layer_num]
              for group in l.datasource.describe().split('\n\n'):
                for item in group.split('\n'):
                  if item.find('name')> -1:
                    info += '\n%s\t' % item
                  else:
                    info += '%s\t' % item 
              self.output_message("'%s' Datasource:\n %s\n" % (l.name, info))
        if not found_layer:
            if len(layers) == 1:
              output_error("Layer '%s' not found" % layers[0])
            else:
              output_error('No requested layers found')    
    
      # TODO: accept <OSGEO:code>
      if self.srs:
        self.output_message('Reprojecting map output')
        if self.srs == "epsg:900913" or self.srs == "epsg:3785":
          self.output_message('Google spherical mercator was selected and proj4 string will be used to initiate projection')
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
            output_error('Tried to read from www.spatialreference.org, failed to fetch usable proj4 code', E)
        elif re.match('^epsg:\d+$', self.srs):
          mapnik_proj = mapnik.Projection("+init=%s" % self.srs)
          self.output_message("Mapnik projection successfully initiated with epsg code: '%s'" % mapnik_proj.params())
        elif re.match('^\+proj=.+$', self.srs):
          mapnik_proj = mapnik.Projection(self.srs)
          self.output_message("Mapnik projection successfully initiated with proj.4 string: '%s'" % mapnik_proj.params())
        else:
          output_error('Could not parse the supplied projection information')
        self.mapnik_map.srs = mapnik_proj.params()
        self.mapnik_objects['mapnik_proj'] = mapnik_proj
    
      if self.post_map_pause:
        self.output_message('Pausing for %s seconds...' % self.post_map_pause)
        pause_for(self.post_map_pause)
    
      if self.bbox_geographic:
        try:
          bbox = [float(x) for x in self.bbox_geographic.split(",")]
          bbox = mapnik.Envelope(*bbox)
          p = mapnik.Projection("%s" % self.mapnik_map.srs)
          if not p.geographic:
            self.output_message('Initialized projection: %s' % p.params())
            bbox = mapnik.forward_(bbox, p)
            self.mapnik_objects['bbox'] = bbox
            self.output_message('BBOX has been reprojected to: %s' % bbox)
          else:
            self.mapnik_objects['bbox'] = bbox
            self.output_message('Map is in unprojected, geographic coordinates, BBOX left unchanged')
        except Exception, E:
           output_error("Problem setting geographic bounding box", E)
        self.mapnik_map.zoom_to_box(bbox)
      elif self.bbox_projected:
        try:
          bbox = [float(x) for x in self.bbox_projected.split(",")]
          bbox = mapnik.Envelope(*bbox)
          p = mapnik.Projection("%s" % self.mapnik_map.srs)
          if not p.geographic:
            self.mapnik_objects['bbox'] = bbox
            self.output_message('Map and bbox in projected coordinates (hopefully the srs matches), newly assigned BBOX left unprojected.')
          else:
            self.output_message('Map is in geographic coordinates and you supplied projected coordinates', warning=True)
            output_error('Inverse method not yet supported')        
        except Exception, E:
           output_error("Problem setting projected bounding box", E)
        
        # Finally, zoom map to bbox
        self.mapnik_map.zoom_to_box(bbox)
        self.m_bbox = self.mapnik_map.envelope()
        self.output_message('Map bbox (after zooming to your input) is now: %s' % self.m_bbox)
        self.mapnik_objects['self.m_bbox'] = self.m_bbox
        
  
      else:
        try:    
          # If no bounding box supplied then zoom to the extent of all layers
          self.mapnik_map.zoom_all()
          self.m_bbox = self.mapnik_map.envelope()
          self.output_message('Map bbox (max extent of all layers) is now: %s' % self.m_bbox)
          self.mapnik_objects['self.m_bbox'] = self.m_bbox
        except Exception, E:
          output_error("Problem Zooming to all layers",E)
    
      if self.radius:
        if is_int(self.radius):
          self.m_bbox = self.puff_bbox(self.mapnik_map.envelope(), int(self.radius))
          self.mapnik_map.zoom_to_box(self.m_bbox)
          self.mapnik_objects['self.m_bbox'] = self.m_bbox
          # TODO: need to validate that the expanded bbox still makes sense
          self.output_message('BBOX expanded by %s units to: %s' % (int(self.radius), self.m_bbox))
        else:
          output_error('Radius must be an integer')
    
      # Check for which layers intersect with map envelope
      self.layers_in_extent(self.mapnik_map)

      if self.dry_run:
        output_error('Dry run complete')
        # output custom stats here?

        
    # =====================================
    # Render to the desired format using the desired method
    # =====================================

    def render(self, method=None): 

      out = self.map_out
      if not self.is_file(out):
        if not os.path.exists('%s' % out):
          os.mkdir(out)
        out = '%s/%s.%s' % (out,out,self.format) # place in folder using default format
      if not self.debug:
          if self.format == 'all':
              basename = out.split('.')[0]
              self.call_AGG_FORMATS(basename)
              self.call_CAIRO_FORMATS(basename)
          else:
              self.local_render_wrapper(self.mapnik_map, out, self.format)
      else:
        # look into mapnik scale demoninators
        for lev in self.ZOOM_LEVELS:
          self.mapnik_map.zoom(lev)
          self.output_message('Map Scale: %s' % self.mapnik_map.scale())
          basename = out.split('.')[0]
          level_name = '%s_level-%s' % (basename,lev)
          if self.format == 'all':
                self.call_AGG_FORMATS(level_name)
                self.call_CAIRO_FORMATS(level_name)
          else:
                self.local_render_wrapper(self.mapnik_map,'%s.%s' % (level_name,self.format),self.format)         

    # ===============================================
    # Open the file or folder - this needs to get much smarter, particularly on linux
    # ===============================================    
    
    def open(self, method='Desktop', app=None):
      if not method == 'Desktop':
        output_error('no other method supported at this time')
      else:
        import platform
        if os.name == 'nt':
          os.system('start %s' % self.map_out)
        elif platform.uname()[0] == 'Linux':
          # TODO figure out how to open a folder on linux
          if app:
            os.system('%s %s' % (app, self.map_out))
          else:
            os.system('gthumb %s' % self.map_out) # other apps to try?
        elif platform.uname()[0] == 'Darwin':
          os.system('open %s' % self.map_out)
        self.output_message("Completed, opening '%s' <%s'" %   (self.map_out, color_text(3, "%s" % make_line('=',55)),))


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
    print "-o\t\t" + "<required>\t" + "Image filename: Set the output filename (or a directory name)."
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

    # these apis are going to change so restricting for now...
    #print "--expand\t[0]\t\tExpand bbox in all directions by a given radius (in map's srs units)%s." % color_text(4,'*')
    #print "--debug\t\t[0]\t\tLoop through all formats and zoom levels generating map graphics%s" % color_text(4,'*')
    #print "--levels\t[10]\t\tN number of zoom levels at which to generate graphics%s" % color_text(4,'*')
    #print "--resolutions\t[none]\t\tSet specific rendering resolutions (ie 0.1,0.05,0.025)%s" % color_text(4,'*')
    #print "--quiet\t\t[off]\t\tTurn on quiet mode to suppress the mapnik c++ debug printing and all python errors%s." % color_text(4,'*')

    print "--noopen\t" + "[opens]\t" + "Prevent the automatic opening of the image in the default viewer%s." % color_text(4,'*')
    print "--nocolor\t" + "[colored]\t" + "Turn off colored terminal output%s." % color_text(4,'*')
    print "-h\t\t" + "[off]\t\t" + "Prints this usage/help information."
    
    print "%s\n %s Additional features in nik2img not part of shp2img." % (make_line('-',75), color_text(4,'*'))
    print " %s nik2img does not support sending image to STDOUT (default in shp2img)." % color_text(4,'Note:')
    print "%s" % make_line('-',75)
    print " More info: http://code.google.com/p/mapnik-utils/wiki/Nik2Img"
    color_print(3, "%s" % make_line('=',75))
    color_print(7,"Dane Springmeyer, dbsgeo (a-t) gmail.com")
    print

  def get(key):
    ''' Get the dict key or return None '''
    if has(key): return mapping[key]
    else: return None
  
  def has(key):
    ''' Tiny wrapper to test for a key '''
    if mapping.has_key(key): return True
    else: return False

  try:
    options, arguments = getopt.getopt(sys.argv[1:], "m:o:i:e:s:r:p:t:l:z:d:c:nvh", ['quiet','debug','nocolor','noopen','pause=','pdb=', 'levels=', 'resolutions=', 'expand='])
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
        
    elif option == "--debug":
        mapping['debug'] = True
        
    elif option == "--levels":
        mapping['levels'] = argument
        
    elif option == "--resolutions":
        mapping['resolutions'] = argument
        
    elif option == "--pdb":
        mapping['pdb'] = argument
        
    elif option == "-h":
        usage(sys.argv[0])
        sys.exit(1)
        
    else:
        usage(sys.argv[0])
        sys.exit(1)
    
  if len(mapping) < 2:
    color_print(1, 'Make sure to specify the -m <input mapfile.xml> and -o <output image>')
    usage(sys.argv[0])
    sys.exit(1)

  if has('s'):
      mapping['width'],mapping['height'] = mapping['s'].split(',')
  
  mapfile_in, map_out = mapping['m'], mapping['o']

  nik_map = nik2img( mapfile_in, map_out,
                      format=get('i'), bbox_geographic=get('e'),
                      bbox_projected=get('r'), radius=get('expand'), width=get('width'),
                      height=get('height'), srs=get('p'), layers=get('l'), re_render_times=get('c'),
                      post_map_pause=get('t'), post_step_pause=get('pause'), trace_steps=get('pdb'),
                      levels=get('levels'), resolutions=get('resolutions'), find_and_replace=get('d'), 
                      no_color=has('nocolor'), quiet=has('quiet'), dry_run=has('n'), verbose=has('v'),
                      debug=has('debug'),
                      )
                      
  nik_map.build()
  if has('noopen'):
    nik_map.render()
  else:
    nik_map.render()
    nik_map.open()
