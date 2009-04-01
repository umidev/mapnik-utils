from mapnik.ogcserver.WMS import BaseWMSFactory

class WMSFactory(BaseWMSFactory):
  def __init__(self):
    BaseWMSFactory.__init__(self)
    self.loadXML('population.xml')
    self.finalize()
