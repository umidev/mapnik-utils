Test Suite for Indic Font Support
---------------------------------

Currently indic fonts are not rendered correctly by mapnik.

See: https://trac.mapnik.org/ticket/112

To set up the tests do:

Create a PostGIS test database::

 $ createdb -T template_postgis test

Add the test data to it::

 $ psql -U postgres -f mrdata.sql test

Then run the python script to generate and image and xml config::

 $ python run_test.py

From then on you can run nik2img.py on the xml::

 $ nik2img.py -m mapfile.xml -o test.png --fonts fonts/gargi.ttf