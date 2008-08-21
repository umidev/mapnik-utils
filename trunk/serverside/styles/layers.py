import sys
import pprint
import urllib
import urlparse
import xml.etree.ElementTree
from xml.etree.ElementTree import Element
import cascade

counter = 0

def next_counter():
    global counter
    counter += 1
    return counter

def load_layers(file):
    """
    """
    return xml.etree.ElementTree.parse(urllib.urlopen(file))

def extract_rules(map, base):
    """
    """
    rules = []
    
    for stylesheet in map.findall('Stylesheet'):
        map.remove(stylesheet)
    
        if 'src' in stylesheet.attrib:
            url = urlparse.urljoin(base, stylesheet.attrib['src'])
            styles = urllib.urlopen(url).read()

        elif stylesheet.text:
            styles = stylesheet.text

        else:
            continue
            
        rulesets = cascade.parse_stylesheet(styles)
        rules += cascade.unroll_rulesets(rulesets)

    return rules

def insert_style(map, layer, style):
    """
    """
    style.tail = '\n    '
    map.insert(map._children.index(layer), style)
    
    stylename = Element('StyleName')
    stylename.text = style.get('name')
    stylename.tail = '\n    '
    layer.append(stylename)

def add_polygon_style(map, layer, declarations):
    """
    """
    has_polygon = False
    symbolizer = Element('PolygonSymbolizer')
    property_map = {'polygon-fill': 'fill', 'polygon-opacity': 'fill-opacity'}
    encountered = []
    
    for (property, value, selector) in reversed(declarations):
        if property.name in property_map and property.name not in encountered:
            parameter = Element('CssParameter', {'name': property_map[property.name]})
            parameter.text = str(value)
            symbolizer.append(parameter)

            encountered.append(property.name)
            has_polygon = True

    if has_polygon:
        rule = Element('Rule')
        rule.append(symbolizer)
        style = Element('Style', {'name': 'poly style %d' % next_counter()})
        style.append(rule)
        
        insert_style(map, layer, style)

def add_line_style(map, layer, declarations):
    """
    """
    has_line = False
    symbolizer = Element('LineSymbolizer')
    property_map = {'line-color': 'stroke', 'line-width': 'stroke-width',
                    'line-opacity': 'stroke-opacity', 'line-join': 'stroke-linejoin',
                    'line-cap': 'stroke-linecap', 'line-dasharray': 'stroke-dasharray'}
    encountered = []
    
    for (property, value, selector) in reversed(declarations):
        if property.name in property_map and property.name not in encountered:
            parameter = Element('CssParameter', {'name': property_map[property.name]})
            parameter.text = str(value)
            symbolizer.append(parameter)

            encountered.append(property.name)
            has_line = True

    if has_line:
        rule = Element('Rule')
        rule.append(symbolizer)
        style = Element('Style', {'name': 'line style %d' % next_counter()})
        style.append(rule)
        
        insert_style(map, layer, style)

if __name__ == '__main__':
    
    src = 'example.mml'
    doc = load_layers(src)
    map = doc.getroot()
    
    rules = extract_rules(map, src)

    layers = []
    
    for layer in map.findall('Layer'):
        layer_id = layer.get('id', None)
        layer_classes = layer.get('class', '').split()

        declarations = [(rule['property'], rule['value'], rule['selector'])
                        for rule in rules
                        if rule['selector'].matches(layer_id, layer_classes)]
        
        add_polygon_style(map, layer, declarations)
        add_line_style(map, layer, declarations)
        
        layer.set('name', 'layer %d' % next_counter())
        
        if 'id' in layer.attrib:
            del layer.attrib['id']
    
        if 'class' in layer.attrib:
            del layer.attrib['class']
    
        if declarations:
            layers.append({'layer': layer, 'rules': declarations})
            
    pprint.PrettyPrinter(indent=2).pprint(layers)

    doc.write(sys.stdout)
    print ''
