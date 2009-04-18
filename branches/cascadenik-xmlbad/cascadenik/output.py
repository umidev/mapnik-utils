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
    def __init__(self, color, opacity=None):
        assert color.__class__ is style.color
        assert opacity is None or type(opacity) in (int, float)

        self.color = color
        self.opacity = opacity

    def __repr__(self):
        return 'Polygon(%s, %s)' % (self.color, self.opacity)

class LineSymbolizer:
    def __init__(self, color, width, opacity=None, join=None, cap=None, dashes=None):
        assert color.__class__ is style.color
        assert type(width) in (int, float)
        assert opacity is None or type(opacity) in (int, float)
        assert join is None or type(join) is str
        assert cap is None or type(cap) is str
        assert dashes is None or dashes.__class__ is style.numbers

        self.color = color
        self.width = width
        self.opacity = opacity
        self.join = join
        self.cap = cap
        self.dashes = dashes

    def __repr__(self):
        return 'Line(%s, %s)' % (self.color, self.width)

class TextSymbolizer:
    def __init__(self, face_name, size, color=None, wrap_width=None, \
        spacing=None, label_position_tolerance=None, max_char_angle_delta=None, \
        halo_color=None, halo_radius=None, dx=None, dy=None, avoid_edges=None, \
        min_distance=None, allow_overlap=None, placement=None):

        assert type(face_name) is str
        assert type(size) is int
        assert color is None or color.__class__ is style.color
        assert wrap_width is None or type(wrap_width) is int
        assert spacing is None or type(spacing) is int
        assert label_position_tolerance is None or type(label_position_tolerance) is int
        assert max_char_angle_delta is None or type(max_char_angle_delta) is int
        assert halo_color is None or halo_color.__class__ is style.color
        assert halo_radius is None or type(halo_radius) is int
        assert dx is None or type(dx) is int
        assert dy is None or type(dy) is int
        assert avoid_edges is None or avoid_edges.__class__ is style.boolean
        assert min_distance is None or type(min_distance) is int
        assert allow_overlap is None or allow_overlap.__class__ is style.boolean
        assert placement is None or type(placement) is str

        self.face_name = face_name
        self.size = size

        self.color = color
        self.wrap_width = wrap_width
        self.spacing = spacing
        self.label_position_tolerance = label_position_tolerance
        self.max_char_angle_delta = max_char_angle_delta
        self.halo_color = halo_color
        self.halo_radius = halo_radius
        self.dx = dx
        self.dy = dy
        self.avoid_edges = avoid_edges
        self.min_distance = min_distance
        self.allow_overlap = allow_overlap
        self.placement = placement

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
    def __init__(self, file, filetype, width, height, allow_overlap=None):
        assert type(file) is str
        assert type(filetype) is str
        assert type(width) is int
        assert type(height) is int
        assert allow_overlap is None or allow_overlap.__class__ is style.boolean

        self.file = file
        self.type = filetype
        self.width = width
        self.height = height
        self.allow_overlap = allow_overlap

    def __repr__(self):
        return 'Point(%s)' % self.file

class PolygonPatternSymbolizer(PointSymbolizer):
    def __init__(self, file, filetype, width, height):
        PointSymbolizer.__init__(self, file, filetype, width, height)
    
    def __repr__(self):
        return 'PolyPat(%s)' % self.file

class LinePatternSymbolizer(PointSymbolizer):
    def __init__(self, file, filetype, width, height):
        PointSymbolizer.__init__(self, file, filetype, width, height)
    
    def __repr__(self):
        return 'LinePat(%s)' % self.file
