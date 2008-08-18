import pprint
import simplejson
import cssutils.tokenize2

if __name__ == '__main__':

    t = cssutils.tokenize2.Tokenizer()
    
    print t
    
    s = """
    foo bar[baz>quuz],
    *
    {
        color: red;
        font-family: /* boo yah */ "Helvetica Bold";
        font-size: 10px 10% 10em 10;
    }
    
    * { this: that }
    """
    
    in_selectors = False
    in_block = False
    in_declaration = False # implies in_block
    in_property = False # implies in_declaration
    
    results = []
    
    tokens = t.tokenize(s)
    
    for token in tokens:
        nname, value, line, col = token
        
        if not in_selectors and not in_block:
            if nname == 'IDENT' or (nname == 'CHAR' and value == '*'):
                # beginning of a 
                results.append({'selectors': [[(nname, value)]], 'declarations': [], 'position': (line, col)})
                in_selectors = True
                
        elif in_selectors and not in_block:
            if (nname == 'CHAR' and value == '{'):
                # open curly-brace means we're on to the actual rules
                in_selectors = False
                in_block = True

            elif (nname == 'CHAR' and value == ','):
                # comma means there's a break between selectors
                results[-1]['selectors'].append([])

            elif nname not in ('S', 'COMMENT'):
                # we're just in a selector is all
                results[-1]['selectors'][-1].append((nname, value))

        elif in_block and not in_declaration:
            if nname == 'IDENT':
                # right at the start of a declaration
                results[-1]['declarations'].append({'property': [(nname, value)], 'value': []})
                in_declaration = True
                in_property = True
                
            elif (nname == 'CHAR' and value == '}'):
                # end of block
                in_block = False

        elif in_declaration and in_property:
            if nname == 'CHAR' and value == ':':
                # end of property
                in_property = False

            elif nname not in ('S', 'COMMENT'):
                # in a declaration property
                results[-1]['declarations'][-1]['property'].append((nname, value))

        elif in_declaration and not in_property:
            if nname == 'CHAR' and value == ';':
                # end of declaration
                in_declaration = False

            elif nname not in ('S', 'COMMENT'):
                # in a declaration value
                results[-1]['declarations'][-1]['value'].append((nname, value))

    pprint.PrettyPrinter(indent=4).pprint(results)
