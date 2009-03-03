------------------------
Macports Portfile for Mapnik
------------------------

Overview
--------

Portfile adapted from http://trac.macports.org/ticket/12784

Also see: http://trac.macports.org/ticket/18071

And Macports bugs affecting build:
http://trac.macports.org/ticket/17998
http://trac.macports.org/ticket/15099#comment:11
http://trac.macports.org/ticket/16111
https://lists.berlios.de/pipermail/mapnik-users/2008-April/000865.html

Boost portfile:
http://trac.macports.org/browser/trunk/dports/devel/boost/Portfile

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

 $ sudo port install jam python25 python_select
 $ sudo port install boost +icu +python25
 $ sudo python_select python25 # see below for more info on python_select
 $ sudo port install mapnik

8. Post your problems or successes to http://code.google.com/p/mapnik-utils/issues/list

More info: http://guide.macports.org/#development.local-repositories



To uninstall mapnik run::

sudo rm -rf /opt/local/bin/shapeindex
sudo rm -rf /opt/local/include/mapnik
sudo rm -rf /opt/local/lib/mapnik
sudo rm  /opt/local/lib/libmapnik.dylib
sudo rm -rf /opt/local/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/site-packages/mapnik


python_select tool
----------------

The python_select tool available via macports is a fairly handy way to switch your
default python interpreter between various versions of python installed on your system.

It is able to autodetect all macports versions and the system-provided python.

First run this command to see the list of python versions it is able to switch to::

 $ python_select -l
 Available versions:
 current none python25 python25-apple

Note that if you have a MacPython version installed, such as Python 2.6, python_select will not detect it.
Run the command::

 $ python_select -n python25-apple

Which will give you a sample of the commands needed to switch back to the system python 2.5.
You can manually modify these to enable switching to the python 2.6 version::

 $ sudo ln -sf python26 /opt/local/etc/select/python/current
 $ sudo ln -snf /usr/bin/python2.6 /opt/local/bin/python
 $ sudo ln -snf /usr/bin/pythonw2.6 /opt/local/bin/pythonw
 $ sudo ln -snf /usr/bin/python2.6-config /opt/local/bin/python-config
 $ sudo rm -f /opt/local/bin/idle
 $ sudo ln -snf /usr/bin/pydoc2.6 /opt/local/bin/pydoc
 $ sudo ln -snf /usr/bin/smtpd2.6.py /opt/local/bin/smtpd.py
 $ sudo rm -f /opt/local/share/man/man1/python.1
 $ sudo ln -snf /usr/share/man/man1/python2.6.1.gz /opt/local/share/man/man1/python.1.gz
 $ sudo rm -f /opt/local/Library/Frameworks/Python.framework/Versions/Current
 $ sudo rm -f /opt/local/Library/Frameworks/Python.framework/Headers
 $ sudo rm -f /opt/local/Library/Frameworks/Python.framework/Resources
 $ sudo rm -f /opt/local/Library/Frameworks/Python.framework/Python

