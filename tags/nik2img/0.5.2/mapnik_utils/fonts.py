from mapnik_utils.version_adapter import Mapnik

mapnik = Mapnik()


class FontHandler(object):
    def __init__(self):
        self.added = []
        self.failed = []
        self.fontdir = mapnik.fontscollectionpath
    
    @property
    def available(self):
        return [f for f in mapnik.FontEngine.face_names()]

    def add_fonts(self,fonts):
        engine = mapnik.FontEngine.instance()
        for font in fonts:
            if engine.register_font(font):
                self.added.append(font)
            else:
                self.failed.append(font)