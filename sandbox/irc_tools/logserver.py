#!/usr/bin/env python
# -*- coding: utf-8 -*-


import glob
from os import path
from mimetypes import guess_type
from pygments import highlight
from pygments.lexers import IrcLogsLexer
from pygments.formatters import HtmlFormatter
from werkzeug import Response, Request, DebuggedApplication,  run_simple

ROOT_PATH = path.abspath(path.dirname(__file__))

def not_found(req):
    return Response(u'<h1>Page Not Found</h1>', status=404, mimetype='text/html')

def about(req):
    return Response(u'''<h1>#mapnik logs</h1>
        <p>Docs will go here.</p>
    ''', mimetype='text/html')

def home(req):
    log_days = glob.glob('*.txt')
    log_html = '<ul>'
    for log in log_days:
      name = log.strip('.txt')
      log_html += '<li><a href="/days/%s">%s</a></li>' % (name,name)
    log_html += '</ul>'
    return Response(log_html, mimetype='text/html')

def static_serve(request, file):
    """Return a static file"""
    if not file:
      return Response('Not Found no filename', status=404)
    else:
      filename = path.join(ROOT_PATH,file)

    if path.isfile(filename):
        mimetype = guess_type(filename)[0] or 'application/octet-stream'
        f = open(filename, 'r')
        try:
            return Response(f.read(), mimetype=mimetype)
        finally:
            f.close()
    return Response('Not Found: %s' % filename, status=404)

def get_day(request, filename):
    """Return an html formatter day long irc log."""
    if not filename:
      return Response('Not Found no filename', status=404)
    else:
      filename = path.join(ROOT_PATH,filename + '.txt')

    if path.isfile(filename):
        mimetype = 'text/html'
        f = file(filename, 'r')
        header = '''<html><head>
            <link rel="stylesheet" href="/static/style.css" type="text/css">
            <title>Mapnik Logs</title>
            </head>'''
        content = highlight(f.read(), IrcLogsLexer(), HtmlFormatter(cssclass='syntax'))
        footer = '</html>'
        resp_text = header + content + footer
        try:
            return Response(resp_text, mimetype=mimetype)
        finally:
            f.close()
    return Response('Not Found: %s' % filename, status=404)
        
views = {
    '/':        home,
    '/about':   about,
     }

def application(environ, start_response):
    """
    """
    req = Request(environ)
    if req.path in views:
        resp = views[req.path](req)
    elif req.path.startswith('/days'):
            resp = get_day(req, req.path.replace('/days/',''))
    elif req.path.startswith('/static'):
            resp = static_serve(req, req.path.replace('/static/',''))
    else:
        resp = not_found(req)
    return resp(environ, start_response)

if __name__ == '__main__':
      
    application = DebuggedApplication(application, evalex=True)
    run_simple('localhost', 8000, application)
