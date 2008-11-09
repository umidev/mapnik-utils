#!/usr/bin/env python

from distutils.core import setup

# Dynamically fetch the version and licence
version = __import__('nik2img').__version__
license = __import__('nik2img').__license__

setup(name='nik2img',
        version = version,
        py_modules=['nik2img'],
        #py_modules = ['cascadenik.compile', 'cascadenik.style']
        description='A mapfile to image converter for Mapnik',
        long_description='Use nik2img to interact with the Mapnik C++/Python mapping toolkit. Mirrors the utility of the shp2img script provided with the MapServer project and complements the `generate_image.py` and `generate_tiles.py` scripts used by the OpenStreetMap project to render mapnik graphics.',
        author='Dane Springmeyer',
        author_email='dbsgeo@gmail.com',
        platforms='OS Independent',
        license=license,
        keywords='Mapnik,gis,geospatial',
        url='http://mapnik-utils.googlecode.com/',
        classifiers=['Development Status :: 4 - Beta',
                     'Environment :: Console',
                     'Environment :: Web Environment',
                     'Intended Audience :: End Users/Desktop',
                     'Intended Audience :: Developers',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Utilities'],
        scripts = ['nik2img.py'],
        )