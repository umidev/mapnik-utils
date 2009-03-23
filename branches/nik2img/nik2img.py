#!/usr/bin/env python

import os
import sys
from pdb import set_trace
from timeit import time
from optparse import OptionParser

version = '0.2.3'

from mapnik_utils import Compose
    
def color_print(color,text,no_color=False):
    """
    Accepts an integer key for one of several color choices along with the text string to color
      keys = 1:red, 2:green, 3:yellow, 4: dark blue, 5:pink, 6:teal blue, 7:white
    Prints a colored string of text.
    """
    if not os.name == 'nt' and not no_color:
        print "\033[9%sm%s\033[0m" % (color,text)
    else:
        print text

def color_text(color, text,no_color=False):
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

        self.timing_started = False
        self.step_counter = 0
        self.start_time = 0
        self.versbose = True

        Compose.__init__(self,mapfile,**kwargs)

    def setup(self):
        if self.trace and not self.verbose:
            self.verbose = True
            self.debug_msg('PDB trace requested, automatically entering verbose mode')

    def prepare(self):
        super(ComposeDebug,self).prepare()
        self.timing_started = True
        self.start_time = time.time()
        self.debug_msg('format: %s' % self.format)
        self.debug_msg('mime: %s' % self.mime)

    def build(self):
        self.debug_msg('Building map...')
        super(ComposeDebug,self).build()
        self.debug_msg('srs: %s' % self.map.srs)
        if self.map.proj_obj.srid:
            self.debug_msg('srid: %s' % self.map.proj_obj.srid)
        if self.layers:
            self.debug_msg('active layers: %s' % self.map.active_layers())
        self.debug_msg('center: %s' % self.map.envelope().center())
        self.debug_msg('envelope: %s' % self.map.envelope())
        self.debug_msg('layers bounds: %s' % self.map.layers_bounds())
        
    def render(self):
        if not self.map:
            self.debug_msg('Calling build from render...')
        self.debug_msg('Rendering...')            
        super(ComposeDebug,self).render()

    def register_fonts(self,fonts):
        super(ComposeDebug,self).register_fonts(fonts)
        if self.font_handler.added:
            self.debug_msg("Registered: '%s'" % f.added)
        elif self.font_handler.failed:
            self.debug_msg("Available fonts are: '%s'" % self.font_handler.available,warn=True)
      
    def output_error(msg, E=None):
        sys.stderr.write(color_text(1, '// --> %s: \n\t %s' % (msg, E),self.no_color))
        sys.exit(1)

    def msg(self, msg, warn=False, print_time=True):
        self.debug_msg(msg,warn=True,print_time=False)

    def debug_msg(self, msg, warn=False, print_time=True):
        """
        Output a colored message or warning, incrementing the step_counter
        to enable a pdb trace to be set at any point a verbose message is printed.
        """
        color = 4
        if warn:
            color = 1
        if self.verbose:
            text = 'Step: %s // --> %s\n' % (self.step_counter, msg)
            sys.stderr.write(color_text(color,text,self.no_color))
            self.output_time(print_time)
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
    
    def elapsed(self, last_step):
        """
        Return the full and incremental elasped time.
        """
        total = (time.time() - self.start_time)
        last = (time.time() - last_step)
        return 'Total time: %s | Last step: %s' % (self.get_time(round(total,4)), self.get_time(round(last,8)))
    
    def output_time(self, print_time):
        """
        Timing output wrapper to control the start point and verbosity of timing output.
        """
        if self.timing_started and print_time:
            val = color_text(4,self.elapsed(time.time()),self.no_color)
            sys.stderr.write('%s\n' % val)

parser = OptionParser(usage="""%prog <mapfile> [options]

Example usage:
    $ %proj --help (for possible options)
    $ %prog mapfile.xml image.png
    $ %prog mapfile.xml > image.png

""", version='%prog ' + '%s' % version)

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

# tilecache and osm2pgsql use -b
# should we assume lon/lat, geographic?
parser.add_option('-b','--bbox', dest='bbox',
                  type='float', nargs=4,
                  help='Geographical bounding box. Two long,lat pairs e.g. -124.731422 24.955967 -66.969849 49.371735',
                  action='store')

parser.add_option('-c', '--center', dest='center', nargs=2,
                  help='Center Coordinate. A long,lat pair e.g.: -122.263 37.804', type='float',
                  action='store')

parser.add_option('-z', '--zoom', dest='zoom',
                  help='Zoom level', type='int',
                  action='store')

parser.add_option('-r', '--radius', dest='radius',
                  help='Zoom to radius (in map units) around center', type='float',
                  action='store')

parser.add_option('--zoom-to-layers', dest='zoom_to_layers',
                  help='Zoom to combined extent of one ore more listed layers by name (comma separated)',
                  type='string', # actually results in a comma-delimited list
                  action='callback',
                  callback=make_list)
                  
parser.add_option('-e', '--projected-extent', dest='extent', nargs=4,
                  help='Projected envelope/extent. Two coordinate pairs in the projection of the map', type='float',
                  action='store')

parser.add_option('-m', '--max-extent', dest='max_extent', nargs=4,
                  help='Projected envelope/extent. Two coordinate pairs in the projection of the map', type='float',
                  action='store')
                  
parser.add_option('-s', '--srs',
                  dest='srs',
                  help="Spatial reference system to project the image into - accepts either <epsg:code>, <proj4 literal>, or a url like 'http://spatialreference.org/ref/sr-org/6")

parser.add_option('-d', '--dimensions', dest='dimensions', nargs=2,
                  help='Pixel dimensions of image (width,height)', type='int',
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
                  help="Georeference the image by providing a worldfile output extension ( ie 'wld')")

parser.add_option('-x', '--xml', dest='save_map',
                  help='Serialize the map to xml.')

parser.add_option('-a', '--app', dest='app',
                  help='Application to open the resulting image.')

parser.add_option('--profile', dest='profile',
                  action='store_true', default=False,
                  help='Output a cProfile report')


# todo
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

parser.add_option('--fonts',
                  type='string', # actually results in a comma-delimited list
                  help='List of paths to .ttf or .otf fonts to register (comma separated)',
                  action='callback',
                  callback=make_list)
    
if __name__ == '__main__':
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.error(color_text(1,'\n\nPlease provide the path to a mapnik xml or cascadenik mml file\n',options.no_color))
    else:
        mapfile = args[0]
        if len(args) > 1:
            options.image = args[1]
        else:
            options.image = None
           
    options.width, options.height = options.dimensions

    def main():
        nik_map = ComposeDebug(mapfile,**options.__dict__)
        if not options.no_open:
            if options.image:
                nik_map.open()
            else:
                nik_map.render()
    
    if options.profile:
        import cProfile
        cProfile.run('main()', sort=1)
    else:
        main()