#!/usr/bin/env python

"""
Release Steps
-------------
 * create ~./pypirc file with pypi user:pass
 * Edit CHANGELOG.txt
 * Temporarily remove SVN tag from __version__
 * Run `deploy.py` to create sdist, upload, and create tag
 * commit tag
 * Update Google Code wiki
"""

app = 'nik2img'

import sys
import time
from subprocess import call as subcall

def call(cmd):
  try:
    response = subcall(cmd,shell=True)
    print
    time.sleep(.5)
    if response < 0:
      sys.exit(response)
  except OSError, E:
    sys.exit(E)

version = __import__(app).__version__

tag_dir= '../../../tags/%s/' % app

call('sudo rm *.egg* dist/ build/ -r -f')
call('rm *.pyc')
call('svn cp ../%s/ %s/%s' % (tag_dir,version,app))
call('rm %s/%s/deploy.py' % (tag_dir,version))
call('python setup.py sdist upload')
call('cp dist/%s-%s.tar.gz %s' % (app,version,tag_dir))
call('svn add %s/%s-%s.tar.gz' % (app,tag_dir,version))
call('sudo rm *.egg* dist/ build/ -r -f')

