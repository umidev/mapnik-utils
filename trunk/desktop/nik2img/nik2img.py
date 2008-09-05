#!/usr/bin/env python

'''
 ToDo
  * Code comments
  * Support cairo formats
  * Built in testing framework
  * Support variable substitution
  * Support verbose output
  * Cascadenik integration
'''

def usage (name):
  print
  color_print(3, "===========================================================================")
  color_print(2,"Usage: %s -m <mapnik.xml> -o <image.png>" % name)
  color_print(4,"-option\tstatus\t\t\tdescription")
  print "-m\t<required>\t\tMapfile: Path to xml map file to load styles from."
  print "-o\t<required>\t\tImage: Set the output filename"
  print "-i\t[default: png]\t\tFormat: Choose the output format (all, png, png256, jpeg)"
  #print "-e\t[default: max extent]\tMinx,Miny,Maxx,Maxy: Set the extents to render"
  print "-s\t[default: 600,300]\tWidth,Height: Set the image size in pixels"
  #print "-d\tDatavalue[default: None]: Switch out a value, ie override the projection"
  #print "-v\t[default:off]\t\tRun with verbose output"
  print "-h\t[default:off]\t\tPrints this usage information"
  color_print(3, "===========================================================================")
  color_print(7,"Dane Springmeyer, dbsgeo a-t gmail.com")
  print

def color_print(color,text):
    """
    1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    """
    print "\033[9%sm%s\033[0m" % (color,text)
    
def output_error(msg, usage=False):
    color_print(1, '// --> %s' % msg)
    if usage:
      usage(sys.argv[0])
    sys.exit(1)

if __name__ == "__main__":
  import sys, getopt
  
  WIDTH = 600
  HEIGHT = 300
  AGG_FORMATS = {'png':'.png','png256':'.png','jpeg':'.jpg'}
  
  run = False  
  run_verbose = False
  var = {}        # In/Out paths

  try:
    opts, args = getopt.getopt(sys.argv[1:], "m:o:i:e:s:d:vh")
  except getopt.GetoptError, err:
    output_error(err,usage=True)
  
  if len(sys.argv) <= 1:
    output_error('Too few arguments',usage=True)
  
  for opt, arg in opts:
    if opt == "-m":
         var['m'] = arg
    elif opt == "-o":
        var['o'] = arg
    elif opt == "-i":
        var['i'] = arg
    elif opt == "-e":
        var['e'] = arg
    elif opt == "-s":
        var['s'] = arg
    #elif opt == "-d":
        #var['d'] = arg        
    #elif opt == "-v":
        #run_verbose = True
    elif opt == "-h":
        usage(sys.argv[0])
        sys.exit(1)
    
  if len(var) < 2:
    output_error('Make sure to specify the -m <input mapfile.xml> and -o <output image>',usage=True)
  else:
    run = True
    import os
    
    try:
        import mapnik
        color_print (4,'Loading mapnik python bindings...')
    except:
        output_error('Could not load mapnik python bindings')

  try:
    xml = open(var['m'], "r");
    print "//-- Confirmed path to XML file: %s" % var['m']
    xml.close()
  except IOError:
    output_error("Cannot open XML file: %s" % var['m'])

  #try:
    #image = open(var['o'], "wb")
    #print "Touched output image: %s" % var['o']
  #except:
    #output_error("Cannot create output image: %s" % var['o'])

  if not run:
    sys.exit(1)

  try:
    if var['s']:
      WIDTH,HEIGHT = var['s'].split(',')
  except: pass
  
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

  try:    
    mapnik.load_map(mapnik_map, var['m'])  
  except Exception, E:
    output_error("Problem loading map",E)

  try:    
    mapnik_map.zoom_all()
  except Exception, E:
    output_error("Problem Zooming to all layers",E)

  try:
    if var['i'] == 'all':
      o = var['o'].split('.')[0]
      for k, v in AGG_FORMATS.iteritems():
        try:  
          mapnik.render_to_file(mapnik_map,'%s_%s%s' % (o,k,v), k)
        except Exception, E:
          output_error("Error when rendering to file",E)
    elif var['i']:
      mapnik.render_to_file(mapnik_map,var['o'], var['i'])
  except KeyError:
    mapnik.render_to_file(mapnik_map,var['o'])  
  except Exception, E:
    output_error("Error when rendering to file",E)