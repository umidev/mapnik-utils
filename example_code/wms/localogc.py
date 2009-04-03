#!/usr/bin/env python

import sys
from mapnik.ogcserver.wsgi import WSGIApp

# add to the PYTHONPATH the folder that contains map_factory.py (and ogcserver.conf)
sys.path.append('/Users/spring/projects/utils/example_code/wms/')
#sys.path.append('/Users/spring/projects/mapnik-dev/trunk/bindings/python/')
application = WSGIApp('/Users/spring/projects/utils/example_code/wms/ogcserver.conf')

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8000, application)
    print "Listening on port 8000...."
    httpd.serve_forever()
