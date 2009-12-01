#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import socket
import mapnik
import urllib
import tempfile
#from werkzeug import Response, Request

PORT = 8080

pattern = r'''/(?P<url1>.*)\+(?P<url2>.*)/(?P<z>\d{1,10})/(?P<x>\d{1,10})/(?P<y>\d{1,10})\.(?P<extension>(?:png|jpg))'''
request_re = re.compile(pattern)

server = "http://%s:%s" % (socket.gethostname(),PORT)

url = '%s/http://tile.openstreetmap.org/+http://toolserver.org/~cmarqu/hill/12/2270/1395.png' % server
example = '<a href="%s">%s</a>' % (url,url)

class Response:
    def __init__(self,data,status=None,mimetype=None):
        self.data = data
        self.status = status or '200 OK'
        self.mimetype = mimetype or 'text/plain'
    def __call__(self, environ, start_response):
        start_response(str(self.status),[('Content-Type', self.mimetype)])
        yield self.data
        
class Request:
    def __init__(self,environ):
        self.environ = environ
    
    @property
    def path(self):
        return '/' + (self.environ.get('PATH_INFO') or '').lstrip('/')

def fetch_image(tile):
    temp = tempfile.NamedTemporaryFile(suffix='.png', mode = 'w+b')
    f = urllib.urlopen(tile)
    data = f.read()
    temp.write(data)
    f.close()
    temp.seek(0)
    im = mapnik.Image.open(temp.name)
    temp.close()
    return im
    
def not_found():
    return Response('<h2>Page Not Found (404)</h2><p> try something like:<br>%s' % example, status='404 Not Found', mimetype='text/html')

def tiles(url_a,url_b,z,x,y,format):
    
    tile_uri = '/%s/%s/%s.%s' % (z,x,y,format)
    im_a = fetch_image(url_a.strip('/') + tile_uri)
    im_b = fetch_image(url_b.strip('/') + tile_uri)
    
    opacity = 1.0
    im_a.blend(0,0,im_b,opacity)
    return Response(im_a.tostring(str(format)),mimetype='image/%s' % format)

def application(environ, start_response):
    req = Request(environ)
    if request_re.match(req.path):
        url_a,urlb,z,x,y,format = request_re.match(req.path).groups()
        resp = tiles(url_a,urlb,z,x,y,format)
    else:
        resp = not_found()
    return resp(environ, start_response)

def run(process):
    try:
        process.serve_forever()
    except KeyboardInterrupt:
        process.server_close()
        sys.exit(0)

if __name__ == '__main__':
    #from werkzeug import DebuggedApplication, run_simple
    #application = DebuggedApplication(application, evalex=True)
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', PORT, application)
    run(httpd)
