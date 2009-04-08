#!/usr/bin/env python

"""
Release Steps
-------------
 * create ~./pypirc file with pypi user:pass
 * Edit CHANGELOG.txt
 * Temporarily remove SVN tag from __version__ and in setup.py
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
    time.sleep(1)
    if response < 0:
      sys.exit(response)
  except OSError, E:
    sys.exit(E)

version = __import__(app).__version__

tag_dir= '../../tags/%s/' % app

call('sudo rm *.egg* *.pyc tests_output dist/ build/ -r -f')
call('svn cp ../%s/ %s/%s' % (app,tag_dir,version))
call('svn rm %s/%s/deploy.py' % (tag_dir,version))
call('python setup.py sdist upload')
call('cp dist/%s-%s.tar.gz %s' % (app,version,tag_dir))
call('svn add %s/%s-%s.tar.gz' % (tag_dir,app,version))
call('sudo rm *.egg* tests_output dist/ build/ -r -f')

