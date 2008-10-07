#!/usr/bin/env python

# http://blog.brandonking.net//2008/01/django-app-modfcgid-apache-2-setup-on.html/
# http://blog.cleverelephant.ca/2008/05/fastcgi-on-osx-leopard.html

import sys
sys.path.append('/Users/spring/projects/mapnik-utils/trunk/tutorials/wms/')

from mapnik.ogcserver.cgiserver import Handler
from jon import fcgi

class OGCServerHandler(Handler):
    configpath = '/Users/spring/projects/mapnik-utils/trunk/tutorials/wms/ogcserver.conf'

fcgi.Server({fcgi.FCGI_RESPONDER: OGCServerHandler}).run()