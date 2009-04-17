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

    property_map = {'polygon-fill': 'fill', 'polygon-opacity': 'fill-opacity'}

    def __init__(self, fill=None, opacity=None):
        self.fill = fill
        self.opacity = opacity

    def __repr__(self):
        return 'Polygon(%s, %s)' % (self.fill, self.opacity)

class LineSymbolizer:
    
    def __init__(self, color, width):
        self.color = color
        self.width = width
        
        self.opacity = None
        self.join = None
        self.cap = None
        self.dasharray = None
