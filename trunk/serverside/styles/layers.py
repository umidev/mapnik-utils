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

def is_gym_projection(map):
    """ Return true if the map projection matches that used by VEarth, Google, OSM, etc.
    """ 
    # expected
    gym = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null'
    gym = dict([p.split('=') for p in gym.split() if '=' in p])
    
    # observed
    srs = map.get('srs', '')
    srs = dict([p.split('=') for p in srs.split() if '=' in p])
    
    for p in gym:
        if srs.get(p, None) != gym.get(p, None):
            return False

    return True

def extract_rules(map, base):
    """ Given a Map element and a URL base string, remove and return a complete
        list of style declarations from any Stylesheet elements found within.
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

def insert_layer_style(map, layer, style):
    """ Given a Map element, a Layer element, and a Style element, insert the
        Style element into the flow and point to it from the Layer element.
    """
    style.tail = '\n    '
    map.insert(map._children.index(layer), style)
    
    stylename = Element('StyleName')
    stylename.text = style.get('name')
    stylename.tail = '\n        '
    layer.insert(layer._children.index(layer.find('Datasource')), stylename)
    #layer.append(stylename)

def add_map_style(map, declarations):
    """
    """
    property_map = {'map-bgcolor': 'bgcolor'}
    
    for (property, value, selector) in declarations:
        if property.name in property_map:
            map.set(property_map[property.name], str(value))

def add_polygon_style(map, layer, declarations):
    """ Given a Map element, a Layer element, and a list of declarations
        consisting of (property, value, selector) tuples, create a new Style element
        with a PolygonSymbolizer, add it to Map and refer to it in Layer.
    """
    has_polygon = False
    symbolizer = Element('PolygonSymbolizer')
    property_map = {'polygon-fill': 'fill', 'polygon-opacity': 'fill-opacity'}
    encountered = []
    
    # collect all the applicable declarations into a symbolizer element
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
        
        insert_layer_style(map, layer, style)

def add_line_style(map, layer, declarations):
    """ Given a Map element, a Layer element, and a list of declarations
        consisting of (property, value, selector) tuples, create a new Style element
        with a LineSymbolizer, add it to Map and refer to it in Layer.
    """
    has_line = False
    symbolizer = Element('LineSymbolizer')
    property_map = {'line-color': 'stroke', 'line-width': 'stroke-width',
                    'line-opacity': 'stroke-opacity', 'line-join': 'stroke-linejoin',
                    'line-cap': 'stroke-linecap', 'line-dasharray': 'stroke-dasharray'}
    encountered = []
    
    # collect all the applicable declarations into a symbolizer element
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
        
        insert_layer_style(map, layer, style)

def add_text_styles(map, layer, declarations):
    """ Given a Map element, a Layer element, and a list of declarations
        consisting of (property, value, selector) tuples, create new Style elements
        with a TextSymbolizer, add them to Map and refer to them in Layer.
    """
    has_text = False
    symbolizer = Element('TextSymbolizer')
    property_map = {'text-face-name': 'face_name', 'text-size': 'size', 
                    'text-ratio': 'text_ratio', 'text-wrap-width': 'wrap_width', 'text-spacing': 'spacing',
                    'text-label-position-tolerance': 'label_position_tolerance',
                    'text-max-char-angle-delta': 'max_char_angle_delta', 'text-fill': 'fill',
                    'text-halo-fill': 'halo_fill', 'text-halo-radius': 'halo_radius',
                    'text-dx': 'dx', 'text-dy': 'dy',
                    'text-avoid-edges': 'avoid_edges', 'text-min-distance': 'min_distance',
                    'text-allow-overlap': 'allow_overlap', 'text-placement': 'placement'}

    text_names = {}
    
    # first, break up the text declarations among different names (see <TextSymbolizer name=""/>)
    for (property, value, selector) in declarations:
        if len(selector.elements) is 2 and len(selector.elements[1].names) is 1:
            text_name = selector.elements[1].names[0]

            if not text_names.has_key(text_name):
                text_names[text_name] = {}

            if property.name in property_map:
                text_names[text_name][property.name] = value
                has_text = True

    # make as many styles as are necessary
    if has_text:
        for text_name in text_names:
            symbolizer = Element('TextSymbolizer', {'name': text_name})
        
            for property_name in text_names[text_name]:
                symbolizer.set(property_map[property_name], str(text_names[text_name][property_name]))

            rule = Element('Rule')
            rule.append(symbolizer)
            style = Element('Style', {'name': 'text style %d' % next_counter()})
            style.append(rule)

            insert_layer_style(map, layer, style)

def get_applicable_declaration(element, rules):
    """ Given an XML element and a list of rules, return the ones
        that match as a list of (property, value, selector) tuples.
    """
    element_tag = element.tag
    element_id = element.get('id', None)
    element_classes = element.get('class', '').split()

    return [(rule['property'], rule['value'], rule['selector'])
            for rule in rules
            if rule['selector'].matches(element_tag, element_id, element_classes)]

if __name__ == '__main__':
    
    src = 'example.mml'
    doc = load_layers(src)
    map = doc.getroot()
    
    rules = extract_rules(map, src)
    
    add_map_style(map, get_applicable_declaration(map, rules))

    layers = []
    
    for layer in map.findall('Layer'):
        declarations = get_applicable_declaration(layer, rules)
        
        add_polygon_style(map, layer, declarations)
        add_line_style(map, layer, declarations)
        add_text_styles(map, layer, declarations)
        
        layer.set('name', 'layer %d' % next_counter())
        
        if 'id' in layer.attrib:
            del layer.attrib['id']
    
        if 'class' in layer.attrib:
            del layer.attrib['class']
    
        if declarations:
            layer.set('status', 'on')
            layers.append({'layer': layer, 'rules': declarations})
        else:
            layer.set('status', 'off')
            
    #pprint.PrettyPrinter(indent=2).pprint(layers)

    doc.write(sys.stdout)
