from mapnik.ogcserver.WMS import BaseWMSFactory
from mapnik import * #Shapefile, Layer, Style, Rule, Color, PolygonSymbolizer, LineSymbolizer

SHAPEFILE = '/Users/spring/projects/utils/data/world_borders'
PROJ4_STRING = '+init=epsg:4326'

# Switch to these settings to use data in mercator projection from: http://tile.openstreetmap.org/world_boundaries-spherical.tgz 
#PROJ4_STRING = '+init=epsg:3395'
#SHAPEFILE = '/Users/spring/projects/mapnik-utils/trunk/sample_data/world_boundaries_m'

# Example query string for reprojected data:
# http://localhost/cgi-bin/mapnikwms.py?LAYERS=world&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&EXCEPTIONS=application%2Fvnd.ogc.se_inimage&FORMAT=image%2Fpng&SRS=EPSG%3A3395&BBOX=-20037400.000000,-19929239.110000,%2020037400.000000,18375854.709643&WIDTH=256&HEIGHT=256

class WMSFactory(BaseWMSFactory):
  def __init__(self):
    BaseWMSFactory.__init__(self)
    sty = Style()
    rl = Rule()
    rl.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
    rl.symbols.append(LineSymbolizer(Color('steelblue'),.1))
    sty.rules.append( rl )
    self.register_style('s', sty)
    lyr = Layer('world',PROJ4_STRING)
    lyr.title = 'World Borders'
    lyr.abstract = 'World Test'
    lyr.queryable = True
    lyr.datasource = Shapefile(file=SHAPEFILE)
    self.register_layer(lyr,'s',('s',))
    self.finalize()