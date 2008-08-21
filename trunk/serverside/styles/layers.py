import sys
import pprint
import urllib
import urlparse
import xml.etree.ElementTree
import cascade

if __name__ == '__main__':
    
    file = 'example.mml'
    
    map = xml.etree.ElementTree.parse(open(file))
    
    rules = []
    
    for stylesheet in map.findall('Stylesheet'):
        if 'src' in stylesheet.attrib:
            url = urlparse.urljoin(file, stylesheet.attrib['src'])
            styles = urllib.urlopen(url).read()

        elif stylesheet.text:
            styles = stylesheet.text

        else:
            continue
            
        rulesets = cascade.parse_stylesheet(styles)
        rules += cascade.unroll_rulesets(rulesets)
        
    layers = []
    
    for layer in map.findall('Layer'):
        layer_id = layer.attrib.get('id', None)
        layer_classes = layer.attrib.get('class', '').split()
        layer_rules = [(rule['property'], rule['value'], rule['selector'])
                       for rule in rules
                       if rule['selector'].matches(layer_id, layer_classes)]
        
        if layer_rules:
            layers.append({'layer': layer, 'rules': layer_rules})
    
    pprint.PrettyPrinter(indent=2).pprint(layers)

    #print urlparse.urljoin('/tmp/', '/hello.txt')