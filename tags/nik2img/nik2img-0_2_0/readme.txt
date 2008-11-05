
Nik2img.py 0.2.0
Copyright 2008, Dane Springmeyer (dbsgeo [ -a- ] gmail.com)
======================================

A command line utility to take a mapnik xml or mml file as input and output an image.

To run this program:
   Make sure you have Mapnik installed
   Then install or run locally

To Install:
   $ wget http://mapnik-utils.googlecode.com/svn/tags/nik2img/nik2img-0_2_0.tar
   $ tar xvf nik2img-0_2_0.tar
   $ cd nik2img-0_2_0
   $ sudo python setup.py install
   This will place nik2img.py in `/usr/local/bin` and as a python module in `site-packages`

Test Installation of module:
   $ python
   >>> from nik2img import Map # should prompt no error
   >>> m = Map('/path/to/mapfile.xml')
   >>> m.test() # should confirm path to mapfile

Test Installation of command-line script:
   $ nik2img.py # should be able to tab complete...
   $ which nik2img.py # should show install location
   $ nik2img.py -h # should display usage

To run locally:
   Download the script from: http://mapnik-utils.googlecode.com/svn/tags/nik2img/nik2img-0_2_0/nik2img.py
   Then in that directory run:
   $ python nik2img.py

For more info see: http://code.google.com/p/mapnik-utils/wiki/Nik2Img