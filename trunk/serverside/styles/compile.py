import os, sys
import math
import pprint
import urllib
import urlparse
import tempfile
import StringIO
import optparse
from operator import lt, le, eq, ge, gt
import xml.etree.ElementTree
from xml.etree.ElementTree import Element
import style
import PIL.Image

def main(file, dir):
    """ Given an input layers file and a directory, print the compiled
        XML file to stdout and save any encountered external image files
        to the named directory.
    """
    print compile(file, dir)
    return 0

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
        if self.leftedge and self.rightedge and self.leftedge > self.rightedge:
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

class Filter:
    """
    """
    def __init__(self, *tests):
        self.tests = list(tests)

    def isOpen(self):
        """
        """
        equals = {}
        
        for test in self.tests:
            if test.op == '=':
                if equals.has_key(test.arg1) and test.arg2 != equals[test.arg1]:
                    # a contradiction!
                    return False
                    
                equals[test.arg1] = test.arg2
        
        return True

    def clone(self):
        """
        """
        return Filter(*self.tests[:])
    
    def minusExtras(self):
        """ Return a new Filter that's equal to this one,
            without extra terms that don't add meaning.
        """
        assert self.isOpen()
        
        trimmed = self.clone()
        
        equals = {}
        
        for test in trimmed.tests:
            if test.op == '=':
                equals[test.arg1] = test.arg2

        extras = []

        for (i, test) in enumerate(trimmed.tests):
            if test.op == '!=' and equals.has_key(test.arg1) and equals[test.arg1] != test.arg2:
                extras.append(i)

        while extras:
            trimmed.tests.pop(extras.pop())

        return trimmed

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

def selectors_filters(selectors):
    """ Given a list of selectors and a map, return a list of Filters that
        fully describes all possible unique equality tests within those selectors.
    """
    tests = {}
    arg1s = set()
    
    # get all the tests and test.arg1 values out of the selectors
    for selector in selectors:
        for test in selector.allTests():
            if test.isSimple():
                tests[str(test)] = test
                arg1s.add(test.arg1)

    tests = tests.values()
    filters = []
    
    # create something like a truth table
    for i in range(int(math.pow(2, len(tests)))):
        filter = Filter()
    
        for (j, test) in enumerate(tests):
            if bool(i & (0x01 << j)):
                filter.tests.append(test)
            else:
                filter.tests.append(test.inverse())

        if filter.isOpen():
            filters.append(filter.minusExtras())

    if len(filters):
        return filters

    # if no filters have been defined, return a blank one that matches anything
    return [Filter()]

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
            
        rulesets = style.parse_stylesheet(styles, base=local_base, is_gym=is_gym_projection(map))
        declarations += style.unroll_rulesets(rulesets)

    return declarations

def make_rule_element(range, filter):
    """ Given a Range, return a Rule element prepopulated
        with applicable min/max scale denominator elements.
    """
    rule_element = Element('Rule')

    if range.leftedge:
        minscale = Element('MinScaleDenominator')
        rule_element.append(minscale)
    
        if range.leftop is ge:
            minscale.text = str(range.leftedge)
        elif range.leftop is gt:
            minscale.text = str(range.leftedge + 1)
    
    if range.rightedge:
        maxscale = Element('MaxScaleDenominator')
        rule_element.append(maxscale)
    
        if range.rightop is le:
            maxscale.text = str(range.rightedge)
        elif range.rightop is lt:
            maxscale.text = str(range.rightedge - 1)
    
    filter_text = ' and '.join("[%s] %s '%s'" % (test.arg1, test.op, test.arg2) for test in filter.tests)
    
    if filter_text:
        filter_element = Element('Filter')
        filter_element.text = filter_text
        rule_element.append(filter_element)
    
    rule_element.tail = '\n        '
    
    return rule_element

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

def is_applicable_selector(selector, range, filter):
    """
    """
    if not selector.inRange(range.midpoint()) and selector.isRanged():
        return False

    for test in selector.allTests():
        if not test.inFilter(filter.tests):
            return False
    
    return True

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
    
    # a matrix of checks for filter and min/max scale limitations
    ranges = selectors_ranges([dec.selector for dec in declarations])
    filters = selectors_filters([dec.selector for dec in declarations])
    
    for range in ranges:
        for filter in filters:
            has_poly = False
            symbolizer = Element('PolygonSymbolizer')
            encountered = []
            
            # collect all the applicable declarations into a symbolizer element
            for dec in reversed(declarations):
                if is_applicable_selector(dec.selector, range, filter) and dec.property.name not in encountered:
                    parameter = Element('CssParameter', {'name': property_map[dec.property.name]})
                    parameter.text = str(dec.value)
                    symbolizer.append(parameter)
        
                    encountered.append(dec.property.name)
                    has_poly = True
        
            if has_poly:
                rule = make_rule_element(range, filter)
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
    
    # a matrix of checks for filter and min/max scale limitations
    ranges = selectors_ranges([dec.selector for dec in declarations])
    filters = selectors_filters([dec.selector for dec in declarations])
    
    for range in ranges:
        for filter in filters:
            has_line = False
            symbolizer = Element('LineSymbolizer')
            encountered = []
            
            # collect all the applicable declarations into a symbolizer element
            for dec in reversed(declarations):
                if is_applicable_selector(dec.selector, range, filter) and dec.property.name not in encountered:
                    parameter = Element('CssParameter', {'name': property_map[dec.property.name]})
                    parameter.text = str(dec.value)
                    symbolizer.append(parameter)
        
                    encountered.append(dec.property.name)
                    has_line = True

            # TODO: handle outline- properties here, now that we know how wide the line ought to be?
        
            if has_line:
                rule = make_rule_element(range, filter)
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
    
        # just the ones we care about here.
        # the complicated conditional means: get all declarations that
        # apply to this text_name specifically, or text in general.
        name_declarations = [dec for dec in declarations
                             if dec.property.name in property_map
                                and (len(dec.selector.elements) == 1
                                     or (len(dec.selector.elements) == 2
                                         and dec.selector.elements[1].names[0] in (text_name, '*')))]
    
        # a place to put rule elements
        rules = []
        
        # a matrix of checks for filter and min/max scale limitations
        ranges = selectors_ranges([dec.selector for dec in name_declarations])
        filters = selectors_filters([dec.selector for dec in name_declarations])
    
        for range in ranges:
            for filter in filters:
                has_text = False
                symbolizer = Element('TextSymbolizer')
                
                for dec in name_declarations:
                    if is_applicable_selector(dec.selector, range, filter):
                        symbolizer.set(property_map[dec.property.name], str(dec.value))
                        has_text = True
                        
                        # the 'name' attribute will be used as a flag in a few
                        # lines to determine if this symbolizer is worth keeping.
                        if len(dec.selector.elements) == 2 and (len(dec.selector.elements) == 1 or dec.selector.elements[1].names[0] == text_name):
                            symbolizer.set('name', text_name)
                
                if has_text and symbolizer.get('name', False):
                    rule = make_rule_element(range, filter)
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
    
    # a matrix of checks for filter and min/max scale limitations
    ranges = selectors_ranges([dec.selector for dec in declarations])
    filters = selectors_filters([dec.selector for dec in declarations])
    
    for range in ranges:
        for filter in filters:
            symbolizer = Element('PointSymbolizer')
            
            # collect all the applicable declarations into a symbolizer element
            for dec in reversed(declarations):
                if is_applicable_selector(dec.selector, range, filter):
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
                
                rule = make_rule_element(range, filter)
                rule.append(symbolizer)
                rules.append(rule)

    if rules:
        style = Element('Style', {'name': 'point style %d' % next_counter()})
        style.text = '\n        '
        
        for rule in rules:
            style.append(rule)
        
        insert_layer_style(map, layer, style)

def add_polygon_pattern_style(map, layer, declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a PolygonPatternSymbolizer, add it to Map
        and refer to it in Layer.
        
        Optionally provide an output directory for local copies of image files.
    """
    property_map = {'polygon-pattern-file': 'file', 'polygon-pattern-width': 'width',
                    'polygon-pattern-height': 'height', 'polygon-pattern-type': 'type'}
    
    # just the ones we care about here
    declarations = [dec for dec in declarations if dec.property.name in property_map]

    # a place to put rule elements
    rules = []
    
    # a matrix of checks for filter and min/max scale limitations
    ranges = selectors_ranges([dec.selector for dec in declarations])
    filters = selectors_filters([dec.selector for dec in declarations])
    
    for range in ranges:
        for filter in filters:
            symbolizer = Element('PolygonPatternSymbolizer')
            
            # collect all the applicable declarations into a symbolizer element
            for dec in reversed(declarations):
                if is_applicable_selector(dec.selector, range, filter):
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
                
                rule = make_rule_element(range, filter)
                rule.append(symbolizer)
                rules.append(rule)

    if rules:
        style = Element('Style', {'name': 'pattern style %d' % next_counter()})
        style.text = '\n        '
        
        for rule in rules:
            style.append(rule)
        
        insert_layer_style(map, layer, style)

def add_line_pattern_style(map, layer, declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a LinePatternSymbolizer, add it to Map
        and refer to it in Layer.
        
        Optionally provide an output directory for local copies of image files.
    """
    property_map = {'line-pattern-file': 'file', 'line-pattern-width': 'width',
                    'line-pattern-height': 'height', 'line-pattern-type': 'type'}
    
    # just the ones we care about here
    declarations = [dec for dec in declarations if dec.property.name in property_map]

    # a place to put rule elements
    rules = []
    
    # a matrix of checks for filter and min/max scale limitations
    ranges = selectors_ranges([dec.selector for dec in declarations])
    filters = selectors_filters([dec.selector for dec in declarations])
    
    for range in ranges:
        for filter in filters:
            symbolizer = Element('LinePatternSymbolizer')
            
            # collect all the applicable declarations into a symbolizer element
            for dec in reversed(declarations):
                if is_applicable_selector(dec.selector, range, filter):
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
                
                rule = make_rule_element(range, filter)
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

def compile(src, dir=None):
    """
    """
    doc = xml.etree.ElementTree.parse(urllib.urlopen(src))
    map = doc.getroot()
    
    declarations = extract_declarations(map, src)
    
    add_map_style(map, get_applicable_declarations(map, declarations))

    for layer in map.findall('Layer'):
        layer_declarations = get_applicable_declarations(layer, declarations)
        
        #pprint.PrettyPrinter().pprint(layer_declarations)
        
        add_polygon_style(map, layer, layer_declarations)
        add_polygon_pattern_style(map, layer, layer_declarations, dir)
        add_line_style(map, layer, layer_declarations)
        add_line_pattern_style(map, layer, layer_declarations, dir)
        add_text_styles(map, layer, layer_declarations)
        add_point_style(map, layer, layer_declarations, dir)
        
        layer.set('name', 'layer %d' % next_counter())
        
        if 'id' in layer.attrib:
            del layer.attrib['id']
    
        if 'class' in layer.attrib:
            del layer.attrib['class']
    
        if layer_declarations:
            layer.set('status', 'on')
        else:
            layer.set('status', 'off')

    out = StringIO.StringIO()
    doc.write(out)
    
    return out.getvalue()

parser = optparse.OptionParser(usage="""compile.py [options]

Example map of San Francisco and Oakland:
    python compose.py -o out.png -p MICROSOFT_ROAD -d 800 800 -c 37.8 -122.3 11

Map provider and output image dimensions MUST be specified before extent
or center/zoom. Multiple extents and center/zooms may be specified, but
only the last will be used.""")

parser.add_option('-d', '--dir', dest='directory',
                  help='Write to output directory')

if __name__ == '__main__':

    (options, args) = parser.parse_args()
    
    layersfile = args[0]

    sys.exit(main(layersfile, options.directory))
