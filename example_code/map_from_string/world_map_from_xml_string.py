#!/usr/bin/env python

from mapnik import *
import xml.dom.minidom as m

mapfile_string = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE Map>
<Map bgcolor="steelblue" srs="+proj=latlong +datum=WGS84">

  <Style name="My Style">
    <Rule>
      <PolygonSymbolizer>
        <CssParameter name="fill">#f2eff9</CssParameter>
      </PolygonSymbolizer>
      <LineSymbolizer>
        <CssParameter name="stroke">rgb(50%,50%,50%)</CssParameter>
        <CssParameter name="stroke-width">0.1</CssParameter>
      </LineSymbolizer>
    </Rule>
  </Style>

  <Layer name="world">
    <StyleName>My Style</StyleName>
    <Datasource>
      <Parameter name="type">shape</Parameter>
      <Parameter name="file">../../data/world_borders</Parameter>
    </Datasource>
  </Layer>

</Map>
'''

# manipulate the xml in-place by switching the style name and the reference in the layer
xml_doc = m.parseString(mapfile_string)
styles = xml_doc.getElementsByTagName("Style")
styles[0].setAttribute('name','New Style Name')
layers = xml_doc.getElementsByTagName("Layer")
layer1_style = layers[0].getElementsByTagName('StyleName')
layer1_style[0].childNodes[0].nodeValue = 'New Style Name'
    
m = Map(600, 300)
# note: the xml is unicode, so we must first coerce to a proper string
# see: http://trac.mapnik.org/ticket/163
load_map_from_string(m, str(xml_doc.toxml()))
m.zoom_to_box(m.layers[0].envelope()) 
render_to_file(m, 'map_from_string.png') 
