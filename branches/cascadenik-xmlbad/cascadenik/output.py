import style

class Rule:
    def __init__(self, minscale, maxscale, filter, *symbolizers):
        self.minscale = minscale
        self.maxscale = maxscale
        self.filter = filter
        self.symbolizers = symbolizers

    def __repr__(self):
        return 'Rule(%s:%s, %s, %s)' % (repr(self.minscale), repr(self.maxscale), repr(self.filter), repr(self.symbolizers))

class MinScaleDenominator:
    def __init__(self, value):
        assert type(value) is int
        self.value = value

    def __repr__(self):
        return str(self.value)

class MaxScaleDenominator:
    def __init__(self, value):
        assert type(value) is int
        self.value = value

    def __repr__(self):
        return str(self.value)

class Filter:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return str(self.text)

class PolygonSymbolizer:
    def __init__(self, fill, opacity=None):
        assert fill.__class__ is style.color
        assert type(opacity) in (int, float) or opacity is None
        self.fill = fill
        self.opacity = opacity

    def __repr__(self):
        return 'Polygon(%s, %s)' % (self.fill, self.opacity)

class LineSymbolizer:
    def __init__(self, color, width):
        assert color.__class__ is style.color
        assert type(width) in (int, float)
        self.color = color
        self.width = width

    def __repr__(self):
        return 'Line(%s, %s)' % (self.color, self.width)

class TextSymbolizer:
    def __init__(self, face_name, size):
        assert type(size) is int
        self.face_name = face_name
        self.size = size

    def __repr__(self):
        return 'Text(%s, %s)' % (self.face_name, self.size)

class ShieldSymbolizer:
    def __init__(self, face_name, size, file, filetype, width, height):
        assert type(size) is int
        assert type(width) is int
        assert type(height) is int
        self.face_name = face_name
        self.size = size
        self.file = file
        self.type = filetype
        self.width = width
        self.height = height

    def __repr__(self):
        return 'Shield(%s, %s, %s)' % (self.face_name, self.size, self.file)

class PointSymbolizer:
    def __init__(self, file, filetype, width, height):
        assert type(width) is int
        assert type(height) is int
        self.file = file
        self.type = filetype
        self.width = width
        self.height = height

    def __repr__(self):
        return 'Point(%s)' % self.file

class PolygonPatternSymbolizer(PointSymbolizer):
    def __repr__(self):
        return 'PolyPat(%s)' % self.file

class LinePatternSymbolizer(PointSymbolizer):
    def __repr__(self):
        return 'LinePat(%s)' % self.file
