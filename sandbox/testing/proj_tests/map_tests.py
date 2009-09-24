#!/usr/bin/env python
from mapnik import *

def py_layer(m):
  s,r = Style(),Rule()
  r.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
  r.symbols.append(LineSymbolizer(Color('rgb(50%,50%,50%)'),0.1))
  s.rules.append(r)
  m.append_style('My Style',s)
  lyr = Layer('world')
  lyr.datasource = Shapefile(file='data/processed_p')
  lyr.styles.append('My Style')
  return lyr

def from_xml_no_srs(bbox):
  m = Map(600, 600)
  load_map(m, 'mapfiles/mapfile_no_srs.xml')
  envelope = Envelope(*bbox)
  m.zoom_to_box(envelope) 
  render_to_file(m, 'outputs/from_xml_no_srs.png', 'png')

def with_python_no_srs(bbox):
  m = Map(600, 600)
  m.background = Color('steelblue')
  lyr = py_layer(m)
  m.layers.append(lyr)
  envelope = Envelope(*bbox)
  m.zoom_to_box(envelope) 
  render_to_file(m, 'outputs/with_python_no_srs.png', 'png')

def from_xml_gmerc_srs(bbox, srs):
  m = Map(600, 600)
  load_map(m, 'mapfiles/mapfile_gmerc_srs.xml')
  envelope = Envelope(*bbox)
  m.zoom_to_box(envelope) 
  render_to_file(m, 'outputs/from_xml_gmerc_srs.png', 'png')

def with_python_gmerc_srs(bbox, srs):
  m = Map(600, 600, srs)
  m.background = Color('steelblue')
  lyr = py_layer(m)
  lyr.srs = srs
  m.layers.append(lyr)
  envelope = Envelope(*bbox)
  m.zoom_to_box(envelope) 
  render_to_file(m, 'outputs/with_python_gmerc_srs.png', 'png')


# These require the gmerc proj literal in your /usr/local/share/proj/epsg file

def from_xml_gmerc_epsg_init(bbox, epsg):
  m = Map(600, 600)
  load_map(m, 'mapfiles/mapfile_gmerc_epsg_init.xml')
  envelope = Envelope(*bbox)
  m.zoom_to_box(envelope) 
  render_to_file(m, 'outputs/from_xml_epsg_%s.png' % epsg.split(':')[1], 'png')

def from_xml_32766_epsg_init(bbox, epsg):
  m = Map(600, 600)
  load_map(m, 'mapfiles/mapfile_32766_epsg_init.xml')
  envelope = Envelope(*bbox)
  m.zoom_to_box(envelope) 
  render_to_file(m, 'outputs/from_xml_epsg_%s.png' % epsg.split(':')[1], 'png')

def with_python_epsg_init(bbox, epsg):
  m = Map(600, 600, epsg)
  m.background = Color('steelblue')
  lyr = py_layer(m)
  lyr.srs = epsg
  m.layers.append(lyr)
  envelope = Envelope(*bbox)
  m.zoom_to_box(envelope) 
  render_to_file(m, 'outputs/with_python_epsg_%s.png' % epsg.split(':')[1], 'png')

if __name__ == '__main__':
  #from_xml_no_srs()
  #with_python_no_srs()
  pass