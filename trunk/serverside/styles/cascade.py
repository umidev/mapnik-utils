import re
import sys
import pprint
import simplejson
import operator
from binascii import unhexlify as unhex
from cssutils.tokenize2 import Tokenizer as cssTokenizer

# recognized properties

class color:
    def __init__(self, r, g, b):
        self.channels = r, g, b

    def __repr__(self):
        return '#%02x%02x%02x' % self.channels

    def __str__(self):
        return repr(self)

class uri:
    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return str(self.address) #'url("%(address)s")' % self.__dict__

    def __str__(self):
        return repr(self)

class boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if self.value:
            return 'true'
        else:
            return 'false'

    def __str__(self):
        return repr(self)

properties = {
    #--------------- map

    # 
    'map-bgcolor': color,

    #--------------- polygon symbolizer

    # 
    'polygon-fill': color,

    # 
    'polygon-opacity': float,

    #--------------- line symbolizer

    # CSS colour (default "black")
    'line-color': color,

    # 0.0 - n (default 1.0)
    'line-width': int,

    # 0.0 - 1.0 (default 1.0)
    'line-opacity': float,

    # miter, round, bevel (default miter)
    'line-join': ('miter', 'round', 'bevel'),

    # round, butt, square (default butt)
    'line-cap': ('butt', 'round', 'square'),

    # d0,d1, ... (default none)
    'line-dasharray': None, # Number(s)

    #--------------- text symbolizer

    # This is the query field you want to use for the label text, ie "street_name"
    'text-name': None, # (use selector for this)

    # Font name
    'text-face-name': str,

    # Font size
    'text-size': int,

    # ?
    'text-ratio': None, # ?

    # length before wrapping long names
    'text-wrap-width': int,

    # space between repeated labels
    'text-spacing': int,

    # allow labels to be moved from their point
    'text-label-position-tolerance': None, # ?

    # Maximum angle (in degrees) between two consecutive characters in a label allowed (to stop placing labels around sharp corners)
    'text-max-char-angle-delta': int,

    # Color of the fill ie #FFFFFF
    'text-fill': color,

    # Color of the halo
    'text-halo-fill': color,

    # Radius of the halo in whole pixels, fractional pixels are not accepted
    'text-halo-radius': int,

    # displace label by fixed amount on either axis.
    'text-dx': int,
    'text-dy': int,

    # Boolean to avoid labeling near intersection edges.
    'text-avoid-edges': boolean,

    # Minimum distance between repeated labels such as street names or shield symbols
    'text-min-distance': int,

    # Allow labels to overlap other labels
    'text-allow-overlap': boolean,

    # "line" to label along lines instead of by point
    'text-placement': ('point', 'line'),

    #--------------- point symbolizer

    # path to image file
    'point-file': uri, # none

    # px (default 4)
    'point-width': int,

    # px (default 4)
    'point-height': int,

    # png tiff
    'point-type': None, # png, tiff (derived from file)

    # true/false
    'point-allow-overlap': None, # ?

    #--------------- polygon pattern symbolizer

    # path to image file (default none)
    'pattern-file': uri,

    # px (default 4)
    'pattern-width': int,

    # px (default 4)
    'pattern-height': int,

    # png tiff (default none)
    'pattern-type': None, # png, tiff (derived from file)

    #--------------- shield symbolizer

    # 
    'shield-name': None, # (use selector for this)

    # 
    'shield-face-name': str,

    # 
    'shield-size': None, # ?

    # 
    'shield-fill': color,

    # 
    'shield-file': uri,

    # 
    'shield-type': None, # png, tiff (derived from file)

    # 
    'shield-width': int,

    # 
    'shield-height': int
}

class ParseException(Exception):
    pass

class Selector:
    """ Represents a complete selector with elements and attribute checks.
    """
    def __init__(self, *elements):
        if len(elements) > 2:
            raise ParseException('Only two-element selectors are supported for Mapnik styles')

        if len(elements) == 0:
            raise ParseException('At least one element must be present in selectors for Mapnik styles')

        if elements[0].names[0] not in ('Map', 'Layer') and elements[0].names[0][0] not in ('.', '#', '*'):
            raise ParseException('All non-ID, non-class first elements must be "Layer" Mapnik styles')
        
        if len(elements) == 2 and elements[1].countTests():
            raise ParseException('Only the first element in a selector may have attributes in Mapnik styles')

        if len(elements) == 2 and elements[1].countIDs():
            raise ParseException('Only the first element in a selector may have an ID in Mapnik styles')
    
        if len(elements) == 2 and elements[1].countClasses():
            raise ParseException('Only the first element in a selector may have a class in Mapnik styles')
    
        self.elements = elements[:]

    def specificity(self):
        """ Loosely based on http://www.w3.org/TR/REC-CSS2/cascade.html#specificity
        """
        ids = sum(a.countIDs() for a in self.elements)
        non_ids = sum((a.countNames() - a.countIDs()) for a in self.elements)
        tests = sum(len(a.tests) for a in self.elements)
        
        return (ids, non_ids, tests)

    def matches(self, tag, id, classes):
        """ Given an id and a list of classes, return True if this selector would match.
        """
        element = self.elements[0]
        unmatched_ids = [name[1:] for name in element.names if name.startswith('#')]
        unmatched_classes = [name[1:] for name in element.names if name.startswith('.')]
        unmatched_tags = [name for name in element.names if name is not '*' and not name.startswith('#') and not name.startswith('.')]
        
        if tag and tag in unmatched_tags:
            unmatched_tags.remove(tag)

        if id and id in unmatched_ids:
            unmatched_ids.remove(id)

        for class_ in classes:
            if class_ in unmatched_classes:
                unmatched_classes.remove(class_)
        
        if unmatched_tags or unmatched_ids or unmatched_classes:
            return False

        else:
            return True

    def __repr__(self):
        return ' '.join(repr(a) for a in self.elements)

class SelectorElement:
    """ One element in selector, with names and tests.
    """
    def __init__(self, names=None, tests=None):
        if names:
            self.names = names
        else:
            self.names = []

        if tests:
            self.tests = tests
        else:
            self.tests = []

    def addName(self, name):
        self.names.append(name)
    
    def addTest(self, test):
        self.tests.append(test)

    def countTests(self):
        return len(self.tests)
    
    def countIDs(self):
        return len([n for n in self.names if n.startswith('#')])
    
    def countNames(self):
        return len(self.names)
    
    def countClasses(self):
        return len([n for n in self.names if n.startswith('.')])
    
    def __repr__(self):
        return ''.join(self.names) + ''.join(repr(t) for t in self.tests)

class SelectorAttributeTest:
    """ Attribute test for a Selector, i.e. the part that looks like "[foo=bar]"
    """
    def __init__(self, arg1, op, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        return '[%(arg1)s%(op)s%(arg2)s]' % self.__dict__

class Property:
    """ A style property.
    """
    def __init__(self, name):
        if name not in properties:
            raise ParseException('"%s" is not a recognized property name' % name)
    
        self.name = name

    def group(self):
        return self.name.split('-')[0]
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self)

class Value:
    """ A style value.
    """
    def __init__(self, value, important):
        self.value = value
        self.important = important

    def importance(self):
        return int(self.important)
    
    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

def parse_stylesheet(s):
    """ Parse a string representing a stylesheet into a list of rulesets.
    """
    in_selectors = False
    in_block = False
    in_declaration = False # implies in_block
    in_property = False # implies in_declaration
    
    rulesets = []
    tokens = cssTokenizer().tokenize(s)
    
    for token in tokens:
        nname, value, line, col = token
        
        try:
            if not in_selectors and not in_block:
                if nname == 'CHAR' and value == '{':
                    # 
                    raise ParseException('Encountered unexpected opening "{"')

                elif (nname in ('IDENT', 'HASH')) or (nname == 'CHAR' and value != '{'):
                    # beginning of a 
                    rulesets.append({'selectors': [[(nname, value)]], 'declarations': []})
                    in_selectors = True
                    
            elif in_selectors and not in_block:
                ruleset = rulesets[-1]
            
                if (nname == 'CHAR' and value == '{'):
                    # open curly-brace means we're on to the actual rule sets
                    ruleset['selectors'][-1] = postprocess_selector(ruleset['selectors'][-1])
                    in_selectors = False
                    in_block = True
    
                elif (nname == 'CHAR' and value == ','):
                    # comma means there's a break between selectors
                    ruleset['selectors'][-1] = postprocess_selector(ruleset['selectors'][-1])
                    ruleset['selectors'].append([])
    
                elif nname not in ('COMMENT'):
                    # we're just in a selector is all
                    ruleset['selectors'][-1].append((nname, value))
    
            elif in_block and not in_declaration:
                ruleset = rulesets[-1]
            
                if nname == 'IDENT':
                    # right at the start of a declaration
                    ruleset['declarations'].append({'property': [(nname, value)], 'value': [], 'position': (line, col)})
                    in_declaration = True
                    in_property = True
                    
                elif (nname == 'CHAR' and value == '}'):
                    # end of block
                    in_block = False

                elif nname not in ('S', 'COMMENT'):
                    # something else
                    raise ParseException('Unexpected %(nname)s while looking for a property' % locals())
    
            elif in_declaration and in_property:
                declaration = rulesets[-1]['declarations'][-1]
            
                if nname == 'CHAR' and value == ':':
                    # end of property
                    declaration['property'] = postprocess_property(declaration['property'])
                    in_property = False
    
                elif nname not in ('COMMENT'):
                    # in a declaration property
                    declaration['property'].append((nname, value))
    
            elif in_declaration and not in_property:
                declaration = rulesets[-1]['declarations'][-1]
            
                if nname == 'CHAR' and value == ';':
                    # end of declaration
                    declaration['value'] = postprocess_value(declaration['value'], declaration['property'])
                    in_declaration = False
    
                elif nname not in ('COMMENT'):
                    # in a declaration value
                    declaration['value'].append((nname, value))

        except:
            #print >> sys.stderr, 'Exception at line %(line)d, column %(col)d' % locals()
            raise

    return rulesets

def unroll_rulesets(rulesets):
    """ Convert a list of rulesets (as returned by parse_stylesheet)
        into an ordered list of individual selectors and declarations.
    """
    rules = []
    
    for ruleset in rulesets:
        for declaration in ruleset['declarations']:
            for selector in ruleset['selectors']:
                rules.append({'selector': selector,
                              'property': declaration['property'],
                              'value': declaration['value'],
                              'sort key': (declaration['value'].importance(), selector.specificity(), declaration['position'])})

    # sort by a css-like method
    return sorted(rules, key=operator.itemgetter('sort key'))

def trim_extra(tokens):
    """ Trim comments and whitespace from each end of a list of tokens.
    """
    if len(tokens) == 0:
        return tokens
    
    while tokens[0][0] in ('S', 'COMMENT'):
        tokens = tokens[1:]

    while tokens[-1][0] in ('S', 'COMMENT'):
        tokens = tokens[:-1]
        
    return tokens

def postprocess_selector(tokens):
    """ Convert a list of tokens into a Selector.
    """
    tokens = (token for token in trim_extra(tokens))
    
    elements = []
    parts = []
    
    in_element = False
    in_attribute = False
    
    for token in tokens:
        nname, value = token
        
        if not in_element:
            if (nname == 'CHAR' and value in ('.', '*')) or nname in ('IDENT', 'HASH'):
                elements.append(SelectorElement())
                in_element = True
                # continue on to if in_element below...

        if in_element and not in_attribute:
            if nname == 'CHAR' and value == '.':
                next_nname, next_value = tokens.next()
                
                if next_nname == 'IDENT':
                    elements[-1].addName(value + next_value)
                
            elif nname in ('IDENT', 'HASH') or (nname == 'CHAR' and value == '*'):
                elements[-1].addName(value)

            elif nname == 'CHAR' and value == '[':
                in_attribute = True

            elif nname == 'S':
                in_element = False
                
        elif in_attribute:
            if nname == 'IDENT':
                parts.append(value)
                
            elif nname == 'CHAR' and value in ('<', '=', '>'):
                parts.append(value)

            elif nname == 'CHAR' and value == ']':
                elements[-1].addTest(SelectorAttributeTest(*parts[-3:]))
                in_attribute = False

            elif nname == 'S':
                in_element = False
    
    selector = Selector(*elements)
    
    return selector

def postprocess_property(tokens):
    """ Convert a one-element list of tokens into a Property.
    """
    tokens = trim_extra(tokens)
    
    if len(tokens) != 1:
        raise ParseException('Too many tokens in property: ' + repr(tokens))
    
    if tokens[0][0] != 'IDENT':
        raise ParseException('Incorrect type of token in property: ' + repr(tokens))
    
    return Property(tokens[0][1])

def postprocess_value(tokens, property):
    """
    """
    tokens = trim_extra(tokens)
    
    if len(tokens) >= 2 and (tokens[-2] == ('CHAR', '!')) and (tokens[-1] == ('IDENT', 'important')):
        important = True
        tokens = trim_extra(tokens[:-2])

    else:
        important = False
    
    value = tokens
    
    if properties[property.name] in (int, float, str, color, uri, boolean) or type(properties[property.name]) is tuple:
        if len(tokens) != 1:
            raise ParseException('Single value only for property "%(property)s"' % locals())

    if properties[property.name] is int:
        if tokens[0][0] != 'NUMBER':
            raise ParseException('Number value only for property "%(property)s"' % locals())

        value = int(tokens[0][1])

    elif properties[property.name] is float:
        if tokens[0][0] != 'NUMBER':
            raise ParseException('Number value only for property "%(property)s"' % locals())

        value = float(tokens[0][1])

    elif properties[property.name] is str:
        if tokens[0][0] != 'STRING':
            raise ParseException('String value only for property "%(property)s"' % locals())

        value = tokens[0][1][1:-1]

    elif properties[property.name] is color:
        if tokens[0][0] != 'HASH':
            raise ParseException('Hash value only for property "%(property)s"' % locals())

        if not re.match(r'^#([0-9a-f]{3}){1,2}$', tokens[0][1], re.I):
            raise ParseException('Unrecognized color value for property "%(property)s"' % locals())

        hex = tokens[0][1][1:]
        
        if len(hex) == 3:
            hex = hex[0]+hex[0] + hex[1]+hex[1] + hex[2]+hex[2]
        
        rgb = (ord(unhex(h)) for h in (hex[0:2], hex[2:4], hex[4:6]))
        
        value = color(*rgb)

    elif properties[property.name] is uri:
        if tokens[0][0] != 'URI':
            raise ParseException('URI value only for property "%(property)s"' % locals())

        raw = tokens[0][1]

        if raw.startswith('url("') and raw.endswith('")'):
            raw = raw[5:-2]
            
        elif raw.startswith("url('") and raw.endswith("')"):
            raw = raw[5:-2]
            
        elif raw.startswith('url(') and raw.endswith(')'):
            raw = raw[4:-1]

        value = uri(raw)
            
    elif properties[property.name] is boolean:
        if tokens[0][0] != 'IDENT' or tokens[0][1] not in ('true', 'false'):
            raise ParseException('true/false value only for property "%(property)s"' % locals())

        value = boolean(tokens[0][1] == 'true')
            
    elif type(properties[property.name]) is tuple:
        if tokens[0][0] != 'IDENT':
            raise ParseException('Identifier value only for property "%(property)s"' % locals())

        if tokens[0][1] not in properties[property.name]:
            raise ParseException('Unrecognized value for property "%(property)s"' % locals())

        value = tokens[0][1]

    return Value(value, important)

if __name__ == '__main__':

    s = """
    Layer#foo.foo[baz>quuz] bar,
    *
    {
        polygon-fill: #f90;
        text-face-name: /* boo yah */ "Helvetica Bold";
        text-size: 10;
        pattern-file: url('http://example.com');
        line-cap: square;
        text-allow-overlap: false;
    }
    
    * { text-fill: #ff9900 !important; }
    """
    
    rulesets = parse_stylesheet(s)
    
    rules = unroll_rulesets(rulesets)
    

    #pprint.PrettyPrinter(indent=2).pprint(rulesets)
    pprint.PrettyPrinter(indent=2).pprint(rules)
