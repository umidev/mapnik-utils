#!/usr/bin/env python

import sys
sys.path.append('/Users/spring/projects/mapnik-utils/example_code/wms/')

from mapnik.ogcserver.cgiserver import Handler
from jon import fcgi

class OGCServerHandler(Handler):
    configpath = '/Users/spring/projects/mapnik-utils/example_code/wms/ogcserver.conf'

fcgi.Server({fcgi.FCGI_RESPONDER: OGCServerHandler}).run()