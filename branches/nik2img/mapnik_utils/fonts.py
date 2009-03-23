from mapnik import FontEngine, paths

class FontHandler(object):
    def __init__(self):
        self.added = []
        self.failed = []
        self.fontdir = paths.fontscollectionpath
    
    @property
    def available(self):
        return [f for f in FontEngine.face_names()]

    def add_fonts(self,fonts):
        engine = FontEngine.instance()
        for font in fonts:
            if engine.register_font(font):
                self.added.append(font)
            else:
                self.failed.append(font)