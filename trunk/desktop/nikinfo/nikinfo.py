#!/usr/bin/env python

import sys
import os
import re

def get_attr_dict(l):
  pattern = r'(\w+)=(.*)'
  match = re.findall(pattern, l.describe())
  attr, encoding, idx = {},'',0
  for x in match:
    if x[1] == 'shape':
     encoding = match[idx+1][1]
    elif x[0] == 'name':
     attr[x[1]] = {}
     attr[x[1]]['type'] = match[idx+1][1]
     attr[x[1]]['size'] = match[idx+2][1]
    idx += 1
  return attr

def get_attr_list(l):
    pattern = r'(\w+)=(.*)'
    match = re.findall(pattern, l.describe())
    item, idx = [],0
    for x in match:
        if x[0] == 'name' and not x[0] == 'shape':
            attr = {}
            attr['name'] = x[1]
            attr['type'] = match[idx+1][1]
            attr['size'] = match[idx+2][1]
            item.append(attr)
        idx += 1
    return item

layer_xml = '''
  <Layer name="%s" status="on">
    <StyleName>%s_style</StyleName>
    <Datasource>
      <Parameter name="type">shape</Parameter>
      <Parameter name="file">%s</Parameter>
    </Datasource>
  </Layer>
'''
def main():
    if (len(sys.argv) < 2):
        print sys.argv[0] + " <shapefile>"
        sys.exit(1)
    else:
        import mapnik
        shp = sys.argv[1]
        shp_dir = os.path.abspath(sys.argv[1]).split('.shp')[0]
        shp_ptr = shp.split('.shp')[0]
        lyr = mapnik.Shapefile(file=shp_ptr)
        e = lyr.envelope()
        attributes = get_attr_list(lyr)
        print '-'*70
        print 'Info for %s shapefile:' % shp_ptr
        print 'Envelope:',
        print e
        print 'MaxX, MaxY, MinX, MinY:',
        print e.minx, e.miny, e.maxx, e.maxy
        print 'Center:',
        print e.center()
        print 'Height:',
        print e.height()
        print 'Width:',
        print e.width()
        print 'Attributes:'
        for attr in attributes:
          for k,v in attr.items():
            print '\t',k,'\t',v,
          print '\n',
        print 
        print 'Sample XML layer:'
        print layer_xml % (shp_ptr,shp_ptr,shp_dir)
        
        print '-'*70

if __name__ == "__main__":
  main()
