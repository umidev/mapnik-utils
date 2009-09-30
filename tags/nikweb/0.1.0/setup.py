#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(name='Nikweb',
    version='0.1.0',
    description="A GeoJSON web service for Mapnik",
    long_description="Submit GeoJSON feature data via HTTP request, and receive your Mapnik map rendered with the feature data in the appropriate places.",
    author='Robert Coup',
    author_email='robert@coup.net.nz',
    requires=['mapnik (>=0.6.0)'],
    provides=['nikweb'],
    keywords='mapnik,gis,geospatial,webob,django',
    url='http://code.google.com/p/mapnik-utils/',
    packages=['nikweb', 'nikweb.http'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Utilities'],
)
