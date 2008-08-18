## Build notes for TileCache Tutorial on Mac OS 10.5 ##

A companion to the tutorial here: http://www.paolocorti.net/2008/08/06/a-day-with-tilecache-generating-kml-super-overlays/

# Note, Mac OS comes pre-installed with Apache so only mod_python is needed.

# Install mod_python
svn co https://svn.apache.org/repos/asf/quetzalcoatl/mod_python/trunk/ mod_python
cd mod_python
./configure
make
sudo make install

# Make backup of apache configuration file
cp /private/etc/apache2/httpd.conf /private/etc/apache2/httpd_original.conf

# Make test directory and give ownership to Apache user
mkdir /Library/WebServer/Documents/test
chgrp www /Library/WebServer/Documents/test
chown www /Library/WebServer/Documents/test

# Open apache config in default text editor
open /private/etc/apache2/httpd.conf

### Make the below additions to http.conf ###
# Add load instructions for mod_python
LoadModule python_module libexec/apache2/mod_python.so

# Add mod_python directive
AddHandler mod_python .py
PythonHandler mptest
PythonDebug On

# Then create the hello world python file and make executable
touch /Library/WebServer/Documents/test/mptest.py
chmod +x /Library/WebServer/Documents/test/mptest.py

# Open up in text editor to add sample code
open /Library/WebServer/Documents/test/mptest.py

# Test and restart apache
apachectl configtest
apachectl restart

# Or go to System Preferences > Sharing > Web Sharing (check it)

# Go to test url in browser
open http://localhost/test/mptest.py

# If you experience any problems open up the apache error log
open /private/var/log/apache2/error_log

# Install TileCache
svn co http://svn.tilecache.org/trunk/tilecache tilecache
cp -r tilecache/ /Library/WebServer/Documents/

# Make cache directory
mkdir /Library/WebServer/Documents/cache
chgrp www /Library/WebServer/Documents/cache
chown www /Library/WebServer/Documents/cache

# Open apache config again in default text editor
open /private/etc/apache2/httpd.conf

### Make the below additions to http.conf ###
# Add tilecache directive
AddHandler python-program .py
PythonHandler TileCache.Service
PythonPath "['/Library/WebServer/Documents/tilecache'] + sys.path"
PythonOption TileCacheConfig "/Library/WebServer/Documents/tilecache/tilecache.cfg"
PythonDebug Off

# Open the tilecache.cfg to edit
open /Library/WebServer/Documents/tilecache/tilecache.cfg

# Change this line as such:
base=/Library/WebServer/Documents/cache

# Test and restart apache
apachectl configtest
apachectl restart

# Open sample html page in browser
open /Library/WebServer/Documents/tilecache/index.html

# proceed with modifying the javascript to extend example…

# Send a big thanks to Diego and Chris!