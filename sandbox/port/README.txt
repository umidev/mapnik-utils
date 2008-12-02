-------------------------------------------------------
MACPortfile for Mapnik
-------------------------------------------------------
1. Edit the Sources file for macports (/opt/local/etc/sources.conf)
2. Scroll down to the line that says rsync:// add a new line before that, 
    file:///Users/YOUR USERNAME/ports
3. mkdir -p ~/ports/graphics/mapnik
4. copy the port file to the newly created directory
5. cd ~/ports
6. portindex
7. port install mapnik

Should be expanded more i guess
Instructions adapted from 
http://guide.macports.org/#development.local-repositories


