#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO - embedding ppi-metadata in exif
# http://tilloy.net/dev/pyexiv2/
# calculate all iso dynamically?
# [sqrt(v[0]*v[1]) for k,v in iso.items()]
# support specifing margins in pixels
# carry through ppi for later use

# dpi, ppi, and metric standards 
# http://en.wikipedia.org/wiki/Dots_per_inch
# http://en.wikipedia.org/wiki/Pixels_per_inch
# http://en.wikipedia.org/wiki/Metric_typographic_units

# dpi myths
# http://www.woram.com/temp/woram.htm
# http://www.scantips.com/no72dpi.html
# http://www.danrichard.com/2006/03/23/to-print-or-not-to-print-making-sense-of-the-dpi-equation/

# paper sizes
# http://www.inkjetart.com/weight.html
# http://en.wikipedia.org/wiki/ISO_216
# http://en.wikipedia.org/wiki/Paper_size

import optparse
import sys
import copy
import math

VERBOSE = False
POSTSCRIPT_POINT = 72 # pixels per inch
STANDARDIZED_PIXEL = 0.28 # mm
PLOTTER_MAX_WIDTH = 36 # inches
POWER_POINT_MAX = (36,56)
MS_WORD_MAX = (11,17)

def error(E,msg):
  if __name__ == '__main__':
    sys.exit('// -- Error: %s' % msg)
  else:
    raise E(msg)

def msg(msg):
 global VERBOSE
 if VERBOSE:
   print msg

# Paper sizes by name/shorthand

# in millimetres
iso = {
  # iso A series
  'A0': (841,1189),
  'A1': (594,841),
  'A2': (420,594),
  'A3': (297,420),
  'A4': (210,297),
  'A5': (148,210),
  'A6': (105,148),
  'A7': (74,105),
  'A8': (52,74),
  'A9': (37,52),
  'A10': (26,37),
  # iso B series
  'B0': (1000,1414),
  'B1': (707,1000),
  'B2': (500,707),
  'B3': (353,500),
  'B4': (250,353),
  'B5': (176,250),
  'B6': (125,176),
  'B7': (88,125),
  'B8': (62,88),
  'B9': (44,62),
  'B10': (31,44),
  # iso C series
  'C0': (917,1297),
  'C1': (648,917),
  'C2': (458,648),
  'C3': (324,458),
  'C4': (228,324),
  'C5': (162,229),
  'C6': (114.9,162),
  'C7': (88,114.9),
  'C8': (57,81),
  'C9': (40,57),
  'C10': (28,40),
  # DIN 476
  '4A0': (1682,2378),
  '2A0': (1189,1682),
  # SIS 014711
  'G5': (169,239),
  'E5': (155,220),
  }

jis = {
  'J0': (1030,1456),
  'J1': (728,1030),
  'J2': (515,728),
  'J3': (364,515),
  'J4': (257,364),
  'J5': (182,257),
  'J6': (128,182),
  'J7': (91,128),
  'J8': (64,91),
  'J9': (45,64),
  'J10': (32,45),
  'J11': (22,32),
  'J12': (16,22),
  }

# inches
ansi = {
  'ANSI-A': (8.5,11),
  'ANSI-B': (11,17),
  'ANSI-C': (17,22),
  'ANSI-D': (22,34),  
  'ANSI-E': (34,44),
  }

# inches
north_america = {
  'letter': (8.5,11),
  'carta': (8.5,11),
  'legal': (8.5,14),
  'oficio': (8.5,14),
  'executive': (7.25,10.5),
  'tabloid': (11,17),
  'ledge': (17,11),
  'government-letter': (8,10.5),
  'chilean-legal': (8.5,13),
  'philippine-legal': (8.5,13),
  
  }

sizes = (
  (north_america,'in'),
  (iso,'mm'),
  (jis,'mm'),
  (ansi,'in'),
  )

# Fetch a size and respective unit
def get_size_by_name(papername):
    """Return the units, width, and height of a given paper size.
    
    Supports lookup of ISO, Japanese, ANSI, and North American sizes.
    """
    u = h = w = None
    up,lo = papername.upper(),papername.lower()
    for size in sizes:      
      if size[0].has_key(lo):
        w,h = size[0][lo]
        u = size[1]
      elif size[0].has_key(up):
        w,h = size[0][up]
        u = size[1]
    if not w:
      error(AttributeError,'Could not find paper size of: %s' % papername)
    msg("%s size found, using unit: '%s'; width: '%s'; height: '%s'" % (papername.upper(),u,w,h))
    if u != 'in':
      factor = get_factor(u)
      w,h = w/factor,h/factor
      #if 
      msg("%s equivalent in inches is: %s, %s" % (papername.upper(),w,h))
    return u,w,h

# Basic resolution conversions

def print_scale(ppi):
    """Return the scale factor to print a given ppi at the mythical 'standard' resolution.
    """
    return POSTSCRIPT_POINT/ppi * 100
    
def ppi2microns(ppi):
    """Convert ppi to µm
    """
    return 25400.0/ppi

# 76dpi (postcript) translates to a resolution of 334.21 microns
# http://www.cl.cam.ac.uk/~mgk25/metric-typo/
def microns2ppi(microns):
    """Convert µm to ppi
    """
    return 25400.0/microns

# Factor for converting to inches by division
# read this as 1 inch == unit value
inch_eq = {
  'ft': 0.0833333333,
  'yd': 0.0277777778,
  'in' : 1,
  'm': 0.0254,
  'dm': 0.254,
  'cm': 2.54,
  'mm': 25.4,
  'um': 25400.0,
  'px': POSTSCRIPT_POINT,
  }
upper_inch_eq = dict([(k.upper(), v) for k, v in inch_eq.items()])

alias = {
  'centimeter' : 'cm',
  'foot' : 'ft',
  'inch' : 'in',
  'kilometer' : 'km',
  'kilometre' : 'km',
  'meter' : 'm',
  'metre' : 'm',
  'millimeter' : 'mm',
  'millimetre' : 'mm',
  'mile' : 'mi',
  'yard' : 'yd',
  }
upper_alias = dict([(k.upper(), v) for k, v in alias.items()])

def get_factor(unit):
    """Return the conversion factor to inches for a given unit.
    """
    if inch_eq.has_key(unit):
        return inch_eq[unit]
    elif upper_inch_eq.has_key(unit):
        return inch_eq[upper_inch_eq[unit]]
    elif alias.has_key(unit):
        return inch_eq[alias[unit]]
    elif upper_alias.has_key(unit):
        return inch_eq[upper_alias[unit]]
    else:
        error(AttributeError,'Unknown unit type: %s' % unit)

def get_px_screen_density(pixels_wide=1440,pixels_high=900,screen_width=15.4):
    """Return the pixels per unit (density) for a given display resolution and width.
    """
    pixel_density = math.sqrt(pixels_wide**2 + pixels_high**2)/screen_width
    msg("Screen pixel density: '%s'" % pixel_density)
    return pixel_density

def get_px_for_print_size(unit,print_w,print_h,print_res,res_unit):
    """Return the pixel width and height given a target print size.
    """
    # get the conversion factor to inches
    factor = get_factor(unit)
    if res_unit == 'microns':
      # convert microns to inches since our print sizes
      # are going to be forced into inch units
      msg("Setting resolution using micrometres (µm)... to '%s' µm" % print_res)
      print_res = microns2ppi(print_res)
      msg("Micron value equivalent to '%s' ppi" % print_res)
    elif res_unit == 'inches':
      microns = ppi2microns(print_res)
      msg("Setting resolution using inches... to '%s' ppi" % print_res)
      msg("Per inch resolution equivalent to pixel size of '%s' microns" % microns)
    else:
      error(AttributeError,'Unknown print resolution type: %s' % res_unit)
    px_w = print_w/factor*print_res
    px_h = print_h/factor*print_res
    return px_w,px_h

def get_pixels(unit,w,h,print_res=300,res_unit='inches',margin=0,layout=None,**kwargs):
    """Return the pixel width and height given a target resolution, margin, and layout.
    """
    if margin:
      w,h = w-margin,h-margin
      msg("Margin requested, dimensions in '%s' now: %s,%s " % (unit,w,h))
    px_w, px_h = get_px_for_print_size(unit,w,h,print_res,res_unit)
    if layout:
      dim = [px_w, px_h]
      dim_copy = copy.copy(dim)
      if layout == 'portrait':
        dim.sort()
        if dim_copy == dim:
          msg('Layout already of portrait orientation...')
        else:
          msg('Switched to Portrait type orientation...') 
        return tuple(dim)
      elif layout == 'landscape':
        dim.sort()
        dim.reverse()
        if dim_copy == dim:
          msg('Layout already of landscape orientation...')
        else:
          msg('Switched to Landscape type orientation...')          
        return tuple(dim)
    else:
      return px_w,px_h
      #return int(px_w),int(px_h)

def print_map_by_dimensions(params,**kwargs):
    """Return the pixels given user defined dimensions and units.
    """
    try:
      w,h,unit = params.split(',')
    except ValueError: # assume inches for now...
      unit = 'in'
      w,h = params.split(',')
    return get_pixels(unit,float(w),float(h),**kwargs)

def print_map_by_name(papername,**kwargs):
    """Return the pixels given a known, named paper size.
    """
    unit,w,h = get_size_by_name(papername)
    return get_pixels(unit,w,h,**kwargs)


parser = optparse.OptionParser(usage="""python print2pixel.py <papersize> [options]

Usage:
    $ python print2pixel.py tabloid -r 300 -u inches
    $ python print2pixel.py letter -u inches -r 76
    $ python print2pixel.py letter -u microns -r 334.21

""")

parser.add_option('-r', '--resolution',
    dest='print_res', type='float',
    help='Specify the desired resolution in ppi (pixels per inch) of micron (size of pixel)')
parser.add_option('-u', '--units',
    dest='res_unit',
    help='Specify the units as either inches or microns')
parser.add_option('-m', '--margin',
    dest='margin', type='float',
    help='Paper margin in the units of the paper size')
parser.add_option('-l', '--landscape',
    action='store_const', const='landscape', dest='layout',
    help='Force lanscape orientation')
parser.add_option('-p', '--portrait',
    action='store_const', const='portrait', dest='layout',
    help='Force portrait orientation')
parser.add_option('-v', '--VERBOSE',
    action='store_true', dest='VERBOSE',
    help='VERBOSE debug output')
parser.add_option('-s', '--screen',
    action='store_const', const=True, dest='screen_res',
    help='Set the --resolution to the PPI of your screen')
parser.add_option('-w', '--screenwidth',
    dest='screen_width', type='float',
    help='Screen width in inches')
parser.add_option('-d', '--displaypixels',
    dest='display_res',
    help='Display pixels as w,h')
parser.add_option('--render',
    action='store_const', const=True, dest='render',
    help='Render the result using nik2img')

if __name__ == '__main__':
    (options, args) = parser.parse_args()

    size = args[0]
    
    if len(args) < 1:
      sys.exit('\nPlease provide a named paper size\n')

    if options.print_res and not options.res_unit:
      sys.exit('\nPlease provide a unit for the resolution value\n')

    if options.res_unit and not options.print_res:
      if not options.screen_res:
        sys.exit('\nPlease provide a resolution value in addition to the respective unit\n')
    
    USE_MACBOOK = True
    if options.screen_res:
      if USE_MACBOOK:
        options.print_res = get_px_screen_density()
      elif not options.res_unit or not options.screen_width or not options.display_res:
        sys.exit('\nPlease provide a screen width in inches, and the display resolution\n')        
      else:
        try: 
          p_w, p_h = map(float,options.display_res.split(','))
        except ValueError:
          sys.exit('Problem setting the display resolution\n')
        options.print_res = get_px_screen_density(pixels_wide=p_w,pixels_high=p_h,screen_width=options.screen_width)

    if options.VERBOSE:
      VERBOSE = True
      print

    kwargs = {}
    for k,v in vars(options).items():
      if v != None:
       kwargs[k] = v

    if len(size.split(','))> 1:
      result = print_map_by_dimensions(size, **kwargs)
    else:
      result = print_map_by_name(size, **kwargs)

    print '// --  Pixel Width: %s' % result[0]
    print '// --  Pixel Height: %s' % result[1]

    if options.render:
      import nik2img
      m = nik2img.Map('mapfile.xml','test.png',width=result[0],height=result[1])
      m.open()

