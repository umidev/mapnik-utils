#!/usr/bin/env python

from distutils.core import setup

setup(name='nikinfo',
        version = '0.1.0',
        scripts = ['nikinfo.py'],
        py_modules=['nikinfo'],
        description='Tool for getting details about a shapefile for use with Mapnik',
        #long_description='',
        author='Dane Springmeyer',
        author_email='dbsgeo@gmail.com',
        platforms='OS Independent',
        license='GPlv2',
        url='http://mapnik-utils.googlecode.com/',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
            ],
        )