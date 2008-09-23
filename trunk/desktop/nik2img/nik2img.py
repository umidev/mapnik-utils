#!/usr/bin/env python

"""

nik2img.py - In Mapnik xml, out Map image

Summary:
  A command line tool for generating map images by pointing to an XML file.
  
  Mirrors the shp2img utility developed by the MapServer project.
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
  Very sparse on the error handling so far.
 
ToDo
  * Add docstrings and code comments.
  * Add mapfile stats output.
  * Add timeit module.
  * Add ability to load alternative fonts (perhaps do automatically if found in mapfile?)
  * Need to check if removed layers were active or inactive
  * Further test the zoom resolutions feature (not sure about mapniks starting scale)
  * Add ability to set specific resolutions for ZOOM_LEVELS with flag
  * Refactor into a single function when run as main.
  * Support cairo renderer and formats.
  * Refactor debug to shp2img setting of debug type: graphics, zooms, times, mapfile, layers, all, etc.
  * Implement datavalue substitute within mapfile using boost python access to map elements.
      ie. -d <layer/style:datavalue:newvalue>, -d world:file:'/new/path/to/datasource', -d 'my style':fill:green
  * Until datavalue substitution with native objects, perhaps using ElementTree
      ie. -d <currentvalue:newvalue:find/findall>
  * Implement a prepared variable substitution ability within the mapfile.
  * Map draw looping n times
  * Cascadenik integration | ability to read in css.mml or css.mss.
  * Allow for setting the path to datasources.
  
"""

__author__ = "Dane Springmeyer (dbsgeo [ -a- ] gmail.com"
__copyright__ = "Copyright 2008, Dane Springmeyer"
__version__ = "0.1 $Rev: 1 $"
__license__ = "GPLv2"

def usage (name):
  print
  color_print(3, "%s" % make_line('=',75))
  color_print(2,"Usage: %s -m <mapnik.xml> -o <image.png>" % name)
  color_print(4,"Option\tDefault\t\tDescription")
  print "-m\t<required>\tMapfile: Path to xml map file to load styles from."
  print "-o\t<required>\tImage: Set the output filename (or a directory name - with no .ext%s)" % color_text(3,'*')
  print "-i\t[png]\t\tFormat: Choose the output format: png, png256, jpeg, or all (will loop through all formats)"
  print "-e\t[max extent]\tMinx,Miny,Maxx,Maxy: Set map extent in geographic (lon/lat) coordinates%s" % color_text(3,'*')
  print "-r\t[max extent]\tMinx,Miny,Maxx,Maxy: Set map extent in projected coordinates of mapfile"
  print "-s\t[600,300]\tWidth,Height: Set the image size in pixels"
  print "-p\t[mapfile srs]\tReproject using epsg, proj4 string, or url 'ie -p http://spatialreference.org/ref/user/6/'%s" % color_text(3,'*')
  print "-l\t[all enabled]\tSet layers to enable (quote and comma-separate if several)"  
  print "-v\t[off]\t\tRun with verbose output"
  print "-c\t[1]\t\tDraw map n number of times" 
  print "-n\t[0]\t\tDry run mode: no map output"
  print "-t\t[0]\t\tPause n seconds after reading the map"
  print "--debug\t[0]\t\tLoop through all formats and zoom levels generating map graphics (more opt later)%s" % color_text(3,'*')
  print "-z\t[10]\t\tN number of zoom levels generate graphics for%s" % color_text(3,'*')
  print "-d\t[None]\t\tFind and replace of any text string within a mapfile (modifies mapfile in memory)"
  print "-h\t[off]\t\tPrints this usage information"
  print "%s\n %s Additional features in nik2img not part of shp2img" % (make_line('-',75), color_text(3,'*'))
  print " %s nik2img does not support sending image to STDOUT (default in shp2img)" % color_text(3,'Note:')
  color_print(3, "%s" % make_line('=',75))
  color_print(7,"Dane Springmeyer, dbsgeo (a-t) gmail.com")
  print

def make_line(character, n):
    line = character*n
    return line

def color_print(color,text):
    """
    1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    """
    print "\033[9%sm%s\033[0m" % (color,text)

def color_text(color,text):
    """
    1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    """
    return "\033[9%sm%s\033[0m" % (color,text)

def output_error(msg, E=None, yield_usage=False):
    if E:
      color_print(1, '// --> %s: \n\n %s' % (msg, E))
    else:
      color_print(1, '\\ --> %s' % msg)    
    if yield_usage:
      usage(sys.argv[0])
    sys.exit(1)

def output_message(msg, warning=False):
    if VERBOSE:
      if warning:
        color_print(1, '// --> WARNING: %s' % msg)    
      else:
        color_print(2, '// --> %s' % msg)
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
          l = mapnik_map.layers[layer_num]
          layer_envelope = l.envelope()
          if map_envelope.intersects(layer_envelope):
              output_message("Map layer '%s' intersects Map envelope" % l.name)
          else:
              output_message("Map layer '%s' does not intersect with Map envelope" % l.name, warning=True)

if __name__ == "__main__":
  import os
  import sys
  import getopt
  import time
  
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
  built_test_outputs = False
  var = {}        # In/Out paths

  try:
    opts, args = getopt.getopt(sys.argv[1:], "m:o:i:e:s:r:p:t:l:z:d:c:nvhq", ['debug'])
  except getopt.GetoptError, err:
    output_error(err,yield_usage=True)
  
  if len(sys.argv) <= 1:
    usage(sys.argv[0])
    sys.exit(1)
  
  for opt, arg in opts:
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
    elif opt == "-s":
        var['s'] = arg
    elif opt == "-l":
        var['l'] = arg   
    elif opt == "-z":
        var['z'] = arg
    elif opt == "-c":
        var['c'] = arg   
    elif opt == "-d":
        var['d'] = arg
    elif opt == "-n":
        DRY_RUN = True
    elif opt == "-v":
        VERBOSE = True
    elif opt == "-q":
        QUIET = True
    elif opt == "--debug":
        built_test_outputs = True
    elif opt == "-h":
        usage(sys.argv[0])
        sys.exit(1)
    
  if len(var) < 2:
    output_error('Make sure to specify the -m <input mapfile.xml> and -o <output image>',yield_usage=True)
  else:
    run = True
    
    if QUIET:
      output_message('Quite mode requested')
      #sys.stderr = open(os.devnull,"w")
      errors = sys.__stderr__.fileno()
      os.close(errors) # suppress the errors, mostly mapnik debug
      #os.dup2(devnull.fileno(), suppressed_errors
      #sys.stdout = open(os.devnull,"w")
    
    try:
        import mapnik
        output_message('Loaded mapnik python bindings')
    except Exception, E:
        output_error('Could not load mapnik python bindings', E)

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

  try:
    mapnik_map = mapnik.Map(WIDTH,HEIGHT)
    output_message('Map object created successfully')
  except Exception, E:
    output_error("Problem initiating map",E)

  if var.has_key('z'):
    levels = var['z']
    try:
      levels= int(levels) + 1
      ZOOM_LEVELS = generate_levels(levels)
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
    # TODO: allow remote mapfile
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
    layers = var['l'].split(",")
    mapfile_layers = mapnik_map.layers
    output_message('Scanning %s layers' % len(mapnik_map.layers))
    for layer_num in range(len(mapnik_map.layers)-1, -1, -1):
          l = mapnik_map.layers[layer_num]
          if l.name not in layers:
              del mapnik_map.layers[layer_num]
              output_message("Removed layer '%s' loaded from mapfile, not in list: %s" % (l.name, layers))

  # TODO: Accept spatialreference.org url
  if var.has_key('p'):
    output_message('Reprojecting map output')
    if var['p'] == "epsg:900913":
      output_message('Google spherical mercator was selected and proj4 string will be used to initiate projection')
      google_merc = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
      epsg = mapnik.Projection(google_merc)
    else:
      epsg = mapnik.Projection("+init=%s" % var['p'])
      output_message("Mapnik projection successfully initiated with epsg code: '%s'" % epsg.params())
    mapnik_map.srs = epsg.params()

  if var.has_key('t'):
    output_message('Pausing for %s seconds...' % var['t'])
    for sec in range(1, int(var['t'])):
      output_message('%s' % sec)
      time.sleep(1)

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
  
  # Check for which layers intersect with map envelope
  layers_in_extent()
  
  # TODO: cleanup this crappy code.
  if DRY_RUN:
    output_error('Dry run complete')

render(*args)
  if var.has_key('c'):
    loop = len(var['c']
    for map in loop:
      mapnik.render_to_file(*args)
  else:
    mapnik.render_to_file(*args)
  
  o = var['o']
  if not is_file(o):
      try:
        os.mkdir(o)
      except OSError:
        output_message('Directory already exists, doing nothing...', warning=True)
      o = '%s/%s.%s' % (o,o,FORMAT)
  if not built_test_outputs:    
    try:
      if var['i'] == 'all':
        o = o.split('.')[0]
        for k, v in AGG_FORMATS.iteritems():
          try:  
            render(mapnik_map,'%s_%s%s' % (o,k,v), k)
          except Exception, E:
            output_error("Error when rendering to file",E)
      elif var['i']:
        render(mapnik_map,o, var['i'])
    except KeyError:
      render(mapnik_map,o,FORMAT)  
    except Exception, E:
      output_error("Error when rendering to file",E)
  else:
    for lev in ZOOM_LEVELS:
      mapnik_map.zoom(lev)
      output_message('%s' % mapnik_map.scale())
      o_name = '%s_level-%s' % (o.split('.')[0],lev)
      try:
        if var['i'] == 'all':
          for k, v in AGG_FORMATS.iteritems():
            try:
              file = '%s_%s%s' % (o_name,k,v)
              color_print (1,file)
              render(mapnik_map,file, k)
            except Exception, E:
              output_error("Error when rendering to file",E)
        elif var['i']:
            render(mapnik_map,o_name, var['i'])
      except KeyError:
        render(mapnik_map,'%s.%s' % (o_name,FORMAT),FORMAT)  
      except Exception, E:
        output_error("Error when rendering to file",E)