#!/usr/bin/env python

__all__ = ('NikwebRenderFactory', 'NikwebRenderRequest', 'DEFAULT_MAP_LAYER_PREFIX', 'DEFAULT_SIZE')

import tempfile
import os
import sys
import logging

import mapnik
try:
    import json
except ImportError:
    # Python <2.6 doesn't have a JSON module
    import simplejson as json

DEFAULT_MAP_LAYER_PREFIX = "NIKWEB"
DEFAULT_SIZE = (512, 512)

class NikwebRenderFactory(object):
    def __init__(self, debug=False, map_layer_prefix=DEFAULT_MAP_LAYER_PREFIX, default_size=DEFAULT_SIZE):
        # also accept None for any of the above options to use defaults
        self.debug = bool(debug)
        self.map_layer_prefix = map_layer_prefix or DEFAULT_MAP_LAYER_PREFIX
        self.default_size = default_size or DEFAULT_SIZE
        
        # A cache for the parsed map definitions
        # save us from reloading them every request
        self._map_cache = {}
    
    def requestFromJSON(self, map_definition, json_data):
        """ build a request from some JSON data. """
        return NikwebRenderRequest( self,
                                    map_definition,
                                    features=json_data['features'],
                                    bbox_image=json_data.get('bbox_image'),
                                    width=json_data.get('width'),
                                    height=json_data.get('height'),
                                    format=json_data.get('format'),
                                    bbox_image_buffer=json_data.get('bbox_image_buffer'))
    
    def getMap(self, definition_name, size=None):
        map_info = self._map_cache.get(definition_name, None)
        if (not map_info) or self.debug:
            # cache miss (always miss for DEBUG)
            map = mapnik.Map(*(size or self.default_size))
            mapnik.load_map(map, definition_name)
            
            data_layers = []
            for layer in map.layers:
                if layer.name.startswith(self.map_layer_prefix):
                    data_layers.append(layer)
            if not data_layers:
                raise ValueError("Layer(s) %s* not found in map definition" % self.map_layer_prefix)
            
            self._map_cache[definition_name] = (map, tuple(data_layers))
        else:
            map, data_layers = map_info
            # update the map size
            map.width = size[0]
            map.height = size[1]
        
        return (map, data_layers)
    
    def clearMapCache(self):
        self._map_cache.clear()


class NikwebRenderRequest(object):
    L = logging.getLogger('nikweb.NikwebRenderRequest')
    
    def __init__(self, factory, map_definition, features, bbox_image=None, width=None, height=None, format=None, bbox_image_buffer=None, map_layer_prefix="NIKWEB"):
        self.factory = factory
        self.map_definition = map_definition
        self.features = features
        self.bbox_image = bbox_image
        self.width = width
        self.height = height
        self.format = format or 'image/png'
        self.bbox_image_buffer = bbox_image_buffer
    
    def __str__(self):
        """ Return a GeoJSON representation of the request. """
        return json.dumps({
            'features': self.features,
            'width': self.width,
            'height': self.height,
            'format': self.format,
            'bbox_image': self.bbox_image,
            'type': 'FeatureCollection',
        }, encoding='utf-8')
    
    def get_size(self):
        """ 
        Get a size tuple.
        If width & height are specified, use those.
        If one of width/height are specified, calculate the other based on the bbox ratio.
        Default to 512x512
        """
        if self.width and self.height:
            return (int(self.width), int(self.height))
        elif self.bbox_image:
            bbox_size = (self.bbox_image[2]-self.bbox_image[0], self.bbox_image[3]-self.bbox_image[1])
            if self.width:
                return (int(self.width), int(self.width * bbox_size[1]/bbox_size[0]))
            elif self.height:
                return (int(self.height * bbox_size[0]/bbox_size[1]), int(self.height))
        return self.factory.default_size
    
    def get_format(self):
        """ Turns the mime-type (eg. image/png) into a format specifier (eg. png)"""
        return self.format.split('/')[1].lower()
    
    def render(self):
        """ Renders the request, returning a binary in the specified format. """
        map_size = self.get_size()
        map, data_layers = self.factory.getMap(self.map_definition, map_size)
        
        geojson_file = tempfile.NamedTemporaryFile(suffix='.json')
        try:
            # write the JSON to a temporary file
            geojson_file.write(str(self))
            geojson_file.flush()

            # find the layer definition(s) in the map xml and update it
            # to point to our temporary file
            geojson_dir, geojson_filename = os.path.split(geojson_file.name)
            for layer in data_layers:
                layer.datasource = mapnik.Ogr(base=geojson_dir, file=geojson_filename, layer='OGRGeoJSON')

            # set the map extent
            if self.bbox_image:
                # specified extent
                map_bbox = mapnik.Envelope(
                    mapnik.Coord(self.bbox_image[0], self.bbox_image[1]), 
                    mapnik.Coord(self.bbox_image[2], self.bbox_image[3])
                )
                map.zoom_to_box(map_bbox)
            else:
                # zoom to the extent of our data layers
                extent = data_layers[0].envelope()
                for l in data_layers[1:]:
                    extent += layer.envelope()
                map.zoom_to_box(extent)
                
            # if we have a buffer, apply it
            if self.bbox_image_buffer:
                extent = map.envelope()
                units = self.bbox_image_buffer[1].lower()
                if units == 'map':
                    # map-units
                    buffer = self.bbox_image_buffer[0]
                    extent.expand_to_include(extent.minx-buffer, extent.miny-buffer)
                    extent.expand_to_include(extent.maxx+buffer, extent.maxy+buffer)
                elif units == 'px':
                    # pixels
                    map.buffer_size = self.bbox_image_buffer[0]
                    extent = map.buffered_envelope()
                else:
                    self.L.warn("Unknown bbox_image_buffer units: %s", units)
                    
                # reapply our new extent
                map.zoom_to_box(extent)
            
            # render it
            map_im = mapnik.Image(*map_size)
            mapnik.render(map, map_im)
            return map_im.tostring(str(self.get_format()))
        
        finally:
            geojson_file.close()

if __name__ == "__main__":
    import optparse
    import time

    USAGE = ("Usage: %prog MAP_DEFINITION JSON_FILE OUTPUT_FILE\n\n"
             "The following environment variables do useful things:\n"
             "  NIKWEB_MAP_LAYER_PREFIX is the search prefix for data layer names\n"
             "  NIKWEB_DEBUG (0/1) turns on debugging output for error requests\n" )
        
    parser = optparse.OptionParser(usage=USAGE)
    (options, args) = parser.parse_args()
    
    if len(args) != 3:
        parser.error("Not enough arguments")
    
    map_def, json_data, output = args
    
    if not os.path.exists(map_def):
        parser.error("Map definition not found: %s" % map_def)
    
    logging.basicConfig(level=logging.DEBUG)
    
    mf = NikwebRenderFactory(debug=int(os.environ.get('NIKWEB_DEBUG','0')), 
                             map_layer_prefix=os.environ.get('NIKWEB_MAP_LAYER_PREFIX'))

    json_data = json.loads(open(json_data, 'rb').read())
    mr = mf.requestFromJSON(map_def, json_data)
    output_f = open(output, 'wb')
    
    # render
    t_start = time.time()
    image = mr.render()
    t_end = time.time()

    output_f.write(image)
    output_f.close()
    
    print >>sys.stderr, "\nRendered successfully in %0.3fs" % (t_end-t_start)
