----------------------------
Macports Portfile for Mapnik
----------------------------

Overview
--------

This is a testing sandbox for building Mapnik SVN Head using Macports.

'py25-mapnik' is under development and once ready will be branched into a 'py26' version.

The port script takes advantage of new options in the 0.6.0 release to handle custom builds.
One example is the ability to request linking against the non-system/framework version of
Python with FRAMEWORK_PYTHON=False.
(see http://lists.berlios.de/pipermail/mapnik-users/2008-April/000865.html)

This Portfile was originally adapted from http://trac.macports.org/ticket/12784 (thanks Paul!).
See also: http://trac.macports.org/ticket/18071


Issues
------

Currently one major issue prevents a proper build:
 
1. A bug in the macports version of boost prevents boost from linking against the
  macports version of python, while this 'py25-mapnik' is able to correctly link
  against the macports boost. This results in a 'Python Version Mismatch' error.
  
  See:
    http://trac.mapnik.org/wiki/InstallationTroubleshooting#PythonVersionMismatch
  
  Details on the boost bug:
    http://trac.macports.org/ticket/17998

  Boost portfile:
    http://trac.macports.org/browser/trunk/dports/devel/boost/Portfile
  
  Related:
    http://trac.macports.org/ticket/15099
    http://trac.macports.org/ticket/16111
  
2. And several todo items remain:
    * Get cairo support working/tested
    * troubleshoot library linking issues
     - Currently requires `export DYLD_LIBRARY_PATH=/opt/local/lib/mapnik/`
    * provide a few more variants for xml_parser, etc
    * write a tool to validate/test python linking
    * break off py26 port
    * break off a mapnik-devel port to track trunk


Using Portfile Locally
----------------------

1. Make a 'port/graphics' directory in your user folder like::

  $ mkdir -p ~/ports/graphics

2. Checkout the mapnik-utils portfile into a folder within 'graphics' named 'mapnik'::

  $ svn co http://mapnik-utils.googlecode.com/svn/sandbox/ports/ ~/ports/
 
3. Open for editing the 'sources.conf' file for Macports::

  $ sudo vim /opt/local/etc/macports/sources.conf

4. Add a line before the line that says 'rsync://' to point to your '~/ports' folder::

  file:///Users/YOUR_USER/ports/

5. In your terminal go into the mapnik directory::

  $ cd ~/ports/

6. Run the 'portindex' command::

  $ portindex

7. Then to install run from anywhere (do 'port -d' for debug output)::
  
  # make sure you have installed Macports and XCode
  $ sudo port install jam python25 python_select
  $ sudo port install boost +icu +python25
  $ sudo python_select python25 # see below for more info on python_select
  $ sudo port install py25-mapnik # to install
  $ sudo port uninstall py25-mapnik # to remove

8. Post your problems or successes to http://code.google.com/p/mapnik-utils/issues/list

9. More info on local Portfile development: http://guide.macports.org/#development.local-repositories

10. Just in case you need manually uninstall do::
  
  $ sudo rm -rf /opt/local/bin/shapeindex
  $ sudo rm -rf /opt/local/include/mapnik
  $ sudo rm -rf /opt/local/lib/mapnik
  $ sudo rm /opt/local/lib/libmapnik.dylib
  $ sudo rm -rf /opt/local/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/site-packages/mapnik


Notes on 'python_select'
------------------------

If you want to use Mapnik built with Macports you have to switch to the Macports Python.
Thats just the way that MacPorts works, for better or worse.

The python_select tool available via macports is a fairly handy way to switch your
default python interpreter between various versions of python installed on your system.

It is able to autodetect all macports versions and the one system-provided python.

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