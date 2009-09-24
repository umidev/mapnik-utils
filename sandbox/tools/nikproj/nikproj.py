#!/usr/bin/env python

from mapnik import Coord, Envelope, Projection, forward_, inverse_
import sys

if (len(sys.argv) < 2):
    print sys.argv[0] + " <epsg:code> <Coord or Envelope>"
    sys.exit(1)
else:
    epsg = sys.argv[1]
    p = Projection('+init=%s' % epsg)
    coord = map(float,sys.argv[2].split(','))
    if len(coord) == 2:
        long_lat = Coord(*coord)
        print 'Forwarded:',
        print p.forward(long_lat)
        print
        print 'Inversed:',
        print p.inverse(long_lat)      
    elif len(coord) == 4:
        extent = Envelope(*coord)
        print 'Forwarded:',
        print forward_(extent,p)
        print
        print 'Inversed:',
        print inverse_(extent,p)