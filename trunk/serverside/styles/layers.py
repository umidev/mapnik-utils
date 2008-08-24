import os, sys
import pprint
import urllib
import urlparse
import tempfile
import StringIO
from operator import lt, le, eq, ge, gt
import xml.etree.ElementTree
from xml.etree.ElementTree import Element
import cascade
import PIL.Image

counter = 0

opsort = {lt: 1, le: 2, eq: 3, ge: 4, gt: 5}
opstr = {lt: '<', le: '<=', eq: '==', ge: '>=', gt: '>'}
    
class Range:
    """ Represents a range for use in min/max scale denominator.
    
        Ranges can have a left side, a right side, neither, or both,
        with sides specified as inclusive or exclusive.
    """
    def __init__(self, leftop=None, leftedge=None, rightop=None, rightedge=None):
        assert leftop in (lt, le, eq, ge, gt, None)
        assert rightop in (lt, le, eq, ge, gt, None)

        self.leftop = leftop
        self.rightop = rightop
        self.leftedge = leftedge
        self.rightedge = rightedge

    def midpoint(self):
        """ Return a point guranteed to fall within this range, hopefully near the middle.
        """
        minpoint = self.leftedge

        if self.leftop is gt:
            minpoint += 1
    
        maxpoint = self.rightedge

        if self.rightop is lt:
            maxpoint -= 1

        if minpoint is None:
            return maxpoint
            
        elif maxpoint is None:
            return minpoint
            
        else:
            return (minpoint + maxpoint) / 2

    def isOpen(self):
        """ Return true if this range has any room in it.
        """
        if self.leftedge > self.rightedge:
            return False

        if self.leftedge == self.rightedge:
            if self.leftop is gt or self.rightop is lt:
                return False

        return True
    
    def __repr__(self):
        """
        """
        if self.leftedge == self.rightedge and self.leftop is ge and self.rightop is le:
            # equivalent to ==
            return '(=%s)' % self.leftedge
    
        try:
            return '(%s%s ... %s%s)' % (self.leftedge, opstr[self.leftop], opstr[self.rightop], self.rightedge)
        except KeyError:
            try:
                return '(... %s%s)' % (opstr[self.rightop], self.rightedge)
            except KeyError:
                return '(%s%s ...)' % (self.leftedge, opstr[self.leftop])

def selectors_ranges(selectors):
    """ Given a list of selectors and a map, return a list of Ranges that
        fully describes all possible unique slices within those selectors.
        
        If the map looks like it uses the well-known Google/VEarth maercator
        projection, accept "zoom" attributes in place of "scale-denominator".
        
        This function was hard to write, it should be hard to read.
    """
    repeated_breaks = []
    
    # start by getting all the range edges from the selectors into a list of break points
    for selector in selectors:
        for test in selector.rangeTests():
            repeated_breaks.append(test.rangeOpEdge())
    
    # from here on out, *order will matter*
    # it's expected that the breaks will be sorted from minimum to maximum,
    # with greater/lesser/equal operators accounted for.
    repeated_breaks.sort(key=lambda (o, e): (e, opsort[o]))
    
    breaks = []

    # next remove repetitions from the list
    for (i, (op, edge)) in enumerate(repeated_breaks):
        if i > 0:
            if op is repeated_breaks[i - 1][0] and edge == repeated_breaks[i - 1][1]:
                continue

        breaks.append(repeated_breaks[i])

    ranges = []
    
    # now turn those breakpoints into a list of ranges
    for (i, (op, edge)) in enumerate(breaks):
        if i == 0:
            # get a right-boundary for the first range
            if op in (lt, le):
                ranges.append(Range(None, None, op, edge))
            elif op in (eq, ge):
                ranges.append(Range(None, None, lt, edge))
            elif op is gt:
                ranges.append(Range(None, None, le, edge))

        elif i > 0:
            # get a left-boundary based on the previous right-boundary
            if ranges[-1].rightop is lt:
                ranges.append(Range(ge, ranges[-1].rightedge))
            else:
                ranges.append(Range(gt, ranges[-1].rightedge))

            # get a right-boundary for the current range
            if op in (lt, le):
                ranges[-1].rightop, ranges[-1].rightedge = op, edge
            elif op in (eq, ge):
                ranges[-1].rightop, ranges[-1].rightedge = lt, edge
            elif op is gt:
                ranges[-1].rightop, ranges[-1].rightedge = le, edge

            # equals is a special case, sometimes
            # an extra element may need to sneak in.
            if op is eq:
                if ranges[-1].leftedge == edge:
                    # the previous range also covered just this one slice.
                    ranges.pop()
            
                # equals is expressed as greater-than-equals and less-than-equals.
                ranges.append(Range(ge, edge, le, edge))
            
        if i == len(breaks) - 1:
            # get a left-boundary for the final range
            if op in (lt, ge):
                ranges.append(Range(ge, edge))
            else:
                ranges.append(Range(gt, edge))

    ranges = [range for range in ranges if range.isOpen()]
    
    # print breaks
    # print ranges
    
    if ranges:
        return ranges

    else:
        # if all else fails, return a Range that covers everything
        return [Range()]

def next_counter():
    global counter
    counter += 1
    return counter

def is_gym_projection(map):
    """ Return true if the map projection matches that used by VEarth, Google, OSM, etc.
    
        Will be useful for a zoom-level shorthand for scale-denominator.
    """ 
    # expected
    gym = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null'
    gym = dict([p.split('=') for p in gym.split() if '=' in p])
    
    # observed
    srs = map.get('srs', '')
    srs = dict([p.split('=') for p in srs.split() if '=' in p])
    
    for p in gym:
        if srs.get(p, None) != gym.get(p, None):
            return False

    return True

def extract_declarations(map, base):
    """ Given a Map element and a URL base string, remove and return a complete
        list of style declarations from any Stylesheet elements found within.
    """
    declarations = []
    
    for stylesheet in map.findall('Stylesheet'):
        map.remove(stylesheet)
    
        if 'src' in stylesheet.attrib:
            url = urlparse.urljoin(base, stylesheet.attrib['src'])
            styles, local_base = urllib.urlopen(url).read(), url

        elif stylesheet.text:
            styles, local_base = stylesheet.text, base

        else:
            continue
            
        rulesets = cascade.parse_stylesheet(styles, base=local_base, is_gym=is_gym_projection(map))
        declarations += cascade.unroll_rulesets(rulesets)

    return declarations

def make_ranged_rule_element(range):
    """ Given a Range, return a Rule element prepopulated
        with applicable min/max scale denominator elements.
    """
    rule = Element('Rule')

    if range.leftedge:
        minscale = Element('MinScaleDenominator')
        rule.append(minscale)
    
        if range.leftop is ge:
            minscale.text = str(range.leftedge)
        elif range.leftop is gt:
            minscale.text = str(range.leftedge + 1)
    
    if range.rightedge:
        maxscale = Element('MaxScaleDenominator')
        rule.append(maxscale)
    
        if range.rightop is le:
            maxscale.text = str(range.rightedge)
        elif range.rightop is lt:
            maxscale.text = str(range.rightedge - 1)
    
    rule.tail = '\n        '
    
    return rule

def insert_layer_style(map, layer, style):
    """ Given a Map element, a Layer element, and a Style element, insert the
        Style element into the flow and point to it from the Layer element.
    """
    style.tail = '\n    '
    map.insert(map._children.index(layer), style)
    
    stylename = Element('StyleName')
    stylename.text = style.get('name')
    stylename.tail = '\n        '
    layer.insert(layer._children.index(layer.find('Datasource')), stylename)

def add_map_style(map, declarations):
    """
    """
    property_map = {'map-bgcolor': 'bgcolor'}
    
    for dec in declarations:
        if dec.property.name in property_map:
            map.set(property_map[dec.property.name], str(dec.value))

def add_polygon_style(map, layer, declarations):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a PolygonSymbolizer, add it to Map
        and refer to it in Layer.
    """
    property_map = {'polygon-fill': 'fill', 'polygon-opacity': 'fill-opacity'}
    
    # just the ones we care about here
    declarations = [dec for dec in declarations if dec.property.name in property_map]

    # place to put rule elements
    rules = []
    
    for range in selectors_ranges([dec.selector for dec in declarations]):
        has_poly = False
        symbolizer = Element('PolygonSymbolizer')
        encountered = []
        
        # collect all the applicable declarations into a symbolizer element
        for dec in reversed(declarations):
            if dec.selector.inRange(range.midpoint()) and dec.property.name not in encountered:
                parameter = Element('CssParameter', {'name': property_map[dec.property.name]})
                parameter.text = str(dec.value)
                symbolizer.append(parameter)
    
                encountered.append(dec.property.name)
                has_poly = True
    
        if has_poly:
            rule = make_ranged_rule_element(range)
            rule.append(symbolizer)
            rules.append(rule)

    if rules:
        style = Element('Style', {'name': 'poly style %d' % next_counter()})
        style.text = '\n        '
        
        for rule in rules:
            style.append(rule)
        
        insert_layer_style(map, layer, style)

def add_line_style(map, layer, declarations):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a LineSymbolizer, add it to Map
        and refer to it in Layer.
    """
    property_map = {'line-color': 'stroke', 'line-width': 'stroke-width',
                    'line-opacity': 'stroke-opacity', 'line-join': 'stroke-linejoin',
                    'line-cap': 'stroke-linecap', 'line-dasharray': 'stroke-dasharray'}
    
    # just the ones we care about here
    declarations = [dec for dec in declarations if dec.property.name in property_map]

    # a place to put rule elements
    rules = []
    
    for range in selectors_ranges([dec.selector for dec in declarations]):
        has_line = False
        symbolizer = Element('LineSymbolizer')
        encountered = []
        
        # collect all the applicable declarations into a symbolizer element
        for dec in reversed(declarations):
            if dec.selector.inRange(range.midpoint()) and dec.property.name not in encountered:
                parameter = Element('CssParameter', {'name': property_map[dec.property.name]})
                parameter.text = str(dec.value)
                symbolizer.append(parameter)
    
                encountered.append(dec.property.name)
                has_line = True
    
        if has_line:
            rule = make_ranged_rule_element(range)
            rule.append(symbolizer)
            rules.append(rule)

    if rules:
        style = Element('Style', {'name': 'line style %d' % next_counter()})
        style.text = '\n        '
        
        for rule in rules:
            style.append(rule)
        
        insert_layer_style(map, layer, style)

def add_text_styles(map, layer, declarations):
    """ Given a Map element, a Layer element, and a list of declarations,
        create new Style elements with a TextSymbolizer, add them to Map
        and refer to them in Layer.
    """
    has_text = False
    property_map = {'text-face-name': 'face_name', 'text-size': 'size', 
                    'text-ratio': 'text_ratio', 'text-wrap-width': 'wrap_width', 'text-spacing': 'spacing',
                    'text-label-position-tolerance': 'label_position_tolerance',
                    'text-max-char-angle-delta': 'max_char_angle_delta', 'text-fill': 'fill',
                    'text-halo-fill': 'halo_fill', 'text-halo-radius': 'halo_radius',
                    'text-dx': 'dx', 'text-dy': 'dy',
                    'text-avoid-edges': 'avoid_edges', 'text-min-distance': 'min_distance',
                    'text-allow-overlap': 'allow_overlap', 'text-placement': 'placement'}

    # pull out all the names
    text_names = [dec.selector.elements[1].names[0]
                  for dec in declarations
                  if len(dec.selector.elements) is 2 and len(dec.selector.elements[1].names) is 1]

    # a separate style element for each text name
    for text_name in set(text_names):
    
        # just the ones we care about here
        name_declarations = [dec for dec in declarations
                             if dec.property.name in property_map and dec.selector.elements[1].names[0] == text_name]
    
        # a place to put rule elements
        rules = []
        
        for range in selectors_ranges([dec.selector for dec in name_declarations]):
            has_text = False
            symbolizer = Element('TextSymbolizer', {'name': text_name})
            
            for dec in name_declarations:
                if dec.selector.inRange(range.midpoint()):
                    symbolizer.set(property_map[dec.property.name], str(dec.value))
                    has_text = True
            
            if has_text:
                rule = make_ranged_rule_element(range)
                rule.append(symbolizer)
                rules.append(rule)

        if rules:
            style = Element('Style', {'name': 'text style %d (%s)' % (next_counter(), text_name)})
            style.text = '\n        '
            
            for rule in rules:
                style.append(rule)

            insert_layer_style(map, layer, style)

def add_point_style(map, layer, declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a PointSymbolizer, add it to Map
        and refer to it in Layer.
        
        Optionally provide an output directory for local copies of image files.
    """
    property_map = {'point-file': 'file', 'point-width': 'width',
                    'point-height': 'height', 'point-type': 'type',
                    'point-allow-overlap': 'allow_overlap'}
    
    # just the ones we care about here
    declarations = [dec for dec in declarations if dec.property.name in property_map]

    # a place to put rule elements
    rules = []
    
    for range in selectors_ranges([dec.selector for dec in declarations]):
        symbolizer = Element('PointSymbolizer')
        
        # collect all the applicable declarations into a symbolizer element
        for dec in reversed(declarations):
            if dec.selector.inRange(range.midpoint()):
                symbolizer.set(property_map[dec.property.name], str(dec.value))
    
        if symbolizer.get('file', False):
            # read the image to get some more details
            img_path = symbolizer.get('file')
            img_data = urllib.urlopen(img_path).read()
            img_file = StringIO.StringIO(img_data)
            img = PIL.Image.open(img_file)
            
            # save the image to a tempfile, making it a png no matter what
            (handle, path) = tempfile.mkstemp('.png', 'cascadenik-point-', out)
            os.close(handle)
            
            img.save(path)
            symbolizer.set('file', path)
            symbolizer.set('type', 'png')
            
            # if no width/height have been provided, set them
            if not (symbolizer.get('width', False) and symbolizer.get('height', False)):
                symbolizer.set('width', str(img.size[0]))
                symbolizer.set('height', str(img.size[1]))
            
            rule = make_ranged_rule_element(range)
            rule.append(symbolizer)
            rules.append(rule)

    if rules:
        style = Element('Style', {'name': 'point style %d' % next_counter()})
        style.text = '\n        '
        
        for rule in rules:
            style.append(rule)
        
        insert_layer_style(map, layer, style)

def add_pattern_style(map, layer, declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a PolygonPatternSymbolizer, add it to Map
        and refer to it in Layer.
        
        Optionally provide an output directory for local copies of image files.
    """
    property_map = {'pattern-file': 'file', 'pattern-width': 'width',
                    'pattern-height': 'height', 'pattern-type': 'type'}
    
    # just the ones we care about here
    declarations = [dec for dec in declarations if dec.property.name in property_map]

    # a place to put rule elements
    rules = []
    
    for range in selectors_ranges([dec.selector for dec in declarations]):
        symbolizer = Element('PolygonPatternSymbolizer')
        
        # collect all the applicable declarations into a symbolizer element
        for dec in reversed(declarations):
            if dec.selector.inRange(range.midpoint()):
                symbolizer.set(property_map[dec.property.name], str(dec.value))
    
        if symbolizer.get('file', False):
            # read the image to get some more details
            img_path = symbolizer.get('file')
            img_data = urllib.urlopen(img_path).read()
            img_file = StringIO.StringIO(img_data)
            img = PIL.Image.open(img_file)
            
            # save the image to a tempfile, making it a png no matter what
            (handle, path) = tempfile.mkstemp('.png', 'cascadenik-pattern-', out)
            os.close(handle)
            
            img.save(path)
            symbolizer.set('file', path)
            symbolizer.set('type', 'png')
            
            # if no width/height have been provided, set them
            if not (symbolizer.get('width', False) and symbolizer.get('height', False)):
                symbolizer.set('width', str(img.size[0]))
                symbolizer.set('height', str(img.size[1]))
            
            rule = make_ranged_rule_element(range)
            rule.append(symbolizer)
            rules.append(rule)

    if rules:
        style = Element('Style', {'name': 'pattern style %d' % next_counter()})
        style.text = '\n        '
        
        for rule in rules:
            style.append(rule)
        
        insert_layer_style(map, layer, style)

def get_applicable_declarations(element, declarations):
    """ Given an XML element and a list of declarations, return the ones
        that match as a list of (property, value, selector) tuples.
    """
    element_tag = element.tag
    element_id = element.get('id', None)
    element_classes = element.get('class', '').split()

    return [dec for dec in declarations
            if dec.selector.matches(element_tag, element_id, element_classes)]

def compile_stylesheet(src, out=None):
    """
    """
    doc = xml.etree.ElementTree.parse(urllib.urlopen(src))
    map = doc.getroot()
    
    declarations = extract_declarations(map, src)
    
    add_map_style(map, get_applicable_declarations(map, declarations))

    for layer in map.findall('Layer'):
        declarations = get_applicable_declarations(layer, declarations)
        
        #pprint.PrettyPrinter().pprint(declarations)
        
        add_polygon_style(map, layer, declarations)
        add_pattern_style(map, layer, declarations, out)
        add_line_style(map, layer, declarations)
        add_text_styles(map, layer, declarations)
        add_point_style(map, layer, declarations, out)
        
        layer.set('name', 'layer %d' % next_counter())
        
        if 'id' in layer.attrib:
            del layer.attrib['id']
    
        if 'class' in layer.attrib:
            del layer.attrib['class']
    
        if declarations:
            layer.set('status', 'on')
        else:
            layer.set('status', 'off')

    out = StringIO.StringIO()
    doc.write(out)
    
    return out.getvalue()

if __name__ == '__main__':

    print compile_stylesheet('example.mml')
