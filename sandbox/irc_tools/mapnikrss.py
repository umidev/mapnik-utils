#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mapnikrss.py - Phenny #mapnik rss notification module
"""

import sys
import time
import socket
import feedparser

DEBUG = False
socket.setdefaulttimeout(10)
INTERVAL = 10

urls = (
   'http://trac.mapnik.org/timeline?ticket=on&ticket_details=on&changeset=on&milestone=on&wiki=on&max=1&daysback=1&format=rss',
    )

class Feed(object):
   url = ''
   modified = ''

first_run = True
restarted = False
feeds = []


def read_feeds(phenny):
    for feed in feeds:
        try:
            fp = feedparser.parse(feed.url)
        except IOError, E:
            pass
        try:
            entry = fp.entries[0]
            if not feed.modified == entry.updated:
                try:
                    phenny.say("Mapnik Trac: %s | %s" % (entry.title, fp.entries[0].links[0].href))
                except:
                    phenny.say("Mapnik Trac: %s" % entry.title)
                feed.modified = entry.updated
            else:
                if DEBUG:
                    phenny.say(u'Skipping previously read entry: %s' % entry.title)
        except Exception, E:
            if DEBUG:
                phenny.say(E)

def startrss(phenny, input):
    """Begin reading RSS feeds"""
    global first_run, restarted, DEBUG, INTERVAL
    
    query = input.group(2)
    if query == '-v':
        DEBUG=True
    if query == '-q':
        DEBUG=False
    if query == '-i':
        INVERVAL = input.group(3)
    
    if first_run:
      
        if DEBUG:
            phenny.say("Okay, I'll start rss fetching...")
        first_run = False
        
        for url in urls:
            entry = Feed()
            entry.url = url
            feeds.append(entry)
    else:
        restarted = True      
        if DEBUG:
            phenny.say("Okay, I'll re-start rss...")
            
    while True:
        if DEBUG:
            phenny.say("Rechecking feeds")
        read_feeds(phenny)
        time.sleep(INTERVAL)
        
    if DEBUG:
        phenny.say("Stopped checking")
startrss.commands = ['startrss']
startrss.priority = 'high'
