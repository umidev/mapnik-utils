import sys
import pprint
import simplejson
import cssutils.tokenize2

class Selector:
    def __init__(self, *atoms):
    
        if len(atoms) > 2:
            raise Exception('Only two-atom selectors are supported for Mapnik styles')

        if len(atoms) == 0:
            raise Exception('At least one atom must be present in selectors for Mapnik styles')

        if atoms[0].names[0] != 'Layer' and atoms[0].names[0][0] not in ('.', '#', '*'):
            raise Exception('All non-ID, non-class first elements must be "Layer" Mapnik styles')
        
        if len(atoms) == 2 and atoms[1].hasTests():
            raise Exception('Only the first atom in a selector may have attributes in Mapnik styles')

        if len(atoms) == 2 and atoms[1].countIDs():
            raise Exception('Only the first atom in a selector may have an ID in Mapnik styles')
    
        if len(atoms) == 2 and atoms[1].countClasses():
            raise Exception('Only the first atom in a selector may have a class in Mapnik styles')
    
        self.atoms = atoms[:]

    def specificity(self):
        """ Loosely based on http://www.w3.org/TR/REC-CSS2/cascade.html#specificity
        """
        ids = sum(a.countIDs() for a in self.atoms)
        non_ids = sum((a.countNames() - a.countIDs()) for a in self.atoms)
        tests = sum(len(a.tests) for a in self.atoms)
        
        return '%(ids)04d %(non_ids)04d %(tests)04d' % locals()

    def __repr__(self):
        return ' '.join(repr(a) for a in self.atoms)

class SelectorAtom:
    def __init__(self):
        self.names = []
        self.tests = []

    def addName(self, name):
        self.names.append(name)
    
    def addTest(self, test):
        self.tests.append(test)

    def hasTests(self):
        return bool(len(self.tests))
    
    def countIDs(self):
        return len([n for n in self.names if n.startswith('#')])
    
    def countNames(self):
        return len(self.names)
    
    def countClasses(self):
        return len([n for n in self.names if n.startswith('.')])
    
    def __repr__(self):
        return ''.join(self.names) + ''.join(repr(t) for t in self.tests)

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
    print tokens
    tokens = (token for token in trim_extra(tokens))
    
    atoms = []
    parts = []
    
    in_atom = False
    in_attribute = False
    
    for token in tokens:
        nname, value = token
        
        if not in_atom:
            if (nname == 'CHAR' and value in ('.', '*')) or nname in ('IDENT', 'HASH'):
                atoms.append(SelectorAtom())
                in_atom = True
                # continue on to if in_atom below...

        if in_atom and not in_attribute:
            if nname == 'CHAR' and value == '.':
                next_nname, next_value = tokens.next()
                
                if next_nname == 'IDENT':
                    atoms[-1].addName(value + next_value)
                
            elif nname in ('IDENT', 'HASH') or (nname == 'CHAR' and value == '*'):
                atoms[-1].addName(value)

            elif nname == 'CHAR' and value == '[':
                in_attribute = True

            elif nname == 'S':
                in_atom = False
                
        elif in_attribute:
            if nname == 'IDENT':
                parts.append(value)
                
            elif nname == 'CHAR' and value in ('<', '=', '>'):
                parts.append(value)

            elif nname == 'CHAR' and value == ']':
                atoms[-1].addTest(SelectorAttributeTest(*parts[-3:]))
                in_attribute = False

            elif nname == 'S':
                in_atom = False
    
    print atoms
    selector = Selector(*atoms)
    
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
    
    rulesets = parse_rulesets(s)
    
    rules = []
    
    for ruleset in rulesets:
        for declaration in ruleset['declarations']:
            for selector in ruleset['selectors']:
                rules.append({'selector': selector, 'specificity': selector.specificity(), 'property': declaration['property'], 'value': declaration['value'], 'position': declaration['position']})

    # sort by a css-like method
    rules.sort(key=lambda r: (r['selector'].specificity(), r['position'][0], r['position'][1]))

    #pprint.PrettyPrinter(indent=2).pprint(rulesets)
    pprint.PrettyPrinter(indent=2).pprint(rules)
