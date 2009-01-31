------------------------
Macports Portfile for Mapnik
------------------------

Overview
--------

Portfile adapted from http://trac.macports.org/ticket/12784

Also see: http://trac.macports.org/ticket/18071

Available here for testing against SVN Trunk


Steps to test
-----------

1. Make a 'port/graphics' directory in your user folder like::

 $ mkdir -p ~/ports/graphics

2. Checkout the mapnik-utils portfile into a folder within 'graphics' named 'mapnik'::

 $ cd ~/ports/graphics
 $ svn co http://mapnik-utils.googlecode.com/svn/sandbox/port/ ~/ports/graphics/mapnik
 
3. Open for editing the 'sources.conf' file for Macports::

 $ vim /opt/local/etc/macports/sources.conf

4.  Add a line before the line that says 'rsync://' to point to your '~/ports' folder::

  file:///Users/YOUR_USER/ports/

5. In your terminal go into your users ports directory::

 $ cd ~/ports

6. Run the 'portindex' command::

 $ portindex

7. Then to install run (do 'port -d' for debug output)::

 $ sudo port install jam
 $ sudo port install boost +icu +python25
 $ sudo port install boost mapnik

8. Post your problems or successes to http://code.google.com/p/mapnik-utils/issues/list

More info: http://guide.macports.org/#development.local-repositories


