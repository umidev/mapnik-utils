#!/usr/bin/env python

import sys
sys.path.append('/Users/spring/projects/mapnik-utils/trunk/tutorials/wms/')

from mapnik.ogcserver.cgiserver import Handler
from jon import fcgi

class OGCServerHandler(Handler):
    configpath = '/Users/spring/projects/mapnik-utils/trunk/tutorials/wms/ogcserver.conf'

fcgi.Server({fcgi.FCGI_RESPONDER: OGCServerHandler}).run()