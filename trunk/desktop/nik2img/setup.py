#!/usr/bin/env python

from distutils.core import setup

# Dynamically fetch the version, licence, and readme
version = __import__('nik2img').__version__
license = __import__('nik2img').__license__
readme = file('README.txt','rb').read()

setup(name='nik2img',
        version = version,
        py_modules=['nik2img'],
        #py_modules = ['cascadenik.compile', 'cascadenik.style']
        description='A mapfile to image converter for the Mapnik C++/Python mapping toolkit',
        long_description=readme,
        author='Dane Springmeyer',
        author_email='dbsgeo@gmail.com',
        platforms='OS Independent',
        license=license,
        requires=['Mapnik'],
        #test_suite = 'tests.run_doc_tests',
        keywords='Mapnik,gis,geospatial',
        url='http://mapnik-utils.googlecode.com/',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'Environment :: Console',
                     'Environment :: Web Environment',
                     'Intended Audience :: End Users/Desktop',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Science/Research',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Utilities'],
        scripts = ['nik2img.py'],
        )