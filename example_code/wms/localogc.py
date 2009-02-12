#!/usr/bin/env python

import sys
from mapnik.ogcserver.wsgi import WSGIApp
from wsgiref.simple_server import make_server

# add to the PYTHONPATH the folder that contains map_factory.py (an ogcserver.conf)
sys.path.append('/Users/spring/projects/utils/example_code/wms/')
application = WSGIApp('/Users/spring/projects/utils/example_code/wms/ogcserver.conf')

if __name__ == '__main__':
    httpd = make_server('localhost', 8000, application)
    print "Listening on port 8080...."
    httpd.serve_forever()