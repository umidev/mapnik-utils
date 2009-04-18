import os, sys
import math
import pprint
import urllib
import urlparse
import tempfile
import StringIO
import operator
from operator import lt, le, eq, ge, gt
import PIL.Image
import os.path
import zipfile

import style, output

try:
    import xml.etree.ElementTree as ElementTree
    from xml.etree.ElementTree import Element
except ImportError:
    import elementtree.ElementTree as ElementTree
    from elementtree.ElementTree import Element

opsort = {lt: 1, le: 2, eq: 3, ge: 4, gt: 5}
opstr = {lt: '<', le: '<=', eq: '==', ge: '>=', gt: '>'}
    
counter = 0

def next_counter():
    global counter
    counter += 1
    return counter

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
    
    def toFilter(self, property):
        """ Convert this range to a Filter with a tests having a given property.
        """
        if self.leftedge == self.rightedge and self.leftop is ge and self.rightop is le:
            # equivalent to ==
            return Filter(style.SelectorAttributeTest(property, '=', self.leftedge))
    
        try:
            return Filter(style.SelectorAttributeTest(property, opstr[self.leftop], self.leftedge),
                          style.SelectorAttributeTest(property, opstr[self.rightop], self.rightedge))
        except KeyError:
            try:
                return Filter(style.SelectorAttributeTest(property, opstr[self.rightop], self.rightedge))
            except KeyError:
                try:
                    return Filter(style.SelectorAttributeTest(property, opstr[self.leftop], self.leftedge))
                except KeyError:
                    return Filter()
    
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
                try:
                    return '(%s%s ...)' % (self.leftedge, opstr[self.leftop])
                except KeyError:
                    return '(...)'

class Filter:
    """ Represents a filter of some sort for use in stylesheet rules.
    
        Composed of a list of tests.
    """
    def __init__(self, *tests):
        self.tests = list(tests)

    def isOpen(self):
        """ Return true if this filter is not trivially false, i.e. self-contradictory.
        """
        equals = {}
        nequals = {}
        
        for test in self.tests:
            if test.op == '=':
                if equals.has_key(test.property) and test.value != equals[test.property]:
                    # we've already stated that this arg must equal something else
                    return False
                    
                if nequals.has_key(test.property) and test.value in nequals[test.property]:
                    # we've already stated that this arg must not equal its current value
                    return False
                    
                equals[test.property] = test.value
        
            if test.op == '!=':
                if equals.has_key(test.property) and test.value == equals[test.property]:
                    # we've already stated that this arg must equal its current value
                    return False
                    
                if not nequals.has_key(test.property):
                    nequals[test.property] = set()

                nequals[test.property].add(test.value)
        
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
                equals[test.property] = test.value

        extras = []

        for (i, test) in enumerate(trimmed.tests):
            if test.op == '!=' and equals.has_key(test.property) and equals[test.property] != test.value:
                extras.append(i)

        while extras:
            trimmed.tests.pop(extras.pop())

        return trimmed
    
    def __repr__(self):
        """
        """
        return ''.join(map(repr, sorted(self.tests)))
    
    def __cmp__(self, other):
        """
        """
        # get the scale tests to the front of the line, followed by regular alphabetical
        key_func = lambda t: (not t.isMapScaled(), t.property, t.op, t.value)

        # extract tests into cleanly-sortable tuples
        self_tuples = [(t.property, t.op, t.value) for t in sorted(self.tests, key=key_func)]
        other_tuples = [(t.property, t.op, t.value) for t in sorted(other.tests, key=key_func)]
        
        return cmp(self_tuples, other_tuples)

def test_ranges(tests):
    """ Given a list of tests, return a list of Ranges that fully describes
        all possible unique ranged slices within those tests.
        
        This function was hard to write, it should be hard to read.
        
        TODO: make this work for <= following by >= in breaks
    """
    if len(tests) == 0:
        return [Range()]
    
    assert 1 == len(set(test.property for test in tests)), 'All tests must share the same property'
    assert True in [test.isRanged() for test in tests], 'At least one test must be ranged'
    assert False not in [test.isNumeric() for test in tests], 'All tests must be numeric'
    
    repeated_breaks = []
    
    # start by getting all the range edges from the selectors into a list of break points
    for test in tests:
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
            elif op is ge:
                ranges.append(Range(None, None, lt, edge))
            elif op is gt:
                ranges.append(Range(None, None, le, edge))
            elif op is eq:
                # edge case
                ranges.append(Range(None, None, lt, edge))
                ranges.append(Range(ge, edge, le, edge))

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

def test_combinations(tests, filter=None):
    """ Given a list of simple =/!= tests, return a list of possible combinations.
    
        The filter argument is used to call test_combinations() recursively;
        this cuts down on the potential tests^2 number of combinations by
        identifying closed filters early and culling them from consideration.
    """
    # is the first one simple? it should be
    if len(tests) >= 1:
        assert tests[0].isSimple(), 'All tests must be simple, i.e. = or !='
    
    # does it share a property with the next one? it should
    if len(tests) >= 2:
        assert tests[0].property == tests[1].property, 'All tests must share the same property'

    # -------- remaining tests will be checked in subsequent calls --------
    
    # bail early
    if len(tests) == 0:
        return []

    # base case where no filter has been passed
    if filter is None:
        filter = Filter()

    # knock one off the front
    first_test, remaining_tests = tests[0], tests[1:]
    
    # one filter with the front test on it
    this_filter = filter.clone()
    this_filter.tests.append(first_test)
    
    # another filter with the inverse of the front test on it
    that_filter = filter.clone()
    that_filter.tests.append(first_test.inverse())
    
    # return value
    test_sets = []
    
    for new_filter in (this_filter, that_filter):
        if new_filter.isOpen():
            if len(remaining_tests) > 0:
                # keep diving deeper
                test_sets += test_combinations(remaining_tests, new_filter)
            
            else:
                # only append once the list has been exhausted
                new_set = []
                
                for test in new_filter.minusExtras().tests:
                    if test not in new_set:
                        new_set.append(test)
    
                test_sets.append(new_set)

    return test_sets

def xindexes(slots):
    """ Generate list of possible indexes into a list of slots.
    
        Best way to think of this is as a number where each digit might have a different radix.
        E.g.: (10, 10, 10) would return 10 x 10 x 10 = 1000 responses from (0, 0, 0) to (9, 9, 9),
        (2, 2, 2, 2) would return 2 x 2 x 2 x 2 = 16 responses from (0, 0, 0, 0) to (1, 1, 1, 1).
    """
    # the first response...
    slot = [0] * len(slots)
    
    for i in range(reduce(operator.mul, slots)):
        yield slot
        
        carry = 1
        
        # iterate from the least to the most significant digit
        for j in range(len(slots), 0, -1):
            k = j - 1
            
            slot[k] += carry
            
            if slot[k] >= slots[k]:
                carry = 1 + slot[k] - slots[k]
                slot[k] = 0
            else:
                carry = 0

def selectors_tests(selectors, property=None):
    """ Given a list of selectors, return a list of unique tests.
    
        Optionally limit to those with a given property.
    """
    tests = {}
    
    for selector in selectors:
        for test in selector.allTests():
            if property is None or test.property == property:
                tests[str(test)] = test

    return tests.values()

def tests_filter_combinations(tests):
    """ Return a complete list of filter combinations for given list of tests
    """
    if len(tests) == 0:
        return [Filter()]
    
    # unique properties
    properties = sorted(list(set([test.property for test in tests])))

    property_tests = {}
    
    # divide up the tests by their first argument, e.g. "landuse" vs. "tourism",
    # into lists of all possible legal combinations of those tests.
    for property in properties:
        
        # limit tests to those with the current property
        current_tests = [test for test in tests if test.property == property]
        
        has_ranged_tests = True in [test.isRanged() for test in current_tests]
        has_nonnumeric_tests = False in [test.isNumeric() for test in current_tests]
        
        if has_ranged_tests and has_nonnumeric_tests:
            raise Exception('Mixed ranged/non-numeric tests in %s' % str(current_tests))

        elif has_ranged_tests:
            property_tests[property] = [range.toFilter(property).tests for range in test_ranges(current_tests)]

        else:
            property_tests[property] = test_combinations(current_tests)
            
    # get a list of the number of combinations for each group of tests from above.
    property_counts = [len(property_tests[property]) for property in properties]
    
    filters = []
        
    # now iterate over each combination - for large numbers of tests, this can get big really, really fast
    for property_indexes in xindexes(property_counts):
        # list of lists of tests
        testslist = [property_tests[properties[i]][j] for (i, j) in enumerate(property_indexes)]
        
        # corresponding filter
        filter = Filter(*reduce(operator.add, testslist))
        
        filters.append(filter)

    if len(filters):
        return sorted(filters)

    # if no filters have been defined, return a blank one that matches anything
    return [Filter()]

def is_gym_projection(map_el):
    """ Return true if the map projection matches that used by VEarth, Google, OSM, etc.
    
        Will be useful for a zoom-level shorthand for scale-denominator.
    """ 
    # expected
    gym = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null'
    gym = dict([p.split('=') for p in gym.split() if '=' in p])
    
    # observed
    srs = map_el.get('srs', '')
    srs = dict([p.split('=') for p in srs.split() if '=' in p])
    
    for p in gym:
        if srs.get(p, None) != gym.get(p, None):
            return False

    return True

def extract_declarations(map_el, base):
    """ Given a Map element and a URL base string, remove and return a complete
        list of style declarations from any Stylesheet elements found within.
    """
    declarations = []
    
    for stylesheet in map_el.findall('Stylesheet'):
        map_el.remove(stylesheet)
    
        if 'src' in stylesheet.attrib:
            url = urlparse.urljoin(base, stylesheet.attrib['src'])
            styles, local_base = urllib.urlopen(url).read(), url

        elif stylesheet.text:
            styles, local_base = stylesheet.text, base

        else:
            continue
            
        rulesets = style.stylesheet_rulesets(styles, base=local_base, is_gym=is_gym_projection(map_el))
        declarations += style.rulesets_declarations(rulesets)

    return declarations

def test2str(test):
    """ Return a mapnik-happy Filter expression atom for a single test
    """
    if type(test.value) in (int, float):
        value = str(test.value)
    elif type(test.value) is str:
        value = "'%s'" % test.value
    else:
        raise Exception("test2str doesn't know what to do with a %s" % type(test.value))
    
    if test.op == '!=':
        return "not [%s] = %s" % (test.property, value)
    elif test.op in ('<', '<=', '=', '>=', '>'):
        return "[%s] %s %s" % (test.property, test.op, value)
    else:
        raise Exception('"%s" is not a valid filter operation' % test.op)

def make_rule_element(filter, *symbolizer_els):
    """ Given a Filter, return a Rule element prepopulated with
        applicable min/max scale denominator and filter elements.
    """
    rule_el = Element('Rule')
    
    scale_tests = [test for test in filter.tests if test.isMapScaled()]
    other_tests = [test for test in filter.tests if not test.isMapScaled()]
    
    for scale_test in scale_tests:

        if scale_test.op in ('>', '>='):
            minscale = Element('MinScaleDenominator')
            rule_el.append(minscale)
        
            if scale_test.op == '>=':
                minscale.text = str(scale_test.value)
            elif scale_test.op == '>':
                minscale.text = str(scale_test.value + 1)

        if scale_test.op in ('<', '<='):
            maxscale = Element('MaxScaleDenominator')
            rule_el.append(maxscale)
        
            if scale_test.op == '<=':
                maxscale.text = str(scale_test.value)
            elif scale_test.op == '<':
                maxscale.text = str(scale_test.value - 1)
    
    filter_text = ' and '.join(test2str(test) for test in other_tests)
    
    if filter_text:
        filter_el = Element('Filter')
        filter_el.text = filter_text
        rule_el.append(filter_el)
    
    rule_el.tail = '\n        '
    
    for symbolizer_el in symbolizer_els:
        if symbolizer_el != False:
            rule_el.append(symbolizer_el)
    
    return rule_el

def new_make_rule_element(filter, *symbolizers):
    """ Given a Filter, return a Rule element prepopulated with
        applicable min/max scale denominator and filter elements.
    """
    scale_tests = [test for test in filter.tests if test.isMapScaled()]
    other_tests = [test for test in filter.tests if not test.isMapScaled()]
    
    # these will be replaced with values as necessary
    minscale, maxscale, filter = None, None, None
    
    for scale_test in scale_tests:

        if scale_test.op in ('>', '>='):
            if scale_test.op == '>=':
                value = scale_test.value
            elif scale_test.op == '>':
                value = scale_test.value + 1

            minscale = output.MinScaleDenominator(value)

        if scale_test.op in ('<', '<='):
            if scale_test.op == '<=':
                value = scale_test.value
            elif scale_test.op == '<':
                value = scale_test.value - 1

            maxscale = output.MaxScaleDenominator(value)
    
    filter_text = ' and '.join(test2str(test) for test in other_tests)
    
    if filter_text:
        filter = output.Filter(filter_text)

    rule = output.Rule(minscale, maxscale, filter, *[s for s in symbolizers if s])
    
    return rule

def insert_layer_style(map_el, layer_el, style_name, rule_els):
    """ Given a Map element, a Layer element, a style name and a list of Rule
        elements, create a new Style element and insert it into the flow and
        point to it from the Layer element.
    """
    if not rule_els:
        return
    
    style_el = Element('Style', {'name': style_name})
    style_el.text = '\n        '
    
    for rule_el in rule_els:
        style_el.append(rule_el)
    
    style_el.tail = '\n    '
    map_el.insert(map_el._children.index(layer_el), style_el)
    
    stylename_el = Element('StyleName')
    stylename_el.text = style_name
    stylename_el.tail = '\n        '

    layer_el.insert(layer_el._children.index(layer_el.find('Datasource')), stylename_el)
    layer_el.set('status', 'on')

def is_applicable_selector(selector, filter):
    """ Given a Selector and Filter, return True if the Selector is
        compatible with the given Filter, and False if they contradict.
    """
    for test in selector.allTests():
        if not test.isCompatible(filter.tests):
            return False
    
    return True

def add_map_style(map_el, declarations):
    """
    """
    property_map = {'map-bgcolor': 'bgcolor'}
    
    for dec in declarations:
        if dec.property.name in property_map:
            map_el.set(property_map[dec.property.name], str(dec.value))

def filtered_property_declarations(declarations, property_names):
    """
    """
    # just the ones we care about here
    declarations = [dec for dec in declarations if dec.property.name in property_names]
    selectors = [dec.selector for dec in declarations]

    # a place to put rules
    rules = []
    
    for filter in tests_filter_combinations(selectors_tests(selectors)):
        rule = (filter, {})
        
        # collect all the applicable declarations into a list of parameters and values
        for dec in declarations:
            if is_applicable_selector(dec.selector, filter):
                rule[1][dec.property.name] = dec.value

        if rule[1]:
            rules.append(rule)

    return rules

def get_polygon_rules(declarations):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a PolygonSymbolizer, add it to Map
        and refer to it in Layer.
    """
    property_map = {'polygon-fill': 'fill', 'polygon-opacity': 'fill-opacity'}
    
    property_names = property_map.keys()
    
    # a place to put rules
    rules = []
    
    for (filter, values) in filtered_property_declarations(declarations, property_names):

        color = values.has_key('polygon-fill') and values['polygon-fill'].value
        opacity = values.has_key('polygon-opacity') and values['polygon-opacity'].value or None
        symbolizer = color and output.PolygonSymbolizer(color, opacity)
        
        if symbolizer:
            rules.append(new_make_rule_element(filter, symbolizer))
    
    return rules

def get_line_rules(declarations):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a LineSymbolizer, add it to Map
        and refer to it in Layer.
        
        This function is wise to both line-<foo> and outline-<foo> properties,
        and will generate pairs of LineSymbolizers if necessary.
    """
    property_map = {'line-color': 'stroke', 'line-width': 'stroke-width',
                    'line-opacity': 'stroke-opacity', 'line-join': 'stroke-linejoin',
                    'line-cap': 'stroke-linecap', 'line-dasharray': 'stroke-dasharray'}

    property_names = property_map.keys()
    
    # prepend parameter names with 'in' and 'out'
    for i in range(len(property_names)):
        property_names.append('in' + property_names[i])
        property_names.append('out' + property_names[i])

    # a place to put rules
    rules = []
    
    for (filter, values) in filtered_property_declarations(declarations, property_names):
    
        width = values.has_key('line-width') and values['line-width'].value
        color = values.has_key('line-color') and values['line-color'].value

        opacity = values.has_key('line-opacity') and values['line-opacity'].value or None
        join = values.has_key('line-join') and values['line-join'].value or None
        cap = values.has_key('line-cap') and values['line-cap'].value or None
        dashes = values.has_key('line-dasharray') and values['line-dasharray'].value or None

        line_symbolizer = color and width and output.LineSymbolizer(color, width, opacity, join, cap, dashes) or False

        width = values.has_key('inline-width') and values['inline-width'].value
        color = values.has_key('inline-color') and values['inline-color'].value

        opacity = values.has_key('inline-opacity') and values['inline-opacity'].value or None
        join = values.has_key('inline-join') and values['inline-join'].value or None
        cap = values.has_key('inline-cap') and values['inline-cap'].value or None
        dashes = values.has_key('inline-dasharray') and values['inline-dasharray'].value or None

        inline_symbolizer = color and width and output.LineSymbolizer(color, width, opacity, join, cap, dashes) or False

        # outline requires regular line to have a meaningful width
        width = values.has_key('outline-width') and values.has_key('line-width') \
            and values['line-width'].value + values['outline-width'].value * 2
        color = values.has_key('outline-color') and values['outline-color'].value

        opacity = values.has_key('outline-opacity') and values['outline-opacity'].value or None
        join = values.has_key('outline-join') and values['outline-join'].value or None
        cap = values.has_key('outline-cap') and values['outline-cap'].value or None
        dashes = values.has_key('outline-dasharray') and values['outline-dasharray'].value or None

        outline_symbolizer = color and width and output.LineSymbolizer(color, width, opacity, join, cap, dashes) or False
        
        if outline_symbolizer or line_symbolizer or inline_symbolizer:
            rules.append(new_make_rule_element(filter, outline_symbolizer, line_symbolizer, inline_symbolizer))

    return rules

def get_text_rule_groups(declarations):
    """ Given a Map element, a Layer element, and a list of declarations,
        create new Style elements with a TextSymbolizer, add them to Map
        and refer to them in Layer.
    """
    property_map = {'text-face-name': 'face_name', 'text-size': 'size', 
                    'text-ratio': 'text_ratio', 'text-wrap-width': 'wrap_width', 'text-spacing': 'spacing',
                    'text-label-position-tolerance': 'label_position_tolerance',
                    'text-max-char-angle-delta': 'max_char_angle_delta', 'text-fill': 'fill',
                    'text-halo-fill': 'halo_fill', 'text-halo-radius': 'halo_radius',
                    'text-dx': 'dx', 'text-dy': 'dy',
                    'text-avoid-edges': 'avoid_edges', 'text-min-distance': 'min_distance',
                    'text-allow-overlap': 'allow_overlap', 'text-placement': 'placement'}

    property_names = property_map.keys()
    
    # pull out all the names
    text_names = [dec.selector.elements[1].names[0]
                  for dec in declarations
                  if len(dec.selector.elements) is 2 and len(dec.selector.elements[1].names) is 1]
    
    # a place to put groups
    groups = []
    
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
        
        # a place to put rules
        rules = []
        
        text_face_name, text_size = None, None
        
        for (filter, values) in filtered_property_declarations(declarations, property_names):
            
            face_name = values.has_key('text-face-name') and values['text-face-name'].value
            size = values.has_key('text-size') and values['text-size'].value
            
            color = values.has_key('text-fill') and values['text-fill'].value or None
            ratio = values.has_key('text-ratio') and values['text-ratio'].value or None
            wrap_width = values.has_key('text-wrap-width') and values['text-wrap-width'].value or None
            spacing = values.has_key('text-spacing') and values['text-spacing'].value or None
            label_position_tolerance = values.has_key('text-label-position-tolerance') and values['text-label-position-tolerance'].value or None
            max_char_angle_delta = values.has_key('text-max-char-angle-delta') and values['text-max-char-angle-delta'].value or None
            halo_color = values.has_key('text-halo-fill') and values['text-halo-fill'].value or None
            halo_radius = values.has_key('text-halo-radius') and values['text-halo-radius'].value or None
            dx = values.has_key('text-dx') and values['text-dx'].value or None
            dy = values.has_key('text-dy') and values['text-dy'].value or None
            avoid_edges = values.has_key('text-avoid-edges') and values['text-avoid-edges'].value or None
            min_distance = values.has_key('text-min-distance') and values['text-min-distance'].value or None
            allow_overlap = values.has_key('text-allow-overlap') and values['text-allow-overlap'].value or None
            placement = values.has_key('text-placement') and values['text-placement'].value or None
            
            symbolizer = face_name and size and output.TextSymbolizer(face_name, size, \
                color, wrap_width, spacing, label_position_tolerance, max_char_angle_delta, \
                halo_color, halo_radius, dx, dy, avoid_edges, min_distance, allow_overlap, placement)
            
            if symbolizer:
                rules.append(new_make_rule_element(filter, symbolizer))
        
        groups.append((text_name, rules))
    
    return dict(groups)

def postprocess_symbolizer_image_file(file_name, out, temp_name):
    """ Given a file name, an output directory name, and a temporary
        file name, save the file to a temporary location as a PING
        while noting its dimensions.
    """
    # read the image to get some more details
    img_path = file_name
    img_data = urllib.urlopen(img_path).read()
    img_file = StringIO.StringIO(img_data)
    img = PIL.Image.open(img_file)
    
    # save the image to a tempfile, making it a PNG no matter what
    (handle, path) = tempfile.mkstemp(suffix='.png', prefix='cascadenik-%s-' % temp_name, dir=out)
    os.close(handle)
    
    img.save(path)
    os.chmod(path, 0644)
    
    return path, 'png', img.size[0], img.size[1]

def get_shield_rule_groups(declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create new Style elements with a TextSymbolizer, add them to Map
        and refer to them in Layer.
    """
    property_map = {'shield-face-name': 'face_name', 'shield-size': 'size', 
                    'shield-fill': 'fill', 'shield-min-distance': 'min_distance',
                    'shield-file': 'file', 'shield-width': 'width', 'shield-height': 'height' }

    property_names = property_map.keys()
    
    # pull out all the names
    text_names = [dec.selector.elements[1].names[0]
                  for dec in declarations
                  if len(dec.selector.elements) is 2 and len(dec.selector.elements[1].names) is 1]
    
    # a place to put groups
    groups = []
    
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
        
        # a place to put rules
        rules = []
        
        for (filter, values) in filtered_property_declarations(declarations, property_names):
        
            shield_face_name = values.has_key('shield-face-name') and values['shield-face-name'].value or shield_face_name
            shield_size = values.has_key('shield-size') and values['shield-size'].value or shield_size
            
            shield_file, shield_type, shield_width, shield_height \
                = values.has_key('shield-file') \
                and postprocess_symbolizer_image_file(str(values['shield-file'].value), out, 'shield') \
                or (None, None, None, None)
            
            shield_width = values.has_key('shield-width') and values['shield-width'].value or shield_width
            shield_height = values.has_key('shield-height') and values['shield-height'].value or shield_height

            symbolizer = (shield_face_name and shield_size or shield_file) \
                and output.ShieldSymbolizer(shield_face_name, shield_size, shield_file, shield_type, shield_width, shield_height)
            
            if symbolizer:
                rules.append(new_make_rule_element(filter, symbolizer))
        
        groups.append((text_name, rules))
    
    return dict(groups)

def get_point_rules(declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a PointSymbolizer, add it to Map
        and refer to it in Layer.
        
        Optionally provide an output directory for local copies of image files.
    """
    property_map = {'point-file': 'file', 'point-width': 'width',
                    'point-height': 'height', 'point-type': 'type',
                    'point-allow-overlap': 'allow_overlap'}
    
    property_names = property_map.keys()
    
    # a place to put rules
    rules = []
    
    for (filter, values) in filtered_property_declarations(declarations, property_names):
    
        point_file, point_type, point_width, point_height \
            = values.has_key('point-file') \
            and postprocess_symbolizer_image_file(str(values['point-file'].value), out, 'point') \
            or (None, None, None, None)
        
        point_width = values.has_key('point-width') and values['point-width'].value or point_width
        point_height = values.has_key('point-height') and values['point-height'].value or point_height
        point_allow_overlap = values.has_key('point-allow-overlap') and values['point-allow-overlap'].value or None
        
        symbolizer = point_file and output.PointSymbolizer(point_file, point_type, point_width, point_height, point_allow_overlap)

        if symbolizer:
            rules.append(new_make_rule_element(filter, symbolizer))
    
    return rules

def get_polygon_pattern_rules(declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a PolygonPatternSymbolizer, add it to Map
        and refer to it in Layer.
        
        Optionally provide an output directory for local copies of image files.
    """
    property_map = {'polygon-pattern-file': 'file', 'polygon-pattern-width': 'width',
                    'polygon-pattern-height': 'height', 'polygon-pattern-type': 'type'}
    
    property_names = property_map.keys()
    
    # a place to put rules
    rules = []
    
    for (filter, values) in filtered_property_declarations(declarations, property_names):
    
        poly_pattern_file, poly_pattern_type, poly_pattern_width, poly_pattern_height \
            = values.has_key('polygon-pattern-file') \
            and postprocess_symbolizer_image_file(str(values['polygon-pattern-file'].value), out, 'polygon-pattern') \
            or (None, None, None, None)
        
        poly_pattern_width = values.has_key('polygon-pattern-width') and values['polygon-pattern-width'].value or poly_pattern_width
        poly_pattern_height = values.has_key('polygon-pattern-height') and values['polygon-pattern-height'].value or poly_pattern_height
        symbolizer = poly_pattern_file and output.PolygonPatternSymbolizer(poly_pattern_file, poly_pattern_type, poly_pattern_width, poly_pattern_height)
        
        if symbolizer:
            rules.append(new_make_rule_element(filter, symbolizer))
    
    return rules

def get_line_pattern_rules(declarations, out=None):
    """ Given a Map element, a Layer element, and a list of declarations,
        create a new Style element with a LinePatternSymbolizer, add it to Map
        and refer to it in Layer.
        
        Optionally provide an output directory for local copies of image files.
    """
    property_map = {'line-pattern-file': 'file', 'line-pattern-width': 'width',
                    'line-pattern-height': 'height', 'line-pattern-type': 'type'}
    
    property_names = property_map.keys()
    
    # a place to put rules
    rules = []
    
    for (filter, values) in filtered_property_declarations(declarations, property_names):
    
        line_pattern_file, line_pattern_type, line_pattern_width, line_pattern_height \
            = values.has_key('line-pattern-file') \
            and postprocess_symbolizer_image_file(str(values['line-pattern-file'].value), out, 'line-pattern') \
            or (None, None, None, None)
        
        line_pattern_width = values.has_key('line-pattern-width') and values['line-pattern-width'].value or line_pattern_width
        line_pattern_height = values.has_key('line-pattern-height') and values['line-pattern-height'].value or line_pattern_height
        symbolizer = line_pattern_file and output.LinePatternSymbolizer(line_pattern_file, line_pattern_type, line_pattern_width, line_pattern_height)
        
        if symbolizer:
            rules.append(new_make_rule_element(filter, symbolizer))
    
    return rules

def get_applicable_declarations(element, declarations):
    """ Given an XML element and a list of declarations, return the ones
        that match as a list of (property, value, selector) tuples.
    """
    element_tag = element.tag
    element_id = element.get('id', None)
    element_classes = element.get('class', '').split()

    return [dec for dec in declarations
            if dec.selector.matches(element_tag, element_id, element_classes)]

def localize_shapefile(src, shapefile, dir=None):
    """ Given a stylesheet path, a shapefile name, and a temp directory,
        modify the shapefile name so it's an absolute path.
    
        Shapefile is assumed to be relative to the stylesheet path.
        If it's found to look like a URL (e.g. "http://...") it's assumed
        to be a remote zip file containing .shp, .shx, and .dbf files.
    """
    (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(shapefile)
    
    if scheme == '':
        # assumed to be local
        return os.path.realpath(urlparse.urljoin(src, shapefile))

    # assumed to be a remote zip archive with .shp, .shx, and .dbf files
    zip_data = urllib.urlopen(shapefile).read()
    zip_file = zipfile.ZipFile(StringIO.StringIO(zip_data))
    
    infos = zip_file.infolist()
    extensions = [os.path.splitext(info.filename)[1] for info in infos]
    basenames = [os.path.basename(info.filename) for info in infos]
    
    tmp_dir = tempfile.mkdtemp(prefix='cascadenik-shapefile-', dir=dir)
    
    for (expected, required) in (('.shp', True), ('.shx', True), ('.dbf', True), ('.prj', False)):
        if required and expected not in extensions:
            raise Exception('Zip file %(shapefile)s missing extension "%(expected)s"' % locals())

        for (info, extension, basename) in zip(infos, extensions, basenames):
            if extension == expected:
                file_data = zip_file.read(info.filename)
                file_name = '%(tmp_dir)s/%(basename)s' % locals()
                
                file = open(file_name, 'wb')
                file.write(file_data)
                file.close()
                
                if extension == '.shp':
                    local = file_name[:-4]
                
                break

    return local

def compile(src, dir=None):
    """
    """
    doc = ElementTree.parse(urllib.urlopen(src))
    map = doc.getroot()
    
    declarations = extract_declarations(map, src)
    
    add_map_style(map, get_applicable_declarations(map, declarations))

    for layer in map.findall('Layer'):
    
        for parameter in layer.find('Datasource').findall('Parameter'):
            if parameter.get('name', None) == 'file':
                # make shapefiles local, absolute paths
                parameter.text = localize_shapefile(src, parameter.text, dir)

            elif parameter.get('name', None) == 'table':
                # remove line breaks from possible SQL
                parameter.text = parameter.text.replace('\r', ' ').replace('\n', ' ')

        if layer.get('status') == 'off':
            # don't bother
            continue
    
        # the default...
        layer.set('status', 'off')

        layer_declarations = get_applicable_declarations(layer, declarations)
        
        #pprint.PrettyPrinter().pprint(layer_declarations)
        
        insert_layer_style(map, layer, 'polygon style %d' % next_counter(),
                           get_polygon_rules(layer_declarations) + get_polygon_pattern_rules(layer_declarations, dir))
        
        insert_layer_style(map, layer, 'line style %d' % next_counter(),
                           get_line_rules(layer_declarations) + get_line_pattern_rules(layer_declarations, dir))

        for (shield_name, shield_rule_els) in get_shield_rule_groups(layer_declarations):
            insert_layer_style(map, layer, 'shield style %d (%s)' % (next_counter(), shield_name), shield_rule_els)

        for (text_name, text_rule_els) in get_text_rule_groups(layer_declarations):
            insert_layer_style(map, layer, 'text style %d (%s)' % (next_counter(), text_name), text_rule_els)

        insert_layer_style(map, layer, 'point style %d' % next_counter(), get_point_rules(layer_declarations, dir))
        
        layer.set('name', 'layer %d' % next_counter())
        
        if 'id' in layer.attrib:
            del layer.attrib['id']
    
        if 'class' in layer.attrib:
            del layer.attrib['class']

    out = StringIO.StringIO()
    doc.write(out)
    
    return out.getvalue()
