from mapnik.ogcserver.WMS import BaseWMSFactory
from mapnik import Shapefile, Layer, Style, Rule, Color, PolygonSymbolizer, LineSymbolizer

SHAPEFILE = '/Users/spring/projects/mapnik-utils/trunk/serverside/wms/world_borders'

class WMSFactory(BaseWMSFactory):
  def __init__(self):
    BaseWMSFactory.__init__(self)
    sty = Style()
    rl = Rule()
    rl.symbols.append(PolygonSymbolizer(Color('#f2eff9')))
    rl.symbols.append(LineSymbolizer(Color('steelblue'),.1))
    sty.rules.append( rl )
    self.register_style('s', sty)
    lyr = Layer('world','+init=epsg:4326')
    lyr.title = 'World Borders'
    lyr.abstract = 'World Test'
    lyr.queryable = True
    lyr.datasource = Shapefile(file=SHAPEFILE)
    lyr.styles.append('s')
    self.register_layer(lyr,'s',('s',))
    self.finalize()
