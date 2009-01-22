From Jochen Topf at http://www.geofabrik.de

More info: http://lists.berlios.de/pipermail/mapnik-users/2008-June/000986.html


To generate an html view of your mapfile on the commandline do:

$ xsltproc stylesheet.xsl mapfile.xml > view.html

To transform on-the-fly in a browser simply add this line to the second line of your mapfile.xml:

<?xml-stylesheet type="text/xsl" href="mapnik-overview.xsl"?>

Then open your mapfile.xml in a browser.