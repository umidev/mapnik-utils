#!/usr/bin/env python

"""
Release Steps
-------------
 * create ~./pypirc file with pypi user:pass
 * Edit CHANGELOG.txt
 * rebuild MANIFEST 'python setup.py sdist --manifest-only'
 * Increment '__version__' in main script and 'version' in setup.py
 * Run `deploy.py` to create sdist, upload, and create tag
 * Commit tag
 * Update Google Code wiki
"""

import sys
import time
from subprocess import call as subcall

DEBUG = False

app = 'nik2img'
version = __import__(app).__version__
tag_dir= '../../tags/%s' % app

def call(cmd):
  if DEBUG:
      print 'DEBUG: will execute -> %s' % cmd  
  else:
      try:
        response = subcall(cmd,shell=True)
        print
        time.sleep(1)
        if response < 0:
          sys.exit(response)
      except OSError, E:
        sys.exit(E)

def cleanup():
    call('sudo -rf rm *.egg* *.pyc dist/ build/')

def tag():
    call('svn cp ../%s %s/%s/' % (app,tag_dir,version))

def package():
    call('python setup.py sdist upload')
    call('cp dist/%s-%s.tar.gz %s' % (app,version,tag_dir))
    call('svn add %s/%s-%s.tar.gz' % (tag_dir,app,version))

def commit():
    call('svn ci %s -m "tagging %s %s release"' % (tag_dir,app,version))
    
def main():
    cleanup()
    tag()
    package()
    cleanup()
    commit()
    
if __name__ == '__main__':
    main()