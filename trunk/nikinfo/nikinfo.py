#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Dane Springmeyer (dbsgeo [ -a- ] gmail.com)"
__copyright__ = "Copyright 2009, Dane Springmeyer"
__version__ = "0.0.1SVN"
__license__ = "GPLv2"

import optparse
import sys
import os
import re
from mapnik import Shapefile

def get_attr_list(l):
    pattern = r'(\w+)=(.*)'
    match = re.findall(pattern, l.describe())
    item, idx = [],0
    for x in match:
        if x[0] == 'name' and not x[1] == 'shape':
            attr = {}
            attr['name'] = x[1]
            attr['type'] = match[idx+1][1]
            attr['size'] = match[idx+2][1]
            item.append(attr)
        idx += 1
    return item

map_xml = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE Map>
<Map bgcolor="transparent">
    <Style name="%(name)s_style" srs="%(srs)s">
        <Rule>
            <!--
            <PolygonSymbolizer>
                <CssParameter name="fill">#f2eff9</CssParameter>
            </PolygonSymbolizer>
            -->
            <LineSymbolizer>
                <CssParameter name="stroke">grey</CssParameter>
                <CssParameter name="stroke-width">2</CssParameter>
            </LineSymbolizer>
            <LineSymbolizer>
                <CssParameter name="stroke">steelblue</CssParameter>
                <CssParameter name="stroke-width">1.5</CssParameter>
            </LineSymbolizer>
        </Rule>    
    </Style> 
    <Style name="%(name)s_label_style">
        <Rule>
            <TextSymbolizer name="%(labelfield)s" min_distance="45" spacing="65" max_char_angle_delta="90" placement="line" fill="#1C2237" halo_fill="#E6EBEB" halo_radius="1" face_name="DejaVu Sans Bold" size="11"/>
        </Rule>    
    </Style>
    <Layer name="%(name)s" status="on" srs="%(srs)s">
        <StyleName>%(name)s_style</StyleName>
        <StyleName>%(name)s_label_style</StyleName>
        <Datasource>
            <Parameter name="type">shape</Parameter>
            <Parameter name="file">%(file)s</Parameter>
        </Datasource>
    </Layer>
</Map>
'''

map_python = '''
from mapnik import Map, Layer, Style, Rule, Color, Shapefile
from mapnik import PolygonSymbolizer, LineSymbolizer, TextSymbolizer
from mapnik import render_to_file, save_map

m = Map(256,256)
s,r = Style(), Rule()
r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
r.symbols.append(LineSymbolizer(Color('black'),0.1))
r.symbols.append(TextSymbolizer('%(labelfield)s','DejaVu Sans Book',12,Color('black')))
s.rules.append(r)
m.append_style('%(name)s_style',s)
lyr = Layer('%(name)s')
lyr.datasource = Shapefile(file='%(file)s')
lyr.styles.append('%(name)s_style')
m.layers.append(lyr)
m.zoom_to_box(lyr.envelope())
render_to_file(m, '%(name)s.png')
'''

def proj4_from_osr(shp_dir):
    from osgeo import osr
    srs = osr.SpatialReference()
    prj_file = open(shp_dir+ '.prj','r').read()
    srs.SetFromUserInput(prj_file)
    proj4 = srs.ExportToProj4()
    if not proj4:
        #ERROR 6: No translation for Lambert_Conformal_Conic to PROJ.4 format is known.
        srs.MorphFromESRI()
    proj4 = srs.ExportToProj4()
    if proj4:
        return proj4
    else:
        return None

    
def main(shapefile,xml_only=False,srid=None):
    shp_dir = os.path.abspath(shapefile).split('.shp')[0]
    name = shapefile.split('.shp')[0]
    lyr = Shapefile(file=shp_dir)
    attributes = get_attr_list(lyr)
    info = ''
    labelfield = attributes[0]['name']
    e = lyr.envelope()
    context = {'labelfield':labelfield,'name':name,'file':shp_dir,'e':e,'minx':e.minx,'miny':e.miny,'maxx': e.maxx,'maxy': e.maxy}
    if srid:
        context['srs'] = '+init=epsg:%s' % srid
    else:
        srs = proj4_from_osr(shp_dir)
        if srs:
            context['srs'] = srs
        else:
            context['srs'] = '+proj=latlong +datum=WGS84'
    if not xml_only:
        info = "\nInfo for '%(name)s' shapefile:\nEnvelope: %(e)s\nMaxX, MaxY, MinX, MinY: %(minx)s%(miny)s%(maxx)s%(maxy)s" % (context)
        info += '\nAttributes:\n'
        for attr in attributes:
          for k,v in attr.items():
            info += '\t%s      %s|  ' % (k,v)
          info += '\n'
        info += '\nSample Python:\n'
        info += map_python % (context)
        info += '\nSample XML:\n'
    if info:
        print info
    print map_xml % (context)
    
if __name__ == '__main__':
    parser = optparse.OptionParser(usage="""nikinfo.py <shapefile>""")
    
    parser.add_option('--xml',
        action='store_const', const=True, dest='xml_only',
        help='Only output sample XML')

    parser.add_option('--srid',
        type='int', dest='srid',
        help='Provide an epsg code for the srs')
                
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
      parser.error('Please specify a shapefile to query')
    else:
      main(args[0],options.xml_only,options.srid)
