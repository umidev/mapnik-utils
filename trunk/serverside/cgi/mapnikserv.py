#!/usr/bin/env python

"""
mapnikserv.py (Mapnik SimpleCGI)

Summary:
  A python cgi script for testing and debugging mapnik given a mapnik XML file and basic map variables.

Dependencies:
  Requires Python and Mapnik installed with the python bindings (requires boost +python +icu).
  Pycairo (and cairographics) and Pygments are optional and extend the utility of the script.

Usage:
  Place mapnikserv in your web server directory capable of running cgi scripts.
  Either rename to mapnikserv.cgi or add an Apache directive for your cgi directory like:
    AddHandler cgi-script .cgi .py # add .py
  Make executable (chmod +x mapnikserv.py)
  Then visit http://yourserver/cgi-bin/mapnikserv.py
  A sample mapfile (`mapfile.xml') is located at:
    http://mapnik-utils.googlecode.com/svn/trunk/serverside/cgi/mapfile.xml
  A sample shapefile is located inside:
    http://mapnik-utils.googlecode.com/svn/trunk/sample_data/
  
Limitations: 
  This script offers no support (yet) for reprojections or the development or modification of the mapfile.
  It is not intended for use in a production environment in order to dynamically generate images. 
  The error handling is targeted at humanizing the learning and debugging of mapnik. It can be used
  as a non OGC WMS server, but if that is your goal check out the Mapnik WMS server included in the 
  mapnik source code.

TODO:
  Collect a warnings list that is output whenever an error occurs, such as unhandled wms keys, but that
  will not throw errors
  Fix tile edge-matching problem when used as a WMS server with OpenLayers (until then use singletile mode)
  
"""
__author__ = "Dane Springmeyer (dbsgeo [ -a- ] gmail.com"
__copyright__ = "Copyright 2008, Dane Springmeyer"
__version__ = "0.1 $Rev: 1 $"
__license__ = "GPLv2"

# Python imports
import cgi
import os
import shutil
import sys
import tempfile
import traceback
import urllib

# Pygments (http://pygments.org/) is used for optional syntax highlighting of tracebacks
try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import HtmlFormatter
    HAS_PYGMENTS = True
except:
    HAS_PYGMENTS = False

# If true mapfile, python environment and PYTHONPATH will be displayed (do not use in production environment)
DEBUG = False

# Triggered as True when mapfile is loaded within script, after which mapfile stats will be output
MAPFILE_LOADED = False

# Defaults for query examples/suggestions
MAPFILE = 'mapfile.xml'
BBOX = '-180,-90,180,90'
WIDTH = '1000'
HEIGHT = '500'
MODE = 'view'
FORMAT= 'png' 

def output_headers(content_type, filename = "", length = 0):
  """
  Output HTTP headers
  """
  print "Content-Type: %s" % content_type
  if filename and mode == 'fetch':
    print "Content-Disposition: attachment; filename=\"%s\"" % filename
  if length:
    print "Content-Length: %d" % length
  print ""

def output_file(file):
  """
  Output the contents of a file if svg or pdf download
  """
  if file:
    file.seek(0)
    shutil.copyfileobj(file, sys.stdout)
  else:
    output_error('file empty')
  
# Gt the size of a file
def file_size(file):
  return os.fstat(file.fileno()).st_size

# HTML HEAD and STYLES for error output
query_home = 'http://%s%s?' % (os.environ['SERVER_NAME'], os.environ['SCRIPT_NAME'])
error_top = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en"><head><meta http-equiv="content-type" content="text/html; charset=utf-8"><title>Mapnikserv.py - Mapnik SimpleCGI</title>
 <style type="text/css">
    html * { padding:0; margin:0; }
    body * { padding:10px 20px; }
    body * * { padding:0; }
    body { font:small sans-serif; }
    body>div { border-bottom:1px solid #ddd; }
    h1 { font-weight:normal; }
    h2 { margin: .3em 0 .2em 0; }
    h2 { color:#666; font-weight:normal; }
    h3 { margin:1em 0 .5em 0; }
    h4 { margin:0 0 .5em 0; font-weight: normal; }
    #top { background: #e0ebff; }
    #details { background:#eee; }
    pre { border-right-width: 0px; border-left-width: 0px; border-bottom-width: 2px; border-top-width: 2px; font-family: "DejaVu Sans", Courier, mono; line-height: 16px; border-color:steelblue; border-style: solid; font-size: 11px; margin-bottom: 10px; margin-top: 10px; overflow: auto; padding: 10px; background: #f8f8f9; -moz-border-radius: 2px; -webkit-border-radius: 2px;}
    .highlight .c { color: #999988; font-style: italic } /* Comment */
    .highlight .err { color: #a61717; background-color: #e3d2d2 } /* Error */
    .highlight .k { color: #030788; font-weight: bold } /* Keyword */
    .highlight .o { font-weight: bold } /* Operator */
    .highlight .cm { color: #999988; font-style: italic } /* Comment.Multiline */
    .highlight .cp { color: #999999; font-weight: bold } /* Comment.Preproc */
    .highlight .c1 { color: #999988; font-style: italic } /* Comment.Single */
    .highlight .gd { color: #000000; background-color: #ffdddd } /* Generic.Deleted */
    .highlight .ge { font-style: italic } /* Generic.Emph */
    .highlight .gr { color: #aa0000 } /* Generic.Error */
    .highlight .gh { color: #999999 } /* Generic.Heading */
    .highlight .gi { color: #000000; background-color: #ddffdd } /* Generic.Inserted */
    .highlight .go { color: #888888 } /* Generic.Output */
    .highlight .gp { color: #555555 } /* Generic.Prompt */
    .highlight .gs { font-weight: bold } /* Generic.Strong */
    .highlight .gu { color: #aaaaaa } /* Generic.Subheading */
    .highlight .gt { color: #aa0000 } /* Generic.Traceback */
    .highlight .kc { font-weight: bold } /* Keyword.Constant */
    .highlight .kd { font-weight: bold } /* Keyword.Declaration */
    .highlight .kp { font-weight: bold } /* Keyword.Pseudo */
    .highlight .kr { font-weight: bold } /* Keyword.Reserved */
    .highlight .kt { color: #445588; font-weight: bold } /* Keyword.Type */
    .highlight .m { color: #009999 } /* Literal.Number */
    .highlight .s { color: #bb8844 } /* Literal.String */
    .highlight .na { color: #008080 } /* Name.Attribute */
    .highlight .nb { color: #999999 } /* Name.Builtin */
    .highlight .nc { color: #445588; font-weight: bold } /* Name.Class */
    .highlight .no { color: #ff99ff } /* Name.Constant */
    .highlight .ni { color: #800080 } /* Name.Entity */
    .highlight .ne { color: #990000; font-weight: bold } /* Name.Exception */
    .highlight .nf { color: #990000; font-weight: bold } /* Name.Function */
    .highlight .nn { color: #555555 } /* Name.Namespace */
    .highlight .nt { color: #000080 } /* Name.Tag */
    .highlight .nv { color: #ff99ff } /* Name.Variable */
    .highlight .ow { font-weight: bold } /* Operator.Word */
    .highlight .mf { color: #009999 } /* Literal.Number.Float */
    .highlight .mh { color: #009999 } /* Literal.Number.Hex */
    .highlight .mi { color: #009999 } /* Literal.Number.Integer */
    .highlight .mo { color: #009999 } /* Literal.Number.Oct */
    .highlight .sb { color: #bb8844 } /* Literal.String.Backtick */
    .highlight .sc { color: #bb8844 } /* Literal.String.Char */
    .highlight .sd { color: #bb8844 } /* Literal.String.Doc */
    .highlight .s2 { color: #bb8844 } /* Literal.String.Double */
    .highlight .se { color: #bb8844 } /* Literal.String.Escape */
    .highlight .sh { color: #bb8844 } /* Literal.String.Heredoc */
    .highlight .si { color: #bb8844 } /* Literal.String.Interpol */
    .highlight .sx { color: #bb8844 } /* Literal.String.Other */
    .highlight .sr { color: #808000 } /* Literal.String.Regex */
    .highlight .s1 { color: #bb8844 } /* Literal.String.Single */
    .highlight .ss { color: #bb8844 } /* Literal.String.Symbol */
    .highlight .bp { color: #999999 } /* Name.Builtin.Pseudo */
    .highlight .vc { color: #ff99ff } /* Name.Variable.Class */
    .highlight .vg { color: #ff99ff } /* Name.Variable.Global */
    .highlight .vi { color: #ff99ff } /* Name.Variable.Instance */
    .highlight .il { color: #009999 } /* Literal.Number.Integer.Long */
    
  </style>
</head>
<body><div id="top"><h1><a href=""" + query_home + """>Mapnikserv.py - Mapnik SimpleCGI</a></h1><h2>A serverside map generator and debugger</h2></div>
<div>
"""

# HTML closing DIV after error message
error_tail = """
<div id="details">
<p>For more info see your apache error log file ($ tail -f -n 50 /var/log/apache2/error_log).</p>
</div>
"""
def key(key):
   """
   In a case-insensitive way, check for keys
   """
   if form.has_key(key):
     return True
   elif form.has_key(key.upper()):
     return True
   else:
     return False

def get_key(key):
   """
   In a case-insensitive way, return values
   """
   if form.has_key(key):
     return form.getvalue(key)
   elif form.has_key(key.upper()):
     return form.getvalue(key.upper())
   else:
     return ''

def output_envir():
  """
  Print the mapfile statistics, python environment settings
  and PYTHONPATH if DEBUG =True
  """
  if DEBUG:
    if MAPFILE_LOADED:
      print "</pre><br /><p>MAPFILE STATS:</p><pre>"
      generate_map_stats()
      print '</pre>'
    print "<br /><p>Script Environment Settings:</p>"
    print "<pre><strong>Python %s</strong>" % sys.version
    keys = os.environ.keys()
    keys.sort()
    print os.environ
    for k in keys:
      print "%s\t%s" % (k, os.environ[k])
    paths = sys.path
    print "</pre><br /><p>PYTHONPATH:</p><pre>"
    for path in paths:
      print "%s" % path
    print '</pre>'
  else:
    print '<pre>set DEBUG = True to enable debugging output</pre>'
  print '</body></html>'

def output_traceback(E, message=None):
  """
  Output traceback
  """
  if message:
    print "<h1>%s:</h1>" % message
  print "<h3>Traceback: </h3>"
  error = ["%s\n%s" % (str(E),"".join(traceback.format_tb(sys.exc_traceback)))]
  if HAS_PYGMENTS:
    code = highlight(error[0], PythonLexer(),HtmlFormatter())
    print code
  else:
    print '<pre>'
    print error[0]
    print '</pre>'

def output_error(message, E=None, note=None):
  """
  Report and <pre> formatted error message including
  the traceback (with syntax highlighting if Pygments is
  installed) if the error resulted from an exception
  """
  output_headers("text/html")
  print error_top
  if E:
    output_traceback(E, message=message)
  else:
    print '<h1>%s</h1>' % message
  if note:
    print '<p style="color:red">' + note + '</p>'
  print '</div>' 
  if E:
    print error_tail
  output_envir()
  sys.exit()

def link(href):
  """
  Wrap a query string in html link
  """
  link = '<a href="%s">%s</a>' % (href,href)
  return link

def fetch_query():
  """
  Gather the full string of previous query
  """
  query = 'http://%s%s?%s' % (os.environ['SERVER_NAME'], os.environ['SCRIPT_NAME'],os.environ['QUERY_STRING'])
  return query
  
def rgb2hex(r,g,b):
  """
  Convert Red, Green, And Blue values to HEX
  """
  return '#%02X%02X%02X'%(r,g,b)
  
def generate_map_stats():
  """
  Loop through map object layers, styles, and rules
  printing attributes and counting totals
  """
  styles = []
  num_rules = 0
  num_sym = 0
  print '<b>Map:</b>'
  b = mapnik_map.background
  hex_color = rgb2hex(b.r,b.g,b.b)
  print '\tBackground: &nbsp;&nbsp;<span style="background-color:%s; padding:1.3px">%s</span>' % (hex_color,hex_color)
  print '\tEnvelope: %s' % mapnik_map.envelope()
  print '\tSrs: %s' % mapnik_map.srs
  print '\tScale: %s' % mapnik_map.scale()
  print '\tWidth: %s' % mapnik_map.width
  print '\tHeight: %s' % mapnik_map.height
  for l in mapnik_map.layers:
      print "\n\t<b>Layer</b>: %s"  % l.name
      print '\t\tTitle: <em>%s</em>' % l.title
      print '\t\tAbtract: <em>%s</em>' % l.abstract
      print '\t\tSrs: <em>%s</em>' % l.srs
      if l.datasource:
        print "\t\tEnvelope: <em>%s</em>" % l.envelope()
      else:
        print '\t\tEnvelope: <span style="color:red"><em>Unable to be read</em></span>'      
      print "\t\tMin Zoom: <em>%s</em>" % l.minzoom
      print "\t\tMax Zoom: <em>%s</em>" % l.maxzoom     
      print "\t\tQueryable: <em>%s</em>" % l.queryable
      print "\t\tActive: <em>%s</em>" % l.active
      if not l.datasource:
        print '\t\tDatasource: <span style="color:red"><em>Not Found</em></span>'
        print '\t\t\t<span style="color:darkred">Confirm your relative or absolute path to the datasource in your mapfile</span>'
        print '\t\t\t<span style="color:darkred">Make sure your server has read permissions for the file or directory</span>'
        print '\t\t\t<span style="color:darkred">Note, for shapefiles do not include the .shp extension</span>'
      else:
        print "\t\tDatasource: <em>"
        try:
          for group in l.datasource.describe().split('\n\n'):
            for item in group.split('\n'):
              if item:
                print '\t\t\t%s' % item
        except Exception, E:
          print '<span style="color:red">Datasource listed in mapfile was not able to be read (Script could not parse datasource description)</span>'

          output_traceback(E)
        for s in l.styles:
          print "\n</em>\t\t<b>Style: </b>%s" % s
          styles.append(s)
          style = mapnik_map.find_style(s)
          num_rules += len(style.rules)
          print "\t\t\tRules:"
          for r in style.rules:
              print "\t\t\t\tName: %s" % r.name
              print "\t\t\t\tTitle: %s" % r.title
              print "\t\t\t\tAbstract: %s" % r.abstract
              print "\t\t\t\tFiltered: %s" % r.filter # not working!!
              print "\t\t\t\tUses an Else Filter: %s" % r.has_else()
              print '\t\t\t\tMax Scale: %s' % r.max_scale
              print '\t\t\t\tMin Scale: %s' % r.min_scale
              print '\t\t\t\tSymbolizers: %s' % len(r.symbols)
              num_sym += len(r.symbols)
  print "\n<b>Total number of layers</b>\t\t\t\t%s" % len(mapnik_map.layers)
  print "<b>Total number of styles</b>\t\t\t\t%s" % len(set(styles)) # unique styles
  print "<b>Total number of rules</b>\t\t\t\t%s" % num_rules
  print "<b>Total number of symbolizers</b>\t\t%s" % num_sym
  
def generate_file(format):
  """
  Create SVG or PDF Cairo output for download
  or SVG output as string to view in browser
  """
  try:
    import cairo
  except Exception, E:
    output_error('PyCairo is not installed or available, therefore your cannot write to svg or pdf',E)
  file = tempfile.NamedTemporaryFile()
  if format == "svg":
    surface = cairo.SVGSurface(file.name, mapnik_map.width, mapnik_map.height)
  elif format == "pdf":
    surface = cairo.PDFSurface(file.name, mapnik_map.width, mapnik_map.height)
  try:
    mapnik.render(mapnik_map, surface)
  except Exception, E:
      output_error('Cairo python bindings are installed but mapnik was not properly linked at build time',E,note='try upgrading to the most recent mapnik svn')
  surface.finish()
  if format == "svg" and mode != "fetch":
    output_headers("image/%s+xml" % (format), "map.%s" % (format), file_size(file))
  else:
    output_headers("application/%s" % (format), "map.%s" % (format), file_size(file))
  output_file(file) 
            
def generate_image(format):
  """
  Render png or jpeg image output
  """
  image = mapnik.Image(mapnik_map.width, mapnik_map.height)
  image.background = mapnik.Color("green")
  mapnik.render(mapnik_map, image)
  image_string = image.tostring("%s" % format)
  if format == "png256":
    output_headers("image/png", "map.png", len(image_string))  
  else:
    output_headers("image/%s" % (format), "map.%s" % (format), len(image_string))
  print image_string

def generate_script(format, mapfile):
  """
  Print out a sample script that designed to reproduce
  (for desktop mapping) the output of query string 
  """
  s = '#!/usr/bin/env python\n\n'
  s += '# Generated from this query string:\n'
  s += '# %s\n\n' % os.environ['QUERY_STRING']
  if format == "svg" or format == "pdf":
    s += 'import cairo\n'
  s += 'from mapnik import *\n\n'
  if mapfile_url:
    mapfile = mapfile_url
    map_output = mapfile_url.split('/')[-1].split('.')[0]
  else:
    map_output = mapfile.split('.')[0]
  s += "mapfile = '%s'\n" % mapfile
  if format =="png256":
    s += "map_output = '%s.png'\n" % (map_output)
  else:
    s += "map_output = '%s.%s'\n" % (map_output, format)
  s += "projection = '+proj=latlong +datum=WGS84'\n"
  s += "mapnik_map = Map(%s, %s)\n" % (width, height)
  s += 'load_map(mapnik_map, mapfile)\n'
  s += 'bbox = %s\n' % bbox
  s += 'mapnik_map.zoom_to_box(bbox)\n'
  if format == "svg" or format == "pdf":
    s += "file = open(map_output, 'wb')\n"
    if format == "svg":
      s += 'surface = cairo.SVGSurface(file.name, mapnik_map.width, mapnik_map.height)\n'
    elif format == "pdf":
      s += 'surface = cairo.PDFSurface(file.name, mapnik_map.width, mapnik_map.height)\n'
    s += 'render(mapnik_map, surface)\n'
    s += 'surface.finish()\n'
  elif format == "png256":
    s += "render_to_file(mapnik_map, map_output, 'png256')\n" 
  else:
    s += 'render_to_file(mapnik_map, map_output)\n'
  output_headers("text/plain")
  print s


#
##
####  Begin the CGI Processing  ####
##
#

# Grab the CGI parameters
form = cgi.FieldStorage()

# Check if mapik python bindings are working
try:
    import mapnik
except Exception, E:
    from distutils.sysconfig import get_python_lib
    output_error('Please check your mapnik installation. The Python bindings to mapnik are only available if they are on your PYTHONPATH (%s)' % (get_python_lib()),E)

# Check for a lacking url string and assume a tutorial start at 'script home'
if not form.list:
  query_home += 'map=' + MAPFILE + '&bbox=' + BBOX + '&width=' + WIDTH + '&height=' + HEIGHT + '&format=' + FORMAT + '&mode=' + MODE
  output_error(
"""
  <h1>Congrats, mapnik appears to be properly installed and your cgi script is working<h1>
  <h2>Now you can begin adding values for each of these keys:</h2><br /><br />
  <h4>Use standard query string syntax:  scriptname?key=value&key=value </h4>
  <li>map=path/to/your/mapnik_xml_mapfile | (relative, absolute, or url)</li>
  <li>bbox=min_x,min_y,max_x,max_y | extent (ie for WGS84 projection the whole world is bbox=-180,-90,180,90)</li>
  <li>width=integer_width | in pixels</li>
  <li>height=integer_height | in pixels</li>
  <li>format=png, png256, or jpeg (and svg or pdf if pycairo installed) </li>
  <li>mode=view, fetch (to download), debug, or script (to output a standalone python script to regenerate map)</li><br />
  Here is an example url string: <a href="%s">%s</a> <br /><br />
  <em><b>Note:</b> If you run into any errors while adding parameters you'll be returned to this page with an error message specific to the cgi variable.</em><br /><br />
""" % (query_home, query_home))
  
# Check each query parameter, returning examples if absent and an EOF Exception
try:
    # Check for the cgi keys
    if not key("map"):
      # No mapfile specified
      output_error("No mapfile path specified",note=link(fetch_query()+ '&map=%s' % MAPFILE))
    elif not key("bbox"):
      # No bounding box specified
      output_error("No bounding box specified",note=link(fetch_query()+ '&bbox=%s' % BBOX))
    elif not key("width"):
      # No width specified
      output_error("No width specified <h2>Specify width=integer</h2>",note=link(fetch_query()+ '&width=%s' % WIDTH))
    elif not key("height"):
      # No height specified
      output_error("No height specified <h2>Specify height=integer.</h2>",note=link(fetch_query()+ '&height=%s' % HEIGHT))
    elif not key("format"):
      # No format specified
      output_error("No format specified<br /> Specify either format=png, png256, jpeg, svg, or pdf.",note=link(fetch_query()+ '&format=%s' % FORMAT))

    else:    
      mapfile = str(get_key("map"))
      
      # Check if mapfile is located remotely and attempt to download to temp file
      if mapfile.find('http') > -1:
        mapfile_url = mapfile
        remote_mapfile = urllib.urlopen(mapfile_url).read().replace('\n','')
        tmp = tempfile.NamedTemporaryFile(suffix='.xml', mode = 'w')
        tmp.write(remote_mapfile)
        tmp.flush()
        mapfile = tmp.name
      else:
        mapfile_url = None
      
      # Confirm existance of mapfile on filesystem
      if not os.path.isfile(mapfile):
        output_error("mapfile could not be found at: '%s'" % mapfile)
      
      # Parse Bounding Box items
      try:
       bbox = [float(x) for x in get_key("bbox").split(",")]
       bbox = mapnik.Envelope(*bbox)
      except Exception, E:
       output_error("Problem setting Bounding Box", E)
       
      # Parse the mode of output
      mode = str(get_key("mode"))
      if mode != "fetch" and mode != "view" and mode != "script" and mode != "debug":
        output_error("Specify a mode <h2>mode=fetch to download image, mode=view to view image in the browser, mode=debug to view verbose debugging info, or mode=script to generate a python script to regenerate your map.</h2>",note=link(fetch_query()+ '&mode=%s' % MODE))

      # Make sure width and height are integers
      try:
       width = int(get_key("width"))
      except Exception, E:
       output_error("Problem setting map width dimensions",E)

      try:
       height = int(get_key("height"))
      except Exception, E:
       output_error("Problem setting map height dimensions",E)

      format = get_key("format").lower().replace('image/','')   
      
      # Set a limit on map size
      if width * height > 4000000:
        # Map is too large (limit is approximately A2 size)
        output_error("Map too large: reduce your height and width")

      elif mode == "script":
        generate_script(format, mapfile)

      else:
        # Create map
        try:
         mapnik_map = mapnik.Map(width, height)
        except Exception, E:
         output_error("Problem setting map dimensions",E)
         
        # Load map configuration
        try:
         mapnik.load_map(mapnik_map, mapfile)
         MAPFILE_LOADED = True
        except Exception, E:
         output_error("Mapfile found, but error occurred during loading",E)
         
        # Zoom the map to the bounding box
        try:
         mapnik_map.zoom_to_box(bbox)
        except Exception, E:
         output_error("Problem with bbox",E)
                   
        # Output verbose debugging of mapfile and script status
        if mode == "debug":
          output_error("Verbose Debugging Mode")

        # Render the map
        if format == "png" or format == "png256" or format == "jpeg":
          generate_image(format)
          
        elif format == "svg" or format == "pdf":
          generate_file(format)
        else:
          output_error("Unknown format '%s': Only accepts format=png, png256, jpeg, svg, and pdf" % get_key("format"))
except Exception, E:
    output_error('unknown error at beginning of script!' ,E)