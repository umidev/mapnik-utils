#!/usr/bin/env python

# forward.py
#
# Description: reproject a csv file from a given projection back to geographic coordinates
#
# Usage: ./inverse.py test_3395.csv 1 2 EPSG:3595
#
# A mapnik equivalent to:
# http://trac.osgeo.org/mapserver/browser/trunk/mapserver/mapscript/python/examples/project_csv.py

import sys
import csv
import mapnik

# check input parameters
if (len(sys.argv) != 5):
    print sys.argv[0] + \
        " <csvfile> <x_col> <y_col> <epsg_code_in>"
    sys.exit(1)
else:     
    # set x and y indices
    x = int(sys.argv[2])
    y = int(sys.argv[3])

    # set input and output projections
    epsg = sys.argv[4].lower()
    p = mapnik.Projection("+init=%s" % epsg)
    print '// -- Initialized projection: %s' % p.params()
    
    # open file
    csv_in = open(sys.argv[1], 'r')
    csv_out = open('%s_to_geographic.csv' % (sys.argv[1].split('.')[0]), 'w')

    # read csv 
    csvIn  = csv.reader(csv_in)
    # setup output 
    csvOut = csv.writer(csv_out)

    for aRow in csvIn: # each record
        # set point
        point = mapnik.Coord(float(aRow[x]), float(aRow[y]))
        # project
        projected_point = p.inverse(point)
        
        # update with reprojected coordinates
        aRow[x] = projected_point.x
        if aRow[x].__repr__() == 'inf':
          print 'Coordinate error: try switching your x/y index'
          sys.exit()
        aRow[y] = projected_point.y
        if aRow[y].__repr__() == 'inf':
          print 'Coordinate error: try switching your x/y index'
          sys.exit()        
        csvOut.writerow(aRow)
    csv_in.close()
    csv_out.close()
