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
  * Add query mode, which will output mapfile stuff and not render map.
  * Add ability to load alternative fonts (perhaps do automatically if found in mapfile?)
  * Need to check if removed layers were active or inactive
  * Further test the zoom resolutions feature (not sure about mapniks starting scale)
  * Add ability to set specific resolutions for ZOOM_LEVELS with flag
  * Refactor into a single function when run as main.
  * Support cairo renderer and formats.
  * Add a verbose output setting with timing tests and mapfile debugging.
  * Refactor debug to shp2img setting of debug type: graphics, zooms, times, mapfile, layers, all, etc.
  * Implement variable substitution within the mapfile.
  * Map draw looping
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
  #print "-v\t[off]\t\tRun with verbose output"
  #print "-c\t[1]\t\tDraw map n number of times" 
  print "-t\t[0]\t\tPause n seconds after reading the map"
  print "--debug\t[0]\t\tLoop through all formats and zoom levels generating map graphics (more opt later)%s" % color_text(3,'*')
  print "-z\t[10]\t\tN number of zoom levels generate graphics for%s" % color_text(3,'*')
  #print "-d\tDatavalue[None]: Variable substitution, ie find and replace any value within mapfile"
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
      color_print(1, '// --> %s' % msg)    
    if yield_usage:
      usage(sys.argv[0])
    sys.exit(1)

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

if __name__ == "__main__":
  import os
  import sys
  import getopt
  import time
  
  WIDTH = 600
  HEIGHT = 300
  AGG_FORMATS = {'png':'.png','png256':'.png','jpeg':'.jpg'}
  ZOOM_LEVELS = generate_levels(10)
  FORMAT = 'png'
  run = False  
  run_verbose = False
  built_test_outputs = False
  var = {}        # In/Out paths

  try:
    opts, args = getopt.getopt(sys.argv[1:], "m:o:i:e:s:d:r:p:t:l:z:vh", ['debug'])
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
    #elif opt == "-c":
        #var['c'] = arg   
    #elif opt == "-d":
        #var['d'] = arg        
    #elif opt == "-v":
        #run_verbose = True
    elif opt == "--debug":
        built_test_outputs = True
    elif opt == "-h":
        usage(sys.argv[0])
        sys.exit(1)
    
  if len(var) < 2:
    output_error('Make sure to specify the -m <input mapfile.xml> and -o <output image>',yield_usage=True)
  else:
    run = True
    import os
    
    try:
        import mapnik
        color_print (4,'Loading mapnik python bindings...')
    except Exception, E:
        output_error('Could not load mapnik python bindings', E)

  try:
    xml = open(var['m'], "r");
    print "//-- Confirmed path to XML file: %s" % var['m']
    xml.close()
  except IOError, E:
    output_error("Cannot open XML file: %s" % var['m'], E)

  if not run:
    sys.exit(1)

  if var.has_key('s'):
    WIDTH,HEIGHT = var['s'].split(',')
  
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
  except Exception, E:
    output_error("Problem initiating map",E)

  if var.has_key('z'):
    levels = var['z']
    try:
      levels= int(levels) + 1
    except Exception, E:
      output_error("Zoom level number must be an integer",E)
    ZOOM_LEVELS = generate_levels(levels)
      
  try:    
    mapnik.load_map(mapnik_map, var['m'])  
  except Exception, E:
    output_error("Problem loading map",E)

  if var.has_key('t'):
    time.sleep(float(var['t']))

  if var.has_key('l'):
    layers = var['l'].split(",")
    mapfile_layers = mapnik_map.layers
    for layer_num in range(len(mapnik_map.layers)-1, -1, -1):
          l = mapnik_map.layers[layer_num]
          if l.name not in layers:
              del mapnik_map.layers[layer_num]
              color_print (6, "Removed layer %s loaded from mapfile, not in list: %s" % (l.name, layers))

  # TODO: Accept spatialreference.org url
  if var.has_key('p'):
    if var['p'] == "epsg:900913":
      google_merc = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
      epsg = mapnik.Projection(google_merc)
    else:
      epsg = mapnik.Projection("+init=%s" % var['p'])
    mapnik_map.srs = epsg.params()

  #TODO: refactor zoom function
  if var.has_key('e'):
    try:
      bbox = [float(x) for x in var['e'].split(",")]
      bbox = mapnik.Envelope(*bbox)
      p = mapnik.Projection("%s" % mapnik_map.srs)
      if not p.geographic:
        print '// -- Initialized projection: %s' % p.params()
        bbox = mapnik.forward_(bbox, p)
    except Exception, E:
       output_error("Problem setting geographic bounding box", E)
    mapnik_map.zoom_to_box(bbox)
  elif var.has_key('r'):
    try:
      bbox = [float(x) for x in var['r'].split(",")]
      bbox = mapnik.Envelope(*bbox)
    except Exception, E:
       output_error("Problem setting projected bounding box", E)
    mapnik_map.zoom_to_box(bbox)
  else:
    try:    
      mapnik_map.zoom_all()
    except Exception, E:
      output_error("Problem Zooming to all layers",E)
  
  # TODO: cleanup this crappy code.
  o = var['o']
  if not is_file(o):
      try:
        os.mkdir(o)
      except OSError:
        color_print(1,'// -- Directory already exists, doing nothing...')
      o = '%s/%s.%s' % (o,o,FORMAT)
  if not built_test_outputs:    
    try:
      if var['i'] == 'all':
        o = o.split('.')[0]
        for k, v in AGG_FORMATS.iteritems():
          try:  
            mapnik.render_to_file(mapnik_map,'%s_%s%s' % (o,k,v), k)
          except Exception, E:
            output_error("Error when rendering to file",E)
      elif var['i']:
        mapnik.render_to_file(mapnik_map,o, var['i'])
    except KeyError:
      mapnik.render_to_file(mapnik_map,o,FORMAT)  
    except Exception, E:
      output_error("Error when rendering to file",E)
  else:
    for lev in ZOOM_LEVELS:
      mapnik_map.zoom(lev)
      print mapnik_map.scale()
      o_name = '%s_level-%s' % (o.split('.')[0],lev)
      try:
        if var['i'] == 'all':
          for k, v in AGG_FORMATS.iteritems():
            try:
              file = '%s_%s%s' % (o_name,k,v)
              color_print (1,file)
              mapnik.render_to_file(mapnik_map,file, k)
            except Exception, E:
              output_error("Error when rendering to file",E)
        elif var['i']:
            mapnik.render_to_file(mapnik_map,o_name, var['i'])
      except KeyError:
        mapnik.render_to_file(mapnik_map,'%s.%s' % (o_name,FORMAT),FORMAT)  
      except Exception, E:
        output_error("Error when rendering to file",E)