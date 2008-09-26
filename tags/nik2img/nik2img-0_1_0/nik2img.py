#!/usr/bin/env python


"""

nik2img.py - In Mapnik xml, out Map image

Summary:
  A command line tool for generating map images by pointing to an XML file.
  Docs: http://code.google.com/p/mapnik-utils/wiki/Nik2Img

  Mirrors and extends the shp2img utility developed by the MapServer project.
  shp2img reference: http://mapserver.gis.umn.edu/docs/reference/utilityreference/shp2img
  shp2img code: http://trac.osgeo.org/mapserver/browser/trunk/mapserver/shp2img.c

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
  * Refactor into a single function when run as main.
  * Support cairo renderer and formats.
  * Allow for setting the path to datasources (will need patch to mapnik core)
  
Todo:
  * Add docstrings and code comments.
  * Set all tabs to 4 spaces
  * Add more mapfile statistics output.
  * Add ability to load alternative fonts (perhaps do automatically if found in mapfile?)
  * Further test the zoom levels/resolutions feature (not sure about mapnik's starting scale)

Remaining shp2img features:
  * Refactor debug to shp2img setting of debug type: graphics, zooms, times, mapfile, layers, all, etc.
  * Implement datavalue substitute within mapfile using boost python access to map elements.
      ie. -d <layer/style:datavalue:newvalue>, -d world:file:'/new/path/to/datasource', -d 'my style':fill:green
  * Until datavalue substitution with native objects, perhaps using ElementTree
      ie. -d <currentvalue:newvalue:find/findall>
  * Implement a prepared variable substitution ability within the mapfile.
     ie. http://mapserver.gis.umn.edu/docs/reference/mapfile/variable_sub


"""

__author__ = "Dane Springmeyer (dbsgeo [ -a- ] gmail.com"
__copyright__ = "Copyright 2008, Dane Springmeyer"
__version__ = "0.1.0 $Rev: 1 $"
__license__ = "GPLv2"


import os
import sys
try:
    import pdb
    HAS_PDB = True
except:
    HAS_PDB = False


# =============================================================================
#
# Nik2img Functions.
#
# =============================================================================


def make_line(character, n):
    line = character*n
    return line

def color_print(color,text):
    """
    1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    """
    if not os.name == 'nt' and not var.has_key('nocolor'):
      print "\033[9%sm%s\033[0m" % (color,text)
    else:
      print text

def color_text(color,text):
    """
    1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    """
    if not os.name == 'nt' and not var.has_key('nocolor'):
        return "\033[9%sm%s\033[0m" % (color,text)
    else:
        return text

def pause_for(sec):
    try:
        sec = int(sec)
        for second in range(1, int(sec+1)):
            print color_text(5,second),
            time.sleep(1)
            sys.stdout.flush()
    except Exception, E:
        output_error('Time in seconds but be integer value', E)

def output_error(msg, E=None, yield_usage=False):
    if yield_usage:
        usage(sys.argv[0])
    if E:
        color_print(1, '// --> %s: \n\n %s' % (msg, E))
    else:
        color_print(1, '\\ --> %s' % msg)    
    sys.exit(1)

def set_trace():
    global HAS_PDB
    if HAS_PDB:
      print '>>> Entering PDB interpreter'
      print '>>> Do you want to print out all mapnik variables? (yes or no)'
      response = raw_input()
      if response == 'yes':
        color_print(1,'How to use pdb? see: http://docs.python.org/lib/module-pdb.html')
        color_print(1,"\n\nType 'continue' to leave pdb") 
        print 'Sorry, variable printing not yet implemented'
        pdb.set_trace()
      else:
        pdb.set_trace()
    else:
      print "import pdb' failed, passing..."

def output_message(msg, warning=False):
    global STEP, VERBOSE
    if VERBOSE:      
      if warning:
        color_print(1, 'STEP: %s | --> WARNING: %s' % (STEP, msg)) 
      else:
        if var.has_key('pause'):
          color_print(2, 'STEP: %s // --> %s' % (STEP, msg))
          output_time()
          pause_for(var['pause'])
        else:
          color_print(2, 'STEP: %s // --> %s' % (STEP, msg))
          output_time()         
        print
      STEP += 1
      if var.has_key('pdb') and STEP == int(var['pdb']):
          set_trace() 
    else:
      pass # no debugging messages

def is_file(name):
    if name.find('.') > -1 and name.count('.') == 1:
        return True
    elif name.rfind('.') - (len(name)+1) == -3:
        return True
    elif name.find('.') > -1 and name.count('.') <> 1:
        output_error("Unknown output type; cannot guess whether it's a file or directory")
    else:
        return False

def generate_levels(N=10):
    levels = [x*.1 for x in range(1,N)]
    levels.reverse()
    return levels

def layers_in_extent():
    mapfile_layers = mapnik_map.layers
    map_envelope = mapnik_map.envelope()
    for layer_num in range(len(mapnik_map.layers)-1, -1, -1):
          l = mapfile_layers[layer_num]
          layer_envelope = l.envelope()
          if map_envelope.intersects(layer_envelope):
              output_message("Map layer '%s' intersects Map envelope" % l.name)
              output_message("Map layer '%s' intersects Map envelope" % l.name)
          else:
              output_message("Map layer '%s' does not intersect with Map envelope, skipping details" % l.name, warning=True)
              
def render(*args):
    if var.has_key('c'):
      for graphic in range(1, int(var['c'])):
        mapnik.render_to_file(*args)
        output_message("Map rendered to '%s', %s times" % (args[1], graphic))
    else:
        mapnik.render_to_file(*args)
        output_message("Map rendered to '%s'" % args[1])

def get_time(time):
    if time/60 < 1:
      seconds = '%s seconds' % str(time)
      return seconds
    else:
      minutes = '%s minutes' % str(time/60)
      return minutes

def elapsed(last_step):
    total = (time.time() - start)
    last = (time.time() - last_step)
    return 'Total time: %s | Last step: %s' % (get_time(total), get_time(last))

def output_time():
    global STARTED
    if STARTED:
      color_print(4,elapsed(timeit.time.time()))
    else:
      pass

def puff_bbox(bbox, unit):
    bbox.expand_to_include(bbox.minx-unit,bbox.miny-unit)
    bbox.expand_to_include(bbox.maxx+unit,bbox.maxy+unit)
    return bbox


# =============================================================================
#
# Usage.
#
# =============================================================================


def usage (name):
  print
  color_print(3, "%s" % make_line('=',75))
  color_print(2,"Usage: %s -m <mapnik.xml> -o <image.png>" % name)
  color_print(4,"Option\t\tDefault\t\tDescription")
  print "-m\t\t<required>\tMapfile: Path to xml map file to load styles from."
  print "-o\t\t<required>\tImage: Set the output filename (or a directory name: just use no .ext%s)" % color_text(4,'*')
  print "-i\t\t[png]\t\tFormat: Choose the output format: png, png256, jpeg, or all (will loop through all formats)"
  print "-e\t\t[max extent]\tMinx,Miny,Maxx,Maxy: Set map extent in geographic (lon/lat) coordinates%s" % color_text(4,'*')
  print "-r\t\t[max extent]\tMinx,Miny,Maxx,Maxy: Set map extent in projected coordinates of mapfile"
  print "--expand\t[0]\t\tExpand bbox in all directions by n map units"  
  print "-s\t\t[600,300]\tWidth,Height: Set the image size in pixels"
  print "-p\t\t[mapfile srs]\tReproject using epsg, proj4 string, or url 'ie -p http://spatialreference.org/ref/user/6/'%s" % color_text(4,'*')
  print "-l\t\t[all enabled]\tSet layers to enable (quote and comma-separate if several)"  
  print "-v\t\t[off]\t\tRun with verbose output"
  print "-c\t\t[1]\t\tDraw map n number of times" 
  print "-n\t\toff\t\tTurn on dry run mode: no map output"
  print "-t\t\t[0]\t\tPause n seconds after reading the map"
  print "--pause\t\t[0]\t\tPause n seconds after each step%s" % color_text(4,'*')
  print "--debug\t\t[0]\t\tLoop through all formats and zoom levels generating map graphics%s" % color_text(4,'*')
  print "--pdb\t\t[none]\t\tSet a pdb trace (python debugger) at step n%s" % color_text(4,'*')
  print "--levels\t[10]\t\tN number of zoom levels at which to generate graphics%s" % color_text(4,'*')
  print "--resolutions\t[none]\t\tSet specific rendering resolutions (ie 0.1,0.05,0.025)%s" % color_text(4,'*')
  print "--nocolor\t[colored]\tTurn off colored terminal output%s" % color_text(4,'*')
  print "--quiet\t\t[off]\t\tTurn on quiet mode to suppress the mapnik c++ debug printing and all python errors%s" % color_text(4,'*')
  print "-d\t\t[None]\t\tFind and replace of any text string within a mapfile, separated with ':' like find_this:replace_this"
  print "-h\t\t[off]\t\tPrints this usage/help information"
  print "%s\n %s Additional features in nik2img not part of shp2img" % (make_line('-',75), color_text(4,'*'))
  print " %s nik2img does not support sending image to STDOUT (default in shp2img)" % color_text(4,'Note:')
  color_print(3, "%s" % make_line('=',75))
  color_print(7,"Dane Springmeyer, dbsgeo (a-t) gmail.com")
  print


# =============================================================================
#
# Program mainline.
#
# =============================================================================

if __name__ == "__main__":
  import getopt
  import time
  import timeit
  
  WIDTH = 600
  HEIGHT = 300
  AGG_FORMATS = {'png':'.png','png256':'.png','jpeg':'.jpg'}
  CAIRO_FORMATS = {'svg':'.svg','pdf':'.pdf','ps':'.ps'}
  ZOOM_LEVELS = generate_levels(10)
  FORMAT = 'png'
  run = False  
  VERBOSE = False
  QUIET = False
  DRY_RUN = False
  STARTED = False
  STEP = 0
  SET_TRACE = False
  built_test_outputs = False
  var = {}        # In/Out paths

  try:
    opts, args = getopt.getopt(sys.argv[1:], "m:o:i:e:s:r:p:t:l:z:d:c:nvh", ['quiet','debug','nocolor','pause=','pdb=', 'levels=', 'resolutions=', 'expand='])
  except getopt.GetoptError, err:
    output_error(err,yield_usage=True)

  if len(sys.argv) <= 1:
    usage(sys.argv[0])
    sys.exit(1)
  
  for opt, arg in opts:
    if arg.find('--') > -1:
      output_error("Arguments can't have a '--', did you forget to specify a value for an option %s?" % opt)
    if opt == "-m":
         var['m'] = arg
    elif opt == "-o":
        var['o'] = arg
    elif opt == "-i":
        var['i'] = arg
    elif opt == "-e":
        var['e'] = arg
    elif opt == "-p":
        var['p'] = arg
    elif opt == "-r":
        var['r'] = arg
    elif opt == "-t":
        var['t'] = arg
    elif opt == "--pause":
        var['pause'] = arg
    elif opt == "-s":
        var['s'] = arg
    elif opt == "-l":
        var['l'] = arg   
    elif opt == "-c":
        var['c'] = arg   
    elif opt == "-d":
        var['d'] = arg
    elif opt == "-n":
        DRY_RUN = True
    elif opt == "-v":
        VERBOSE = True
    elif opt == "--quiet":
        var['quiet'] = True
        QUIET = True
    elif opt == "--nocolor":
        var['nocolor'] = True
    elif opt == "--expand":
        var['expand'] = arg
    elif opt == "--debug":
        var['debug'] = arg
        DEBUG =True
    elif opt == "--levels":
        var['levels'] = arg
    elif opt == "--resolutions":
        var['resolutions'] = arg
    elif opt == "--pdb":
        var['pdb'] = arg
    elif opt == "-h":
        usage(sys.argv[0])
        sys.exit(1)
    else:
        usage(sys.argv[0])
        sys.exit(1)
    
  if len(var) < 2:
    output_error('Make sure to specify the -m <input mapfile.xml> and -o <output image>',yield_usage=True)
  else:
    run = True

    if var.has_key('p'):
      if var['p'] == 'db':
        output_error("Did you mean to specify '--pdb'?")

    if var.has_key('pdb'):
      try:
        int(var['pdb'])
      except:
        output_error('Requires integer input')

    if not var.has_key('debug') and (var.has_key('levels') or var.has_key('resolutions')):
      output_error('Must be in debug mode to output multple graphics resolutions (--debug)')

    if var.has_key('l'):
      print var['l']
      if var['l'] == 'evels':
        output_error("Did you mean to specify '--levels'?")

    if var.has_key('pdb') and not var.has_key('v'):
      VERBOSE = True
      output_message('PDB trace requested, automatically entering VERBOSE mode')
      if var.has_key('quiet'):
        QUIET = False
        output_message('Quiet mode requested but not possible (nor smart)', warning=True)

    if var.has_key('quiet') and QUIET:
      output_message('Quite mode requested, careful: no errors will be output')
      errors = sys.__stderr__.fileno()
      os.close(errors) # suppress the errors, mostly mapnik debug but unfortunately also tracebacks

    if not os.path.isfile(var['m']):
      output_error("Cannot open XML mapfile: '%s'" % var['m'])
    else:
      output_message("Confirmed path to XML mapfile: %s" % var['m'])

  if not run:
    sys.exit(1)

  if var.has_key('s'):
    WIDTH,HEIGHT = var['s'].split(',')
    output_message('Custom dimensions requested of %s (width), and %s (height) pixels' % (WIDTH,HEIGHT))
  
  try:
    WIDTH = int(WIDTH)
  except Exception, E:
    output_error("Width must be an integer",E)

  try:
    HEIGHT = int(HEIGHT)
  except Exception, E:
    output_error("Height must be an integer",E)

  start = timeit.time.time()
  STARTED = True
  
  try:
      import mapnik
      output_message('Loaded mapnik python bindings')
  except Exception, E:
      output_error('Could not load mapnik python bindings', E)

  try:
    mapnik_map = mapnik.Map(WIDTH,HEIGHT)
    output_message('Map object created successfully')
  except Exception, E:
    output_error("Problem initiating map",E)

  if var.has_key('resolutions') and var.has_key('levels'):
    output_error('Only accepts one of either --resolutions or --levels options')
  elif var.has_key('resolutions'):
    ZOOM_LEVELS = [float(r) for r in var['resolutions'].split(',')]
    output_message('Using custom zoom levels: %s' % ZOOM_LEVELS)
  elif var.has_key('levels'):
    levels = var['levels']
    try:
      levels= int(levels) + 1
      ZOOM_LEVELS = generate_levels(levels)
      output_message('Using %s zoom levels: %s' % (levels, ZOOM_LEVELS))
    except Exception, E:
      output_error("Zoom level number must be an integer",E)
      
  if not var.has_key('d'):
    try:    
      mapnik.load_map(mapnik_map, var['m'])
      output_message('XML mapfile loaded successfully')
    except Exception, E:
      output_error("Problem loading map",E)
  else:
    # TODO: implement elementtree option for name:value control
    #try:
    #  from xml.etree import ElementTree
    #except:
    #  print 'ElementTree needed for XML find and replace approach'
    import tempfile
    find_replace = var['d'].split(':')
    find_this, replace_this = find_replace[0], find_replace[1]
    mapfile_string = open(var['m']).read().replace(find_this,replace_this)
    tmp = tempfile.NamedTemporaryFile(suffix='.xml', mode = 'w')
    tmp.write(mapfile_string)
    tmp.flush()
    try:
      mapnik.load_map(mapnik_map, tmp.name )
      output_message('XML mapfile loaded and parsed successfully')
    except Exception, E:
      output_error("Problem loading map from variable parsed temporary (in memory) mapfile",E)

  if var.has_key('l'):
    info = ''
    found_layer = False
    layers = var['l'].split(",")
    mapfile_layers = mapnik_map.layers
    output_message('Scanning %s layers' % len(mapnik_map.layers))
    for layer_num in range(len(mapnik_map.layers)-1, -1, -1):
        l = mapnik_map.layers[layer_num]
        if l.name not in layers:
            del mapnik_map.layers[layer_num]
            if l.active == True:
              output_message("Removed previously ACTIVE layer '%s'" % l.name)
            else:
              output_message("Removed layer '%s'" % l.name)              
        else:
          found_layer = True
          output_message("Found layer '%s' out of %s total in mapfile" % (l.name,len(mapnik_map.layers)) )
          for group in l.datasource.describe().split('\n\n'):
            for item in group.split('\n'):
              if item.find('name')> -1:
                info += '\n%s\t' % item
              else:
                info += '%s\t' % item 
          output_message("'%s' Datasource:\n %s\n" % (l.name, info))
    if not found_layer:
        if len(layers) == 1:
          output_error("Layer '%s' not found" % layers[0])
        else:
          output_error('No requested layers found')    

  # TODO: Accept spatialreference.org url, or OSGEO:codes
  if var.has_key('p'):
    output_message('Reprojecting map output')
    if var['p'] == "epsg:900913" or var['p'] == "epsg:3785":
      output_message('Google spherical mercator was selected and proj4 string will be used to initiate projection')
      google_merc = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
      epsg = mapnik.Projection(google_merc)
    elif var['p'].find('http') > -1:
      try:
        import urllib
        proj4 = urllib.urlopen('%sproj4/' % var['p']).read()
        epsg = mapnik.Projection(proj4)
      except Exception, E:
        output_error('Tried to read from www.spatialreference.org, failed to fetch proj4 code', E)
    else:
      epsg = mapnik.Projection("+init=%s" % var['p'])
      output_message("Mapnik projection successfully initiated with epsg code: '%s'" % epsg.params())
    mapnik_map.srs = epsg.params()

  if var.has_key('t'):
    output_message('Pausing for %s seconds...' % var['t'])
    pause_for(var['t'])

  #TODO: refactor, test zoom function
  if var.has_key('e'):
    try:
      bbox = [float(x) for x in var['e'].split(",")]
      bbox = mapnik.Envelope(*bbox)
      p = mapnik.Projection("%s" % mapnik_map.srs)
      if not p.geographic:
        output_message('Initialized projection: %s' % p.params())
        bbox = mapnik.forward_(bbox, p)
        output_message('BBOX in projected coordinates is: %s' % bbox)
    except Exception, E:
       output_error("Problem setting geographic bounding box", E)
    mapnik_map.zoom_to_box(bbox)
  elif var.has_key('r'):
    try:
      bbox = [float(x) for x in var['r'].split(",")]
      bbox = mapnik.Envelope(*bbox)
      output_message('BBOX is: %s' % bbox)
    except Exception, E:
       output_error("Problem setting projected bounding box", E)
    mapnik_map.zoom_to_box(bbox)
  else:
    try:    
      mapnik_map.zoom_all()
      output_message('BBOX (max extent of all layers) is: %s' % mapnik_map.envelope())
    except Exception, E:
      output_error("Problem Zooming to all layers",E)

  if var.has_key('expand'):
    puff_by = int(var['expand'])
    puffed_bbox = puff_bbox(mapnik_map.envelope(), puff_by)
    mapnik_map.zoom_to_box(puffed_bbox)
    # TODO: need to validate that the expanded bbox still makes sense
    output_message('BBOX expanded by %s units to: %s' % (puff_by, puffed_bbox))

  # Check for which layers intersect with map envelope
  layers_in_extent()
    
  if DRY_RUN:
    output_error('Dry run complete')

  # TODO: cleanup this code.
  o = var['o']
  if not is_file(o):
      try:
        os.mkdir(o)
      except OSError:
        # do we dare remove the directory?
        output_error('Directory already exists, please delete before proceeding...')
      o = '%s/%s.%s' % (o,o,FORMAT)
  if not var.has_key('debug'):    
    try:
      if var.has_key('i'):
        if var['i'] == 'all':
          o = o.split('.')[0]
          for k, v in AGG_FORMATS.iteritems():
            try:  
              render(mapnik_map,'%s_%s%s' % (o,k,v), k)
            except Exception, E:
              output_error("Error when rendering to file",E)
        else:
          render(mapnik_map,o, var['i'])
      else:
          render(mapnik_map,o,FORMAT)
    except Exception, E:
      output_error("Error when rendering to file",E)
  else:
    for lev in ZOOM_LEVELS:
      mapnik_map.zoom(lev)
      output_message('Map Scale: %s' % mapnik_map.scale())
      o_name = '%s_level-%s' % (o.split('.')[0],lev)
      try:
        if var.has_key('i'):
          if var['i'] == 'all':
            for k, v in AGG_FORMATS.iteritems():
              try:
                file = '%s_%s%s' % (o_name,k,v)
                output_message('File output: %s' % file)
                # TODO: check for feature intersection here
                # warn when none
                render(mapnik_map,file, k)
              except Exception, E:
                output_error("Error when rendering to file",E)
          else:
            render(mapnik_map,o_name, var['i'])
        else:
            render(mapnik_map,'%s.%s' % (o_name,FORMAT),FORMAT)  
      except Exception, E:
        output_error("Error when rendering to file",E)
    
    # open result
  try:
    import platform
    if os.name == 'nt':
      os.system('start %s' % var['o'])
    elif platform.uname()[0] == 'Linux':
      # TODO figure out how to open a folder on linux
      os.system('gthumb %s' % var['o'])
    elif platform.uname()[0] == 'Darwin':
      os.system('open %s' % var['o'])
    output_message("Completed, opening '%s' <%s'" %   (var['o'], color_text(3, "%s" % make_line('=',55)),))
  except:
    print 'Completed'