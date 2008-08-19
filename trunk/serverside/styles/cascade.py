import sys
import pprint
import simplejson
import cssutils.tokenize2

class Selector:
    def __init__(self, *atoms):
    
        if len(atoms) > 2:
            raise Exception('Only two-atom selectors are supported for Mapnik styles')

        if len(atoms) == 2 and atoms[1].hasTests():
            raise Exception('Only the first atom in a selector may have attributes in Mapnik styles')

        if len(atoms) == 2 and atoms[1].isID():
            raise Exception('Only the first atom in a selector may be an ID in Mapnik styles')
    
        if len(atoms) == 2 and atoms[1].isClass():
            raise Exception('Only the first atom in a selector may be a class in Mapnik styles')
    
        self.atoms = atoms[:]

    def specificity(self):
        """ Loosely based on http://www.w3.org/TR/REC-CSS2/cascade.html#specificity
        """
        ids = 0
        elements = len(self.atoms)
        tests = sum(len(a.tests) for a in self.atoms)
        
        return '%(ids)04d %(elements)04d %(tests)04d' % locals()

    def __repr__(self):
        return ' '.join(repr(a) for a in self.atoms)

class SelectorAtom:
    def __init__(self, name):
        self.name = name
        self.tests = []

    def addTest(self, test):
        self.tests.append(test)

    def hasTests(self):
        return bool(len(self.tests))
    
    def isID(self):
        return self.name.startswith('#')
    
    def isClass(self):
        return self.name.startswith('.')
    
    def __repr__(self):
        return self.name + ''.join(repr(t) for t in self.tests)

class SelectorAttributeTest:
    def __init__(self, arg1, op, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        return '[%(arg1)s%(op)s%(arg2)s]' % self.__dict__

class Property:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

def parse_rulesets(s):
    """
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
                if nname == 'IDENT' or (nname == 'CHAR' and value != '{'):
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

def trim_extra(tokens):
    """
    """
    while tokens[0][0] in ('S', 'COMMENT'):
        tokens = tokens[1:]

    while tokens[-1][0] in ('S', 'COMMENT'):
        tokens = tokens[:-1]
        
    return tokens

def postprocess_selector(tokens):
    """
    """
    tokens = (token for token in trim_extra(tokens))
    
    parts = []
    
    in_attribute = False
    
    for token in tokens:
        nname, value = token
        
        if not in_attribute:
            if nname == 'CHAR' and value in ('.', '#'):
                next_nname, next_value = tokens.next()
                
                if next_nname == 'IDENT':
                    parts.append(SelectorAtom(value + next_value))
                
            elif nname == 'IDENT':
                parts.append(SelectorAtom(value))

            elif (nname == 'CHAR' and value == '*'):
                parts.append(SelectorAtom(value))

            elif nname == 'CHAR' and value == '[':
                parts.append([])
                in_attribute = True
                
        elif in_attribute:
            if nname == 'IDENT':
                parts[-1].append(value)
                
            elif nname == 'CHAR' and value in ('<', '=', '>'):
                parts[-1].append(value)

            if nname == 'CHAR' and value == ']':
                parts[-2].addTest(SelectorAttributeTest(*parts[-1][:3]))
                parts = parts[:-1]
                in_attribute = False
    
    selector = Selector(*parts)
    
    return selector

def postprocess_property(tokens):
    """
    """
    tokens = trim_extra(tokens)
    
    if len(tokens) != 1:
        raise Exception('Too many tokens in property: ' + repr(tokens))
    
    if tokens[0][0] != 'IDENT':
        raise Exception('Incorrect type of token in property: ' + repr(tokens))
    
    return Property(tokens[0][1])

def postprocess_value(tokens):
    """
    """
    tokens = trim_extra(tokens)
    
    return tokens

if __name__ == '__main__':

    s = """
    .foo[baz>quuz] bar,
    *
    {
        color: red;
        font-family: /* boo yah */ "Helvetica Bold";
        font-size: 10px 10% 10em 10;
        background: url(http://example.com);
    }
    
    * { this: that !important; }
    """
    
    rulesets = parse_rulesets(s)
    
    rules = []
    
    for ruleset in rulesets:
        for declaration in ruleset['declarations']:
            for selector in ruleset['selectors']:
                rules.append({'selector': selector, 'property': declaration['property'], 'value': declaration['value'], 'position': declaration['position']})

    # sort by a css-like method
    rules.sort(key=lambda r: (r['selector'].specificity(), r['position'][0], r['position'][1]))

    #pprint.PrettyPrinter(indent=2).pprint(rulesets)
    pprint.PrettyPrinter(indent=2).pprint(rules)
