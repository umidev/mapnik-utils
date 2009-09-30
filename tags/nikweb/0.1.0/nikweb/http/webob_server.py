#!/bin/env python

__all__ = ("Nikweb",)

import re

from webob import Request, Response, exc
try:
    import json
except ImportError:
    # Python <2.6 doesn't have a JSON module
    import simplejson as json

import nikweb.http

class Nikweb(object):
    URL_PATTERNS = (
        (r'/$', 'index'),
        (r'/(?P<map>[\w\.-]+)/$', 'render'),
    )
    
    def __init__(self, map_definitions, **kwargs):
        self.nikweb_http = nikweb.http.NikwebHttp(map_definitions, **kwargs)
        
        # compile the urls
        urls = []
        for u_re, u_func in self.URL_PATTERNS:
            urls.append((re.compile(u_re), getattr(self, u_func)))
        self.urls = tuple(urls)
    
    def __call__(self, environ, start_response):
        """ WSGI request handler """
        request = Request(environ)
        
        for url_re, view_func in self.urls:
            m = url_re.match(request.path_info)
            if m:
                kwargs = m.groupdict()
                if kwargs:
                    args = ()
                else:
                    args = m.groups()
                break
        else:
            return exc.HTTPNotFound("Not found")(environ, start_response)
        
        try:
            resp = view_func(request, *args, **kwargs)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)
    
    def index(self, request):
        map_defs = self.nikweb_http.index()
        
        resp = Response(content_type='text/plain', charset="utf8")
        resp.unicode_body = u"\n".join(map_defs) + u"\n"
        return resp

    def render(self, request, map):
        if request.method == 'POST':
            raw_data = request.body
        elif 'q' in request.GET:
            raw_data = request.GET['q']
        else:
            raise exc.HTTPBadRequest("No 'q' parameter specified").exception 
        
        #try:
        d = json.loads(raw_data.decode('utf-8'))
        #except:
        #    raise exc.HTTPBadRequest('Error parsing JSON').exception
        
        #try:
        image, content_type, elapsed = self.nikweb_http.render(map, d)
        #except:
        #    raise exc.HTTPServerError('Error rendering').exception
        
        resp = Response(body=image, content_type=content_type)
        resp.headers['X-nikweb-rendertime'] = "%0.3f" % elapsed
        return resp

if __name__ == "__main__":
    import os
    import sys
    import optparse
    import wsgiref.simple_server
    import logging
    
    USAGE = ("%prog [OPTIONS...]\n\n"
             "Runs a simple debugging web server for the mapnik renderer.\n"
             "Listens on 127.0.0.1:8080 by default.\n\n"
             "The following environment variables do useful things too:\n"
             "  NIKWEB_MAP_LAYER_PREFIX is the search prefix for data layer names\n"
             "  NIKWEB_DEBUG (0/1) turns on debugging output for error requests\n")
    
    parser = optparse.OptionParser(usage=USAGE)
    parser.add_option('--ip', dest='ip', default='127.0.0.1', help='listen on interface IP (0.0.0.0 for all)', metavar='IP')
    parser.add_option('--port', dest='port', type='int', default=8080, help='listen on TCP port PORT', metavar='PORT')
    parser.add_option('--maps', dest='maps_dir', help='load map definitions from PATH', metavar='PATH', default=os.path.join(os.path.split(__file__)[0], '../../examples/'))
    (options, args) = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG)
    
    print >>sys.stderr, "Starting server at %s:%d ..." % (options.ip, options.port)

    # WSGI application
    application = Nikweb(options.maps_dir, 
                         debug=int(os.environ.get('NIKWEB_DEBUG','0')), 
                         map_layer_prefix=os.environ.get('NIKWEB_MAP_LAYER_PREFIX'),
                         default_size=os.environ.get('NIKWEB_DEFAULT_SIZE'))

    server = wsgiref.simple_server.make_server(options.ip, options.port, application)
    server.serve_forever()

