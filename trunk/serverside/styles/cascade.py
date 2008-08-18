import simplejson
import cssutils.tokenize2

if __name__ == '__main__':

    t = cssutils.tokenize2.Tokenizer()
    
    print t
    
    s = """
    foo bar[baz=quuz]
    {
        color: red;
        font-family: "Helvetica Bold";
    }
    """
    
    for token in t.tokenize(s):
        print token