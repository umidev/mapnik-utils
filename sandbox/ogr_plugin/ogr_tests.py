#!/usr/bin/env python

from mapnik import *
from glob import glob
import os

def guess_style(name,filename):
    s, r = Style(), Rule()
    line = LineSymbolizer(Color('black'),.5)
    poly = PolygonSymbolizer(Color('steelblue'))
    point = PointSymbolizer()
    if filename.find('collection') > -1:
      r.symbols.append(line)
      r.symbols.append(poly)
      r.symbols.append(point)
    elif filename.find('poly') > -1:
      r.symbols.append(line)
      r.symbols.append(poly)
    elif filename.find('line') > -1:
      r.symbols.append(line)
    elif filename.find('point') > -1:
      r.symbols.append(point)
    else: # assume polygon data...
      r.symbols.append(line)
      r.symbols.append(poly)
    s.rules.append(r)
    return name, s

def text_style(name,field,font='DejavVu Sans Book',size=11,color='black'):
    s, r, color_obj = Style(), Rule(), Color(color)
    text = TextSymbolizer(field,font,size,color_obj)
    r.symbols.append(text)
    s.rules.append(r)
    return name, s

def ogr_layer(filename,layername=None):
    global m
    if not layername:
        layername = filename.split('.')[0].split('/')[1]
    named_style = filename + '_sty'
    m.append_style(*guess_style(named_style,filename))
    lyr = Layer(filename)
    lyr.datasource = Ogr(file=filename,layer=layername)
    lyr.styles.append(named_style)
    return lyr
    
    
def render_ds(ds):
    global m
    ds_list = glob('data/*.%s' % ds)
    for shape in ds_list:
        layername = None
        #shape = shape.split('/')[1]
        if shape.endswith('.geojson'):
            layername = 'OGRGeoJSON'
        if shape.endswith('.gpx'):
            #layername = ['route_points','track_points','routes']
            layername = 'routes'
        if type(layername) == list:
            for layer in layername:
                m.layers.append(ogr_layer(shape,layer))
        else:
            m.layers.append(ogr_layer(shape,layername))
        m.zoom_all()
        output = '%s_type-%s.png' % (shape.split('.')[0].replace('data','maps'),ds)
        render_to_file(m,output)
        print 'rendered... %s' % output
        m.remove_all()

m = Map(600,350)

#try:
#  os.system('rm maps/*.png')
#except: pass

render_ds('shp')
render_ds('geojson')
render_ds('db')
#try:
#  os.system('open maps/*.png')
#except: pass

#import pdb;pdb.set_trace()
render_ds('kml')
#render_ds('csv')
render_ds(gml)

# gpx data seems to crash mapnik...
#render_ds(gpx)
