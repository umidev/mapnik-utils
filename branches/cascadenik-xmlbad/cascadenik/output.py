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
