----------------------------
Macports Portfile for Mapnik
----------------------------

Overview
--------

This is a testing sandbox for building Mapnik using Macports.

Mapnik 0.6.0 was accepted into the Macport tree on May 1, 2009 (http://trac.macports.org/changeset/50499)

This Portfile was originally adapted from http://trac.macports.org/ticket/12784 (thanks Paul!).

Requirements
------------

 * Python26 from Macports
 * Boost +python26 variant

Issues
------

 * Cairo variant not yet working because pycairo cannot be found (some pkg-config problem)
 * Provide a few more variants for xml_parser, etc
 * SQLITE Rtree support
 * write a tool to validate/test python linking
 * break off a mapnik-devel port to track trunk


Using Portfile Locally
----------------------

1. Make a 'port/graphics' directory in your USER folder like::

  $ mkdir -p ~/ports/graphics

2. Checkout the mapnik-utils portfile into a folder within 'graphics' named 'mapnik'::

  $ svn co http://mapnik-utils.googlecode.com/svn/sandbox/ports/ ~/ports/
 
3. Open for editing the 'sources.conf' file for Macports::

  $ sudo vim /opt/local/etc/macports/sources.conf

4. Add a line before the line that says 'rsync://' to point to your '~/ports' folder::

  file:///Users/YOUR_USER/ports/ [nosync]

5. In your terminal go into the mapnik directory::

  $ cd ~/ports/

6. Run the 'portindex' command::

  $ portindex

7. Then to install run from anywhere (do 'port -d' for debug output)::
  
  # make sure you have installed Macports and XCode
  $ sudo port install jam python26 python_select
  $ sudo python_select python26 # see below for more info on python_select
  $ sudo port install boost +icu +python26
  $ sudo port install py26-mapnik # to install
  $ sudo port uninstall py26-mapnik # to remove

8. Post your problems or successes to http://code.google.com/p/mapnik-utils/issues/list

9. More info on local Portfile development: http://guide.macports.org/#development.local-repositories

10. Just in case you need manually uninstall do::
  
  $ sudo rm -rf /opt/local/bin/shapeindex
  $ sudo rm -rf /opt/local/include/mapnik
  $ sudo rm -rf /opt/local/lib/mapnik
  $ sudo rm /opt/local/lib/libmapnik.dylib
  $ sudo rm -rf /opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/mapnik


Notes on 'python_select'
------------------------

If you want to use Mapnik built with Macports you have to switch to the Macports Python.
That's just the way that MacPorts works, for better or worse.

The python_select tool available via macports is a fairly handy way to switch your
default python interpreter between various versions of python installed on your system.

It is able to autodetect all macports versions and the one system-provided python.

First run this command to see the list of python versions available to switch to::

  $ python_select -l
  Available versions:
  current none python25 python25-apple

Note that if you have a MacPython version installed, such as Python 2.6, python_select will not detect it.

So, if you want to switch back to that MacPython version run the command::

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