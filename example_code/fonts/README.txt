# Grab the Fontin Sans Open Type font
http://www.josbuivenga.demon.nl/fontinsans.html

# Unzip into your default mapnik folder (/usr/local/lib/mapnik/fonts)

#
# Change mapnik/__init__.py (installed in your site-packages folder when you build mapnik) to load both .ttf and .otf fonts found in that folder by default
#

from mapnik import DatasourceCache
DatasourceCache.instance().register_datasources('%s' % inputpluginspath)
#register some fonts
from mapnik import FontEngine
from glob import glob
fonts = glob('%s/*.ttf' % fontscollectionpath) + glob('%s/*.otf' % fontscollectionpath)
if len( fonts ) == 0:
    print "### WARNING: No ttf or otf files found in '%s'." % fontscollectionpath
else:
    map(FontEngine.instance().register_font, fonts)

#set dlopen flags back to the original
setdlopenflags(flags)


#
# Check what fonts mapnik can read
#

from mapnik import *
for name in FontEngine.instance().face_names():
    print name

# Now you can call Open Type Fonts by their face name in mapnik projects
<TextSymbolizer name="NAME" face_name="Fontin Sans Small Caps" size="12" fill="white" halo_fill= "#2E2F39" halo_radius="1" wrap_width="20" spacing="5" allow_overlap="false" avoid_edges="true" min_distance="10"/>