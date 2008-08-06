#!/usr/bin/env python

import sys
sys.path.append('/Library/WebServer/CGI-Executables/')

from mapnik.ogcserver.cgiserver import Handler
from jon import fcgi

class OGCServerHandler(Handler):
    configpath = '/Library/WebServer/CGI-Executables/ogcserver.conf'

fcgi.Server({fcgi.FCGI_RESPONDER: OGCServerHandler}).run()