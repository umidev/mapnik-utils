#!/usr/bin/env python

import os
version = __import__('nik2img').__version__

tag_dir= '../../../tags/nik2img/'

os.system('sudo rm dist/ build/ -r -f')
print
os.system('rm *.pyc')
print
os.system('svn cp ../nik2img/ %s/%s' % (tag_dir,version))
print
os.system('rm %s/%s/deploy.py' % (tag_dir,version))
print
os.system('python setup.py sdist upload')
print
os.system('cp dist/nik2img-%s.tar.gz %s' % (version,tag_dir))
print
os.system('svn add %s/nik2img-%s.tar.gz' % (tag_dir,version))
print
os.system('sudo rm dist/ build/ -r -f')

