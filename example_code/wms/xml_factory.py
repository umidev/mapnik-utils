from mapnik.ogcserver.WMS import BaseWMSFactory

# note, this class for loading an xml map requires patch from http://trac.mapnik.org/ticket/129

class WMSFactory(BaseWMSFactory):
  def __init__(self):
    BaseWMSFactory.__init__(self)
    self.loadXML('/Users/spring/projects/mapnik-utils/example_code/wms/population.xml')
    self.finalize()
