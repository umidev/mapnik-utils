#!/usr/bin/env python

from mapnik import *
import os

data = '../data'
mapfiles = '../mapfiles'
PROJ_LITERALS =True

projs = {
    4326: ('+init=epsg:4326','+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'),
    32632: ('+init=epsg:32632','+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'),
    32634: ('+init=epsg:32634','+proj=utm +zone=34 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'),
    }

proj = {}
if PROJ_LITERALS:
 for k,v in projs.items():
   proj[k] = v[1]
else:
 for k,v in projs.items():
   proj[k] = v[0]   
   

postgis = {
    'host':'localhost',
    'port': 5432,
    'user': 'postgres',
    'password':'',
    'dbname':'foss4g2008'
    }

datasources = {
    'states':'%s/states' % data, 
    'states_pg':'states_pg',
    'tiger_shp':'%s/tiger_shp' % data,
    'tiger_pg':'tiger_pg',
    'merano':'%s/merano.tiff' % data,
    'merano2':'%s/merano_jptov.tiff' % data,
    'n_sid':'%s/S-34-30_2000.sid' % data,
    's_sid':'%s/S-34-30_2000.sid' % data,
    }

shp_mapping = {
    '[PERSONS] < 2000000':'77,255,77',
    '[PERSONS] > 2000000 and [PERSONS] < 4000000':'255,77,77',
    '[PERSONS] > 4000000' :'77,77,255',
    }

pg_mapping = {
    '[persons] < 2000000':'77,255,77',
    '[persons] > 2000000 and [persons] < 4000000':'255,77,77',
    '[persons] > 4000000' :'77,77,255',
    }

def poly_filter(name, style_filter):
    s = Style()
    for k,v in style_filter.items():
        r=Rule()
        r.filter = Filter(k)
        color = Color('rgb(%s)' % v)
        r.symbols.append(PolygonSymbolizer(color))
        s.rules.append(r)
    return name, s

def line_style(name,color,width):
    s, r = Style(), Rule()
    line = LineSymbolizer(Color(color),width)
    r.symbols.append(line)
    s.rules.append(r)
    return name, s

def text_style(name,field,font='DejavVu Sans Book',size=11,color='black'):
    s, r, color_obj = Style(), Rule(), Color(color)
    text = TextSymbolizer(field,font,size,color_obj)
    r.symbols.append(text)
    s.rules.append(r)
    return name, s

def raster_style(name):
    s, r = Style(), Rule()
    r.symbols.append(RasterSymbolizer())
    s.rules.append(r)
    return name, s

def generate_layer(name,type,srs,styles=[]):
    lyr = Layer(name,srs)
    if type == 'shapefile':
      lyr.datasource = Shapefile(file=datasources[name])
      lyr.abstract = datasources[name]
      lyr.title = datasources[name]
    elif type == 'postgis':
      params = postgis.copy()
      params['table'] = name
      lyr.datasource = PostGIS(**params)    
    elif type == 'gdal':
      lyr.datasource = Gdal(file=datasources[name])
    lyr.active = False
    for sty in styles:
      lyr.styles.append(sty)
    return lyr

def pg_layer(name,srs,styles=[]):
    lyr = Layer(name,srs)
    lyr.datasource = Shapefile(file=datasources[name])
    for sty in styles:
      lyr.styles.append(sty)
    return lyr

def main():
    m = Map(600,350,proj[4326])
    m.background = Color("white")
    
    # Styles
    m.append_style(*poly_filter('states_shp_styles',shp_mapping) )
    m.append_style(*poly_filter('states_pg_styles',pg_mapping) )
    m.append_style(*line_style('states_outlines','black',.3))
    m.append_style(*text_style('states_shp_labels','STATE_ABBR',font='Times New Roman Regular'))
    m.append_style(*text_style('states_pg_labels','state_abbr',font='Times New Roman Regular'))
    m.append_style(*line_style('tiger_styles','black',1))
    m.append_style(*raster_style('raster_style'))
    
    # Layers
    m.layers.append(generate_layer('states','shapefile',
        srs=proj[4326],
        styles=['states_shp_styles','states_outlines','states_shp_labels']))
    m.layers.append(generate_layer('states_pg','postgis',
        srs=proj[4326],
        styles=['states_pg_styles','states_outlines','states_pg_labels']))
    m.layers.append(generate_layer('tiger_shp','shapefile',
        srs=proj[4326],
        styles=['tiger_styles']))
    m.layers.append(generate_layer('tiger_pg','postgis',
        srs=proj[4326],
        styles=['tiger_styles']))
    m.layers.append(generate_layer('merano','gdal',
        srs=proj[32632],
        styles=['raster_style']))
    m.layers.append(generate_layer('merano2','gdal',
        srs=proj[32632],
        styles=['raster_style']))
    m.layers.append(generate_layer('n_sid','gdal',
        srs =proj[32632],
        styles=['raster_style']))
    m.layers.append(generate_layer('s_sid','gdal',
        srs = proj[32634],
        styles=['raster_style']))
    return m

if __name__ == "__main__":
  m = main()
  mapfile = mapfiles + '/pygen_bench.xml'
  if os.path.exists(mapfile):
    print '-'*75
    print 'ERROR:'
    print "Mapnik's save_map() function cannot overwrite existing files, please delete %s to regenerate" % mapfile
    print '-'*75
  else:
    save_map(m,mapfile)
    print '-'*75
    print 'Mapfile (with all layers INACTIVE by default) output to: %s' % mapfile 
    print '-'*75