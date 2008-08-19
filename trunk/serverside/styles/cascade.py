import sys
import pprint
import simplejson
import cssutils.tokenize2

def parse_rules(s):
    """
    """
    in_selectors = False
    in_block = False
    in_declaration = False # implies in_block
    in_property = False # implies in_declaration
    
    rules = []
    tokens = cssutils.tokenize2.Tokenizer().tokenize(s)
    
    for token in tokens:
        nname, value, line, col = token
        
        try:
            if not in_selectors and not in_block:
                if nname == 'IDENT' or (nname == 'CHAR' and value != '{'):
                    # beginning of a 
                    rules.append({'selectors': [[(nname, value)]], 'declarations': [], 'position': (line, col)})
                    in_selectors = True
                    
            elif in_selectors and not in_block:
                rule = rules[-1]
            
                if (nname == 'CHAR' and value == '{'):
                    # open curly-brace means we're on to the actual rules
                    rule['selectors'][-1] = trim_extra(rule['selectors'][-1])
                    in_selectors = False
                    in_block = True
    
                elif (nname == 'CHAR' and value == ','):
                    # comma means there's a break between selectors
                    rule['selectors'][-1] = trim_extra(rule['selectors'][-1])
                    rule['selectors'].append([])
    
                elif nname not in ('COMMENT'):
                    # we're just in a selector is all
                    rule['selectors'][-1].append((nname, value))
    
            elif in_block and not in_declaration:
                rule = rules[-1]
            
                if nname == 'IDENT':
                    # right at the start of a declaration
                    rule['declarations'].append({'property': [(nname, value)], 'value': []})
                    in_declaration = True
                    in_property = True
                    
                elif (nname == 'CHAR' and value == '}'):
                    # end of block
                    in_block = False
    
            elif in_declaration and in_property:
                declaration = rules[-1]['declarations'][-1]
            
                if nname == 'CHAR' and value == ':':
                    # end of property
                    declaration['property'] = postprocess_property(declaration['property'])
                    in_property = False
    
                elif nname not in ('COMMENT'):
                    # in a declaration property
                    declaration['property'].append((nname, value))
    
            elif in_declaration and not in_property:
                declaration = rules[-1]['declarations'][-1]
            
                if nname == 'CHAR' and value == ';':
                    # end of declaration
                    declaration['value'] = trim_extra(declaration['value'])
                    in_declaration = False
    
                elif nname not in ('COMMENT'):
                    # in a declaration value
                    declaration['value'].append((nname, value))

        except:
            print >> sys.stderr, 'Exception at line %(line)d, column %(col)d' % locals()
            raise

    return rules

def trim_extra(tokens):
    """
    """
    while tokens[0][0] in ('S', 'COMMENT'):
        tokens = tokens[1:]

    while tokens[-1][0] in ('S', 'COMMENT'):
        tokens = tokens[:-1]
        
    return tokens

def postprocess_property(tokens):
    """
    """
    tokens = trim_extra(tokens)
    
    if len(tokens) != 1:
        raise Exception('Too many tokens in property: ' + repr(tokens))
    
    if tokens[0][0] != 'IDENT':
        raise Exception('Incorrect type of token in property: ' + repr(tokens))
    
    return tokens[0][1]

if __name__ == '__main__':

    s = """
    .foo .bar[baz>quuz],
    *
    {
        color: red;
        font-family: /* boo yah */ "Helvetica Bold";
        font-size: 10px 10% 10em 10;
        background: url(http://example.com);
    }
    
    * { this: that; }
    """
    
    rules = parse_rules(s)

    pprint.PrettyPrinter(indent=4).pprint(rules)
