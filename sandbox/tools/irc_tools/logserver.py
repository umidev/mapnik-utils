#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import datetime
from mimetypes import guess_type
from pygments import highlight
from pygments.lexers import IrcLogsLexer
from pygments.formatters import HtmlFormatter
from werkzeug import Response, Request

import sys
sys.stdout = sys.stderr
# requires text files output by loggy placed beside this running app
#ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

ROOT_PATH = '/home/mapniklog/logs/mapnik'

ROOT_URL = '/mapnik_logs'

BASE = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
        "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>%(title)s</title>
<link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
%(body)s
"""

FOOTER = """
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-408098-23");
pageTracker._trackPageview();
} catch(err) {}</script>
</body>
</html>
"""

WELCOME = """
<h1>Mapnik IRC Logs</h1>
<a href="%(root)s/about/">About</a> | <a href="%(root)s/%(year)s/%(month)s/">This Month</a> | <a href="%(root)s/%(year)s/">This Year</a> | <a href="%(root)s/">All logs</a>
"""

ABOUT = """
<h1><a href="irc://irc.freenode.net/mapnik">#mapnik</a> <a href="/">logs</a></h1>
<p>Logging done by <a href="http://inamidst.com/code/loggy.py">Loggy</a> for the <a href="http://mapnik.org">Mapnik project</a></p>
<p><a href="http://mapnik-utils.googlecode.com/svn/sandbox/tools/irc_tools/">Set up</a> in an afternoon by <a href="http://dbsgeo.com">Dane Springmeyer</a></p>
"""

def about(req):
    vars = {'body':ABOUT,'title':"Mapnik IRC Logs - About"}
    return Response(BASE % vars + FOOTER, mimetype='text/html')

def not_found():
    vars = {'body':'<h2>Page Not Found (404)</h2>','title':"Mapnik IRC Logs - Not Found"}
    return Response(BASE % vars + FOOTER, status=404, mimetype='text/html')

def list_days(pattern):
    log_days = glob.glob(ROOT_PATH + pattern)
    top = '<h2><a href="irc://irc.freenode.net/mapnik">#mapnik</a> <a href="/">logs</a>:</h2>'
    log_html = '<ul>'
    for log in log_days:
      logfile = os.path.basename(log)
      name = logfile.strip('.txt')
      date = datetime.date(*map(int,name.split('-')))
      log_html += '<li><a href="%s/%s/">%s</a></li>\n' % (ROOT_URL,name.replace('-','/'),date.strftime("%d %B %Y (%A)"))
    log_html += '</ul>\n'
    vars = {'body':top + log_html,'title':"Mapnik IRC Logs - %s Records" % len(log_days)}
    return Response(BASE % vars + FOOTER, mimetype='text/html')
    
def get_day(filename,path=None):
    """Return an html formatter day long irc log."""
    vars = {}
    if not path:
        f = os.path.join(filename + '.txt')
        if '/' in filename:
            filename = os.path.basename(filename)
    else:
        f = os.path.join(path,filename + '.txt')
        if '/' in filename:
            filename = os.path.basename(filename)
    date = datetime.date(*map(int,filename.split('-')))
    previous = date - datetime.timedelta(1)
    next = date + datetime.timedelta(1)
    datename = date.strftime("%A %d, %B %Y")
    if os.path.isfile(f):
        f_ = file(f, 'r')
        top = '<h2><a href="irc://irc.freenode.net/mapnik">#mapnik</a> <a href="/">log</a>: ' + datename + '</h2>'
        parts = filename.split('-')
        top += '<h4><a href="%s/%s/">%s</a>' % (ROOT_URL,parts[0],parts[0])
        top += ' | <a href="%s/%s/%s/">%s</a>' % (ROOT_URL,parts[0],parts[1],parts[1])
        top += '</h4>'
        links = ''
        pre_file = '%s/%s-%s-%s.txt' % (ROOT_PATH, previous.year,pad(previous.month),pad(previous.day))
        next_file = '%s/%s-%s-%s.txt' % (ROOT_PATH, next.year,pad(next.month),pad(next.day))
        pre_text = '<a href="%s/%s/%s/%s/">previous</a>' % (ROOT_URL,previous.year,pad(previous.month),pad(previous.day))
        next_text = '<a href="%s/%s/%s/%s/">next</a>' % (ROOT_URL,next.year,pad(next.month),pad(next.day))
        if os.path.isfile(pre_file) & os.path.isfile(next_file):
            links += '%s | %s' % (pre_text,next_text)
        elif os.path.isfile(pre_file):
            links += pre_text
        elif os.path.isfile(next_file):
            links += next_text     
        content = links + highlight(f_.read(), IrcLogsLexer(), HtmlFormatter(cssclass='syntax'))
        try:
            title = "Mapnik IRC Log -  %s" % datename
            return (title,top,content)
        finally:
            f_.close()

def pad(num):
    if len(str(num)) < 2:
        return '0%s' % num
    return num

def home(req):
    today = datetime.datetime.today()
    dates = {}
    dates['year'] = today.year
    dates['month'] = today.month
    dates['day'] = today.day
    dates['root'] = ROOT_URL
    items = WELCOME % dates
    log_days = glob.glob(ROOT_PATH + '/%s-%s*.txt' % (today.year,pad(today.month)))
    #import pdb;pdb.set_trace()
    if log_days:
        todays_log = log_days[-1].replace('.txt','')
        if todays_log:
            items += '<h4> Today: </h4>'
            items += get_day(todays_log,ROOT_PATH)[2]
        #last_day = log_days[-2].replace('.txt','')
        #if last_day:
        #    items += '<h4> Yesterday: </h4>'
        #    items += get_day(last_day,ROOT_PATH)[2]

    vars = {'body':items,'title':"Mapnik IRC Logs"}
    return Response(BASE % vars + FOOTER, mimetype='text/html')

def static_serve(request, file):
    """Return a static file"""
    vars = {}
    if file:
        filename = os.path.join(ROOT_PATH,file)
    if os.path.isfile(filename):
        mimetype = guess_type(filename)[0] or 'application/octet-stream'
        f = open(filename, 'r')
        try:
            vars['body'] = f.read()
            vars['title'] = "Mapnik IRC Logs - CSS"
            return Response(BASE % vars + FOOTER, mimetype=mimetype)
        finally:
            f.close()
    return not_found()
    
def query(req, path):
    if path == '':
        return list_days('/*.txt')
    parts = path.strip('/').split('/')
    #try:
    if not len(parts):
        return list_days('/*.txt')
    if len(parts) == 1:
        year = parts[0]
        return list_days('/%s-*.txt' % year)
    elif len(parts) == 2:
        year = parts[0]
        month = parts[1]
        return list_days('/%s-%s-*.txt' % (year,pad(month)))
    elif len(parts) == 3:
        year = parts[0]
        month = parts[1]
        day = parts[2]
        day = get_day('%s-%s-%s' % (year,pad(month),pad(day)),ROOT_PATH)
        if day:
            vars = {'title':day[0],'body':day[1] + day[2]}
            return Response(BASE % vars + FOOTER, mimetype='text/html')
    #except Exception, e:
    #    print e,path
    #    return not_found()
    #print path
    return not_found()

views = {
    '/':        home,
    '%s/about/' % ROOT_URL:   about,
     }

def application(environ, start_response):
    """
    """
    req = Request(environ)
    if req.path in views:
        resp = views[req.path](req)
    elif req.path.startswith(ROOT_URL):
        resp = query(req, req.path.replace(ROOT_URL +'/','').replace(ROOT_URL,'') )
    elif req.path.startswith('/static'):
        resp = static_serve(req, req.path.replace('/static/','') )
    else:
        resp = not_found()
    return resp(environ, start_response)

if __name__ == '__main__':
    print ROOT_PATH
    from werkzeug import DebuggedApplication, run_simple
    application = DebuggedApplication(application, evalex=True)
    run_simple('0.0.0.0', 8000, application)
