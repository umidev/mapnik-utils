import sys
import pprint
import urllib
import urlparse
from operator import lt, le, eq, ge, gt
import StringIO
import xml.etree.ElementTree
from xml.etree.ElementTree import Element
import cascade

counter = 0

opsort = {lt: 1, le: 2, eq: 3, ge: 4, gt: 5}
opstr = {lt: '<', le: '<=', eq: '==', ge: '>=', gt: '>'}
    
class Range:
    """ Represents a range for use in min/max scale denominator. Ranges can have
        a left side, a right side, or both, with sides specified as inclusive
        or exclusive.
    """
    def __init__(self, leftop=None, leftarg=None, rightop=None, rightarg=None):
        self.leftop = leftop
        self.leftarg = leftarg
        self.rightop = rightop
        self.rightarg = rightarg

    def midpoint(self):
        """ Return a point guranteed to fall within this range, hopefully near the middle.
        """
        minpoint = self.leftarg

        if self.leftop is gt:
            minpoint += 1
    
        maxpoint = self.rightarg

        if self.rightop is lt:
            maxpoint -= 1

        if minpoint is None:
            return maxpoint
            
        elif maxpoint is None:
            return minpoint
            
        else:
            return (minpoint + maxpoint) / 2
    
    def __repr__(self):
        """
        """
        if self.leftarg == self.rightarg and self.leftop is ge and self.rightop is le:
            # equivalent to ==
            return '(=%s)' % self.leftarg
    
        try:
            return '(%s%s ... %s%s)' % (self.leftarg, opstr[self.leftop], opstr[self.rightop], self.rightarg)
        except KeyError:
            try:
                return '(... %s%s)' % (opstr[self.rightop], self.rightarg)
            except KeyError:
                return '(%s%s ...)' % (self.leftarg, opstr[self.leftop])

def selectors_ranges(selectors):
    """
    """
    # pprint.PrettyPrinter().pprint(selectors)
    
    repeated_breaks = []
    
    # start by getting all the range edges from the selectors into a list of break points
    for selector in selectors:
        for test in selector.rangeTests():
            repeated_breaks.append(test.rangeOpEdge())

    repeated_breaks.sort(key=lambda (o, e): (e, opsort[o]))
    
    # print repeated_breaks
    
    breaks = []

    # next remove repetitions from the list
    for (i, (op, edge)) in enumerate(repeated_breaks):
        if i > 0:
            if op is repeated_breaks[i - 1][0] and edge == repeated_breaks[i - 1][1]:
                continue

        breaks.append(repeated_breaks[i])

    # print breaks
    
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

        else:
            # get a left-boundary based on the previous right-boundary
            if ranges[-1].rightop is lt:
                ranges.append(Range(ge, ranges[-1].rightarg))
            else:
                ranges.append(Range(gt, ranges[-1].rightarg))

            # get a right-boundary for the current range
            if op in (lt, le):
                ranges[-1].rightop, ranges[-1].rightarg = op, edge
            elif op in (eq, ge):
                ranges[-1].rightop, ranges[-1].rightarg = lt, edge
            elif op is gt:
                ranges[-1].rightop, ranges[-1].rightarg = le, edge

            # equals is a special case
            if op is eq:
                if ranges[-1].leftarg == edge:
                    ranges.pop()
            
                ranges.append(Range(ge, edge, le, edge))
            
        if i == len(breaks) - 1:
            # get a left-boundary for the last range
            if op is lt:
                ranges.append(Range(ge, edge))
            else:
                ranges.append(Range(gt, edge))

    # print ranges
    
    if ranges:
        return ranges

    else:
        return [Range()]

def next_counter():
    global counter
    counter += 1
    return counter

def is_gym_projection(map):
    """ Return true if the map projection matches that used by VEarth, Google, OSM, etc.
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

def extract_rules(map, base):
    """ Given a Map element and a URL base string, remove and return a complete
        list of style declarations from any Stylesheet elements found within.
    """
    rules = []
    
    for stylesheet in map.findall('Stylesheet'):
        map.remove(stylesheet)
    
        if 'src' in stylesheet.attrib:
            url = urlparse.urljoin(base, stylesheet.attrib['src'])
            styles = urllib.urlopen(url).read()

        elif stylesheet.text:
            styles = stylesheet.text

        else:
            continue
            
        rulesets = cascade.parse_stylesheet(styles)
        rules += cascade.unroll_rulesets(rulesets)

    return rules

def make_ranged_rule_element(range):
    """
    """
    rule = Element('Rule')
    
    if range.leftarg:
        minscale = Element('MinScaleDenominator')
        rule.append(minscale)
    
        if range.leftop is ge:
            minscale.text = str(range.leftarg)
        elif range.leftop is gt:
            minscale.text = str(range.leftarg + 1)
    
    if range.rightarg:
        maxscale = Element('MaxScaleDenominator')
        rule.append(maxscale)
    
        if range.rightop is le:
            maxscale.text = str(range.rightarg)
        elif range.rightop is lt:
            maxscale.text = str(range.rightarg - 1)
    
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
    #layer.append(stylename)

def add_map_style(map, declarations):
    """
    """
    property_map = {'map-bgcolor': 'bgcolor'}
    
    for (property, value, selector) in declarations:
        if property.name in property_map:
            map.set(property_map[property.name], str(value))

def add_polygon_style(map, layer, declarations):
    """ Given a Map element, a Layer element, and a list of declarations
        consisting of (property, value, selector) tuples, create a new Style element
        with a PolygonSymbolizer, add it to Map and refer to it in Layer.
    """
    property_map = {'polygon-fill': 'fill', 'polygon-opacity': 'fill-opacity'}
    
    # just the ones we care about here
    declarations = [(p, v, s) for (p, v, s) in declarations if p.name in property_map]

    rules = []
    ranges = selectors_ranges([s for (p, v, s) in declarations])
    
    for range in ranges:
        has_poly = False
        symbolizer = Element('PolygonSymbolizer')
        encountered = []
        
        # collect all the applicable declarations into a symbolizer element
        for (property, value, selector) in reversed(declarations):
            if selector.inRange(range.midpoint()) and property.name not in encountered:
                parameter = Element('CssParameter', {'name': property_map[property.name]})
                parameter.text = str(value)
                symbolizer.append(parameter)
    
                encountered.append(property.name)
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
    """ Given a Map element, a Layer element, and a list of declarations
        consisting of (property, value, selector) tuples, create a new Style element
        with a LineSymbolizer, add it to Map and refer to it in Layer.
    """
    property_map = {'line-color': 'stroke', 'line-width': 'stroke-width',
                    'line-opacity': 'stroke-opacity', 'line-join': 'stroke-linejoin',
                    'line-cap': 'stroke-linecap', 'line-dasharray': 'stroke-dasharray'}
    
    # just the ones we care about here
    declarations = [(p, v, s) for (p, v, s) in declarations if p.name in property_map]

    rules = []
    ranges = selectors_ranges([s for (p, v, s) in declarations])
    
    for range in ranges:
        has_line = False
        symbolizer = Element('LineSymbolizer')
        encountered = []
        
        # collect all the applicable declarations into a symbolizer element
        for (property, value, selector) in reversed(declarations):
            if selector.inRange(range.midpoint()) and property.name not in encountered:
                parameter = Element('CssParameter', {'name': property_map[property.name]})
                parameter.text = str(value)
                symbolizer.append(parameter)
    
                encountered.append(property.name)
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
    """ Given a Map element, a Layer element, and a list of declarations
        consisting of (property, value, selector) tuples, create new Style elements
        with a TextSymbolizer, add them to Map and refer to them in Layer.
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

    text_names = {}
    
    declarations = [(p, v, s) for (p, v, s) in declarations if p.name in property_map]
    
    # first, break up the text declarations among different names (see <TextSymbolizer name=""/>)
    for (property, value, selector) in declarations:
        if len(selector.elements) is 2 and len(selector.elements[1].names) is 1:
            text_name = selector.elements[1].names[0]

            if not text_names.has_key(text_name):
                text_names[text_name] = {}

            text_names[text_name][property.name] = value
            has_text = True

    # make as many styles as are necessary
    if has_text:
        for text_name in text_names:
            symbolizer = Element('TextSymbolizer', {'name': text_name})
        
            for property_name in text_names[text_name]:
                symbolizer.set(property_map[property_name], str(text_names[text_name][property_name]))

            rule = Element('Rule')
            rule.append(symbolizer)
            style = Element('Style', {'name': 'text style %d' % next_counter()})
            style.append(rule)

            insert_layer_style(map, layer, style)

def get_applicable_declaration(element, rules):
    """ Given an XML element and a list of rules, return the ones
        that match as a list of (property, value, selector) tuples.
    """
    element_tag = element.tag
    element_id = element.get('id', None)
    element_classes = element.get('class', '').split()

    return [(rule['property'], rule['value'], rule['selector'])
            for rule in rules
            if rule['selector'].matches(element_tag, element_id, element_classes)]

def compile_stylesheet(src):
    """
    """
    doc = xml.etree.ElementTree.parse(urllib.urlopen(src))
    map = doc.getroot()
    
    rules = extract_rules(map, src)
    
    add_map_style(map, get_applicable_declaration(map, rules))

    layers = []
    
    for layer in map.findall('Layer'):
        declarations = get_applicable_declaration(layer, rules)
        
        #pprint.PrettyPrinter().pprint(declarations)
        
        add_polygon_style(map, layer, declarations)
        add_line_style(map, layer, declarations)
        add_text_styles(map, layer, declarations)
        
        layer.set('name', 'layer %d' % next_counter())
        
        if 'id' in layer.attrib:
            del layer.attrib['id']
    
        if 'class' in layer.attrib:
            del layer.attrib['class']
    
        if declarations:
            layer.set('status', 'on')
            layers.append({'layer': layer, 'rules': declarations})
        else:
            layer.set('status', 'off')

    out = StringIO.StringIO()
    doc.write(out)
    
    return out.getvalue()

if __name__ == '__main__':

    print compile_stylesheet('example.mml')
