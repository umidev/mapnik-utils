import sys
import pprint
import simplejson
import cssutils.tokenize2

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

        if elements[0].names[0] != 'Layer' and elements[0].names[0][0] not in ('.', '#', '*'):
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
        
        return '%(ids)04d %(non_ids)04d %(tests)04d' % locals()

    def __repr__(self):
        return ' '.join(repr(a) for a in self.elements)

class SelectorElement:
    """ One element in selector, with names and tests.
    """
    def __init__(self):
        self.names = []
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
        self.name = name

    def __repr__(self):
        return self.name

def parse_stylesheet(s):
    """ Parse a string representing a stylesheet into a list of rulesets.
    """
    in_selectors = False
    in_block = False
    in_declaration = False # implies in_block
    in_property = False # implies in_declaration
    
    rulesets = []
    tokens = cssutils.tokenize2.Tokenizer().tokenize(s)
    
    for token in tokens:
        nname, value, line, col = token
        
        try:
            if not in_selectors and not in_block:
                if (nname in ('IDENT', 'HASH')) or (nname == 'CHAR' and value != '{'):
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
                    declaration['value'] = postprocess_value(declaration['value'])
                    in_declaration = False
    
                elif nname not in ('COMMENT'):
                    # in a declaration value
                    declaration['value'].append((nname, value))

        except:
            print >> sys.stderr, 'Exception at line %(line)d, column %(col)d' % locals()
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
                rules.append({'selector': selector, 'specificity': selector.specificity(), 'property': declaration['property'], 'value': declaration['value'], 'position': declaration['position']})

    # sort by a css-like method
    return sorted(rules, key=lambda r: (r['selector'].specificity(), r['position'][0], r['position'][1]))

def trim_extra(tokens):
    """ Trim comments and whitespace from each end of a list of tokens.
    """
    while tokens[0][0] in ('S', 'COMMENT'):
        tokens = tokens[1:]

    while tokens[-1][0] in ('S', 'COMMENT'):
        tokens = tokens[:-1]
        
    return tokens

def postprocess_selector(tokens):
    """ Convert a list of tokens into a Selector.
    """
    print tokens
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
    
    print elements
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

def postprocess_value(tokens):
    """
    """
    tokens = trim_extra(tokens)
    
    return tokens

if __name__ == '__main__':

    s = """
    Layer#foo.foo[baz>quuz] bar,
    *
    {
        color: red;
        font-family: /* boo yah */ "Helvetica Bold";
        font-size: 10px 10% 10em 10;
        background: url(http://example.com);
    }
    
    * { this: that !important; }
    """
    
    rulesets = parse_stylesheet(s)
    
    rules = unroll_rulesets(rulesets)
    

    #pprint.PrettyPrinter(indent=2).pprint(rulesets)
    pprint.PrettyPrinter(indent=2).pprint(rules)
