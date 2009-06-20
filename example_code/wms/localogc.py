#!/usr/bin/env python

import os
import sys
from mapnik.ogcserver.wsgi import WSGIApp

import os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
# add to the PYTHONPATH the folder that contains map_factory.py (and ogcserver.conf)
sys.path.append(WORKING_DIR)
#sys.path.append('/Users/spring/projects/mapnik-dev/trunk/bindings/python/')
configpath = os.path.join(WORKING_DIR,'ogcserver.conf')

application = WSGIApp(configpath)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8000, application)
    print "Listening on port 8000...."
    httpd.serve_forever()
