from distutils.core import setup

version = '0.4.0'
app = 'nik2img'
description = 'A mapfile to image generator for the Mapnik C++/Python mapping toolkit'
url = 'http://mapnik-utils.googlecode.com/'
readme = file('README.txt','rb').read()

setup(name='%s' % app,
      version=version,
      description=description,
      long_description=readme,
      author='Dane Springmeyer',
      author_email='dbsgeo@gmail.com',
      requires=['Mapnik'],
      keywords='mapnik,gis,geospatial,shp2img',
      url=url,
      #py_modules=['%s' % app],
      packages=['mapnik_utils'],
      scripts = ['nik2img.py'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: GIS',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Utilities'],
      )
