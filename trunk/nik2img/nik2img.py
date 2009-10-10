#!/usr/bin/env python

import os
import sys
import tempfile
from timeit import time
from pdb import set_trace
from optparse import OptionParser

__version__ = '0.4.0'
__author__ = 'Dane Springmeyer (dbsgeo [ -a- ] gmail.com)'
__copyright__ = 'Copyright 2009, Dane Springmeyer'
__license__ = 'GPLv2'

from mapnik_utils import Compose

def color_print(color, text, no_color=False):
    """
    Accepts an integer key for one of several color choices along with the text string to color
      keys = 1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    Prints a colored string of text.
    """
    if not os.name == 'nt' and not no_color:
        print "\033[9%sm%s\033[0m" % (color,text)
    else:
        print text

def color_text(color, text, no_color=False):
    """
    Accepts an integer key for one of several color choices along with the text string to color
      keys = 1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    Returns a colored string of text.
    """
    if not os.name == 'nt' and not no_color:
        return "\033[9%sm%s\033[0m" % (color,text)
    else:
        return text

class ComposeDebug(Compose):
    """
    """
    def __init__(self,mapfile,**kwargs):
        self.no_color = kwargs.get('no_color')   
        self.pause = kwargs.get('pause')
        self.trace_steps = kwargs.get('trace_steps')
        self.verbose = kwargs.get('verbose')

        self.timing_started = False
        self.step_counter = 1
        self.start_time = 0

        Compose.__init__(self,mapfile,**kwargs)

    def setup(self):
        if self.trace_steps and not self.verbose:
            self.verbose = True
            self.debug_msg('PDB trace requested, automatically entering verbose mode')

    def prepare(self):
        super(ComposeDebug,self).prepare()
        self.timing_started = True
        self.start_time = time.time()
        self.debug_msg('Nik2img starting...')
        self.debug_msg('Format: %s' % self.format)
        #self.debug_msg('mime: %s' % self.mime)

    def build(self):
        try:
            builder = super(ComposeDebug,self).build()
        except Exception, E:
            self.output_error(E)        
        self.last_step('Loading map took... ', builder.load_map_time)
        if self.verbose:
            self.debug_msg('SRS: %s' % self.map.srs)
            if self.map.proj_obj.srid:
                self.debug_msg('SRID: %s' % self.map.proj_obj.srid)
            self.debug_msg('Map extent: %s' % self.map.envelope())
            self.debug_msg('Map long/lat bbox: %s' % self.map.lon_lat_bbox())
            self.debug_msg('Map center: %s' % self.map.envelope().center())
            self.debug_msg('Map long/lat center: %s' % self.map.lon_lat_bbox().center())
            self.debug_msg('Map scale denominator: %s' % self.map.scale_denominator())
            if self.layers:
                self.debug_msg('Active layers: %s' % self.map.active_layers())
            if self.map.layers_bounds():
                self.debug_msg('Extent of all layers: %s' % self.map.layers_bounds())
                self.debug_msg('Long/lat extent of all layers: %s' % self.map.lon_lat_layers_bounds())
                self.debug_msg('Long/lat center of all layers: %s' % self.map.lon_lat_layers_bounds().center())
    
            lyrs = self.map.intersecting_layers()
            if not len(lyrs):
                self.debug_msg("No layers intersecting map!",warn=True)
            else:
                self.debug_msg("Layers intersecting map: [%s]" % ', '.join([l.name for l in lyrs]))
            self.debug_msg("At current scale of '%s'..." % self.map.scale())
            for lyr in lyrs:
                if not l.visible(self.map.scale()):
                    self.debug_msg("Layer '%s' is NOT visible" % lyr.name,warn=True)
                else:
                    self.debug_msg("layer '%s' is visible" % lyr.name)
                # crashing in filter on os x...
                #    rules = ', '.join(['%s:%s (%s -> %s)' % (r.parent,str(r.filter)[:10],r.min_scale,r.max_scale) for r in lyr.active_rules])
                #    self.debug_msg('active rules for %s: %s' % (l.name,rules))
                
        
    def render(self):
        if not self.map:
            self.debug_msg('Calling build from render...')
        self.debug_msg('Starting rendering...')            
        try:
            renderer = super(ComposeDebug,self).render()
        except Exception, E:
            self.output_error(E)
        self.last_step('Rendering image took... ', renderer.render_time)
        self.debug_msg('Finished rendering map to... %s' % self.image)
        self.total_time()

    def register_fonts(self):
        super(ComposeDebug,self).register_fonts()
        if len(self.font_handler.added):
            self.debug_msg("Registered: '%s'" % self.font_handler.added)
        elif len(self.font_handler.failed):
            self.debug_msg("Available fonts are: '%s'" % self.font_handler.available,warn=True)
      
    def output_error(self, msg, E=None):
        if E:
            sys.stderr.write(color_text(1, '// --> %s: \n\t %s\n' % (msg, E),self.no_color))
        else:
            sys.stderr.write(color_text(1, '// --> %s \n' % msg,self.no_color))
        sys.exit(1)

    def msg(self, msg, warn=False):
        self.debug_msg(msg,warn=warn)

    def debug_msg(self, msg, warn=False):
        """
        Output a colored message or warning, incrementing the step_counter
        to enable a pdb trace to be set at any point a verbose message is printed.
        """
        color = 2
        if warn:
            color = 1
        if self.verbose:
            text = 'Step: %s // --> %s\n' % (self.step_counter, msg)
            sys.stderr.write(color_text(color,text,self.no_color))
        if self.pause:
            for second in range(1, (int(self.pause)+1)):
                sys.stderr.write('%s ' % color_text(5,second,self.no_color))
                time.sleep(1)
                sys.stderr.flush()
            sys.stderr.write('... \n')
        if self.trace_steps:
            if self.step_counter in self.trace_steps:
                try:
                    print ">>> Entering PDB interpreter (press 'c' to leave)"
                    set_trace()
                except KeyboardInterrupt:
                    pass
        self.step_counter += 1

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
    
    def total_time(self, last_step=None):
        if self.verbose:
            total = (time.time() - self.start_time)
            out = 'Total Nik2img run time: %s' % (self.get_time(round(total,4)))
            if last_step:
                out += '| Last step: %s'% self.get_time(round(last_step,8))
            val = color_text(4,out,self.no_color)
            sys.stderr.write('%s\n' % val)

    def last_step(self,msg,timing):
        if self.verbose:
            out = '%s %s' % (msg, self.get_time(round(timing,4)))
            val = color_text(4,out,self.no_color)
            sys.stderr.write('%s\n' % val)
        
parser = OptionParser(usage="""%prog <mapfile> <image> [options]

Example usage
-------------

Full help:
 $ %prog -h (or --help for possible options)

Read XML, output image:
 $ %prog mapfile.xml image.png

Read MML in verbose mode
 $ %prog mapfile.mml image.png -v

Read MML, pipe to image
 $ %prog mapfile.mml --pipe > image.png

Accept piped XML
$ <xml stream> | %prog image.png

""", version='%prog ' + __version__)

def make_float_list(option, opt, value, parser):
    try:
        values = [float(i) for i in value.split(',')]
    except:
        parser.error("option %s: invalid float values: '%s'" % (opt,value))
    setattr(parser.values, option.dest, values)

def make_int_list(option, opt, value, parser):
    try:
        values = [int(i) for i in value.split(',')]
    except:
        parser.error("option %s: invalid integer values: '%s'" % (opt,value))
    setattr(parser.values, option.dest, values)

def make_list(option, opt, value, parser):
    values = [i.strip() for i in value.split(',')]
    setattr(parser.values, option.dest, values)
    

parser.add_option('-f', '--format', dest='format',
                  help='Format of image: png (32 bit), png256 (8 bit), jpeg, pdf, svg, ps, or all (will loop through all formats).')

parser.add_option('-c', '--center', dest='center', nargs=2,
                  help='Center coordinates. A long,lat pair e.g. -122.3 47.6 (Seattle)',
                  type='float',
                  action='store')

parser.add_option('-z', '--zoom', dest='zoom',
                  help='Zoom level',
                  type='int',
                  action='store')

parser.add_option('-b','--bbox', dest='bbox',
                  type='float', nargs=4,
                  help='Geographical bounding box. Two long,lat pairs e.g. -126 24 -66 49 (United States)',
                  action='store')

parser.add_option('-e', '--projected-extent', dest='extent', nargs=4,
                  help='Projected envelope/extent. Two coordinate pairs in the projection of the map',
                  type='float',
                  action='store')
                  
parser.add_option('-r', '--radius', dest='radius',
                  help='Zoom to radius (in map units) around center',
                  type='float',
                  action='store')

parser.add_option('--zoom-to-layers', dest='zoom_to_layers',
                  help='Zoom to combined extent of one ore more listed layers by name (comma separated)',
                  type='string', # actually results in a comma-delimited list
                  action='callback',
                  callback=make_list)

parser.add_option('-m', '--max-extent', dest='max_extent', nargs=4,
                  help='Projected envelope/extent. Two coordinate pairs in the projection of the map',
                  type='float',
                  action='store')

parser.add_option('--bbox-factor', dest='bbox_factor',
                  type='float',
                  help='Expand or contract final map bounds by factor (positive values will multiple bbox, negative values will divide bbox',
                  action='store')
                                    
parser.add_option('-s', '--srs',
                  dest='srs',
                  help='Spatial reference system to project the image into - accepts either <epsg:code>, <proj4 literal>, or a url like http://spatialreference.org/ref/sr-org/6')

parser.add_option('-d', '--dimensions', dest='dimensions', nargs=2,
                  help='Pixel dimensions of image (width,height)',
                  type='int',
                  default = (600,400),
                  action='store')

parser.add_option('-l', '--layers',
                  type='string', # actually results in a comma-delimited list
                  help='List of layers by name to render (comma separated)',
                  action='callback',
                  callback=make_list)

parser.add_option('-n', '--dry-run', dest='dry_run',
                  help='Construct map but do not render output',
                  action='store_true')

parser.add_option('-w','--world-file',
                  help="Georeference the image by providing a file extention for worldfile output ( ie 'wld')")

parser.add_option('-x', '--xml', dest='save_xml',
                  help='Serialize the map to xml.')

parser.add_option('-a', '--app', dest='app',
                  help='Application to open the resulting image.')

parser.add_option('--profile', dest='profile',
                  action='store_true', default=False,
                  help='Output a cProfile report')

parser.add_option('-v', '--verbose', dest='verbose',
                  help='Make a bunch of noise',
                  action='store_true')
                  
parser.add_option('-p', '--pause', dest='pause',
                  help='Seconds to pause after each step', type='int',
                  action='store')

parser.add_option('-t', '--trace-steps', dest='trace_steps',
                  type='string', # actually results in a comma-delimited list
                  help='Step(s) at which to set a python debugger trace (separated by commas)',
                  action='callback',
                  callback=make_int_list)

parser.add_option('--no-color', dest='no_color',
                  action='store_true', default=False,
                  help='Turn off colored terminal output')

parser.add_option('--no-open', dest='no_open',
                  action='store_true', default=False,
                  help='Skip opening of image in default viewer')

parser.add_option('--pipe', dest='pipe',
                  action='store_true', default=False,
                  help='Pipe image to byte stream instead of writing to file')
                  
parser.add_option('--fonts',
                  type='string', # actually results in a comma-delimited list
                  help='List of paths to .ttf or .otf fonts to register (comma separated)',
                  action='callback',
                  callback=make_list)
    
if __name__ == '__main__':
    (options, args) = parser.parse_args()
    
    if not sys.stdin.isatty():
        xml = sys.stdin.read()
        import mapnik
        if hasattr(mapnik,'load_map_from_string'):
            options.from_string = True
            mapfile = xml
        else:
            options.from_string = False
            (handle, mapfile) = tempfile.mkstemp('.xml', 'mapfile_string')
            os.close(handle)
            open(mapfile, 'w').write(xml)
        if len(args) > 0:
            options.image = args[0]
    elif len(args) == 0:
        parser.error(color_text(4,'\n\nPlease provide the path to a Mapnik xml or Cascadenik mml file\n',options.no_color))
    else:
        mapfile = args[0]
        if len(args) > 1:
            options.image = args[1]
           
    options.width, options.height = options.dimensions
    if not options.format and hasattr(options,'image'):
        if not options.image.endswith('png'):
            try:
                options.format = options.image.split('.')[-1]
            except:
                pass

    def main():
        nik_map = ComposeDebug(mapfile,**options.__dict__)
        if options.no_open:
            nik_map.render()
        else:
            if hasattr(options,'image'):
                nik_map.open()
            else:
                if not options.pipe:
                    parser.error(color_text(4,'\n\nPlease provide the path to an out image.\n',options.no_color))
                else:
                    nik_map.render()
    
    if options.profile:
        import cProfile
        cProfile.run('main()', sort=1)
    else:
        main()
