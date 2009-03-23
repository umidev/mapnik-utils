import re
from mapnik import Map, Layer, Coord, Envelope
from projection import EasyProjection

try:
    from mapnik import ProjTransform
except:
    pass

BoostPythonMetaclass = Coord.__class__
                
class _injector(object):
    class __metaclass__(BoostPythonMetaclass):
        def __init__(self, name, bases, dict):
            for b in bases:
                if type(b) not in (self, type):
                    for k,v in dict.items():
                        setattr(b,k,v)
            return type.__init__(self, name, bases, dict)

class _Map(Map,_injector):

    def set_easy_srs(self,srs):
        self.srs = EasyProjection(srs).params()

    @property
    def proj_obj(self):
        return EasyProjection(self.srs)

    def find_layer(self,name):
        lyr = [l for l in self.layers if l.name.lower() == name.lower()]
        if not lyr:
            raise ValueError('Layer not found, available layers are: "%s"' % ', '.join(self.layer_names()))
        return lyr[0]
    
    def layer_names(self):
        return [l.name for l in self.layers]

    def active_layers(self):
        return [l.name for l in self.layers if l.active]

    def zoom_to_layer(self,layer):
        layer = self.find_layer(layer)
        layer_box = layer.envelope()
        box = layer_box.transform(layer.proj_obj,self.proj_obj)
        self.zoom_to_box(box)

    def layers_bounds(self):
        first = self.layers[0]
        new_box = first.envelope().transform(first.proj_obj,self.proj_obj)
        for layer in self.layers:
            layer_box = layer.envelope()
            box = layer_box.transform(layer.proj_obj,self.proj_obj)
            new_box.expand_to_include(box)
        return new_box
    
    def zoom_to_layers(self,layers):
        first = self.find_layer(layers[0])
        new_box = first.envelope().transform(first.proj_obj,self.proj_obj)
        for lyr in layers:
            layer = self.find_layer(layer)
            layer_box = layer.envelope()
            box = layer_box.transform(layer.proj_obj,self.proj_obj)
            new_box.expand_to_include(box)
        self.zoom_to_box(new_box)

    def zoom_to_level(self,level):
        c = self.layers_bounds().center()
        self.set_center_and_zoom(c.x,c.y,level=level,geographic=self.proj_obj.geographic)
    
    @property
    def max_resolution(self):
        #self.zoom_max()
        return self.envelope().width()/self.width    

    def get_scales(self,number):
        return [self.max_resolution / 2 ** i for i in range(int(number))]        

    def get_scale_for_zoom_level(self,level):
        return self.get_scales(level+1)[level]
    
    # http://trac.mapnik.org/browser/trunk/src/map.cpp#L245
    def set_center_and_zoom(self,lon,lat,level=0,geographic=True):
        coords = Coord(lon,lat)
        if geographic and not self.proj_obj.geographic:
            coords = coords.forward(self.proj_obj)
        w,h = self.width, self.height
        res = self.get_scale_for_zoom_level(level) 
        box = Envelope(coords.x - 0.5 * w * res,
                    coords.y - 0.5 * h * res, 
                    coords.x + 0.5 * w * res, 
                    coords.y + 0.5 * h * res)
        self.zoom_to_box(box) 

    def set_center_and_radius(self,lon,lat,radius=None,geographic=True):
        coords = Coord(lon,lat)
        box = Envelope(coords.x - radius,
                      coords.y - radius,
                      coords.x + radius,
                      coords.y + radius)
        if geographic and not self.proj_obj.geographic:
            box = box.forward(self.proj_obj)
        self.zoom_to_box(box)

    def zoom_max(self):
        max_extent = Envelope(-179.99999694572804,-85.0511285163245,179.99999694572804,85.0511287798066)
        if not self.proj_obj.geographic:
            max_extent = max_extent.forward(self.proj_obj)
        self.zoom_to_box(max_extent)

    def select_layers(self,names):
        disactivated = []
        selected = []
        if not isinstance(names,list):
            names = [names]
        for lyr in self.layers:
            if not lyr.name in names:
                lyr.active = False
                disactivated.append(lyr.name)
            else:
                lyr.active = True
                selected.append(lyr.name)
        return selected, disactivated 

    def validate_datasources(self):
        for layer in self.layers:
            if not layer.datasource:
                raise IOError("Datasource not found for layer '%s'" % layer.name)
        return True

    def active_rules_for_layer(self,layer):
        active = []
        if not isinstance(layer,Layer):
            layer = self.find_layer(layer)
        for style in layer.styles:
            try:
                sty_obj = self.find_style(style)
            except KeyError:
                sty_obj = None
            if sty_obj:
                for rule in sty_obj.rules:
                    rule_attr = {}
                    if rule.active(self.scale()):
                        rule_attr['parent_style'] = style 
                        rule_attr['filter'] = str(rule.filter)
                        rule_attr['min_scale'] = rule.min_scale
                        rule_attr['max_scale'] = rule.max_scale
                        active.append(rule_attr)
        return active
    
    def intersecting_layers(self):
        lyrs = []
        for layer in self.layers:
            lyr_attr = {}
            layer_box = layer.envelope().transform(layer.proj_obj,self.proj_obj)
            if layer_box.intersects(self.envelope()):
                lyr_attr['name'] = layer.name
                lyr_attr['visible'] = layer.visible(self.scale())
                lyr_attr['active_style_rules'] = self.active_rules_for_layer(layer)
                lyrs.append(lyr_attr)
        return lyrs

    def to_wld(self, x_rotation=0.0, y_rotation=0.0):
        """
        Outputs an ESRI world file that can be used to load the resulting
        image as a georeferenced raster in a variety of gis viewers.
        
        '.wld' is the most common extension used, but format-specific extensions
        are also looked for by some software, such as '.tfw' for tiff and '.pgw' for png
        
        A world file file is a plain ASCII text file consisting of six values separated
        by newlines. The format is: 
            pixel X size
            rotation about the Y axis (usually 0.0)
            rotation about the X axis (usually 0.0)
            pixel Y size (negative when using North-Up data)
            X coordinate of upper left pixel center
            Y coordinate of upper left pixel center
         
        Info from: http://gdal.osgeo.org/frmt_various.html#WLD
        """
        extent = self.envelope()
        pixel_x_size = (extent.maxx - extent.minx)/self.width
        pixel_y_size = (extent.maxy - extent.miny)/self.height
        upper_left_x_center = extent.minx + 0.5 * pixel_x_size + 0.5 * x_rotation
        upper_left_y_center = extent.maxy + 0.5 * (pixel_y_size*-1) + 0.5 * y_rotation
        # http://trac.osgeo.org/gdal/browser/trunk/gdal/gcore/gdal_misc.cpp#L1296
        wld_string = '''%.10f\n%.10f\n%.10f\n-%.10f\n%.10f\n%.10f\n''' % (
                pixel_x_size, # geotransform[1] - width of pixel
                y_rotation, # geotransform[4] - rotational coefficient, zero for north up images.
                x_rotation, # geotransform[2] - rotational coefficient, zero for north up images.
                pixel_y_size, # geotransform[5] - height of pixel (but negative)
                upper_left_x_center, # geotransform[0] - x offset to center of top left pixel
                upper_left_y_center # geotransform[3] - y offset to center of top left pixel.
            )
        return wld_string
                  
class _Layer(Layer,_injector):

    @property
    def proj_obj(self):
        return EasyProjection(self.srs)

    def set_srs_by_srid(self,srid):
        self.srs = EasyProjection(srid).params()
    
    def datasource_dict(self):
        d = {}
        attr = []
        if self.datasource:
            groups = self.datasource.describe().split('\n\n')
            prefix = groups[0].split('\n')
            d['type'] = prefix[0].split('=')[1]
            d['encoding'] = prefix[1].split('=')[1]
            p = {}
            p['name'] = prefix[2].split('=')[1]
            p['type'] = prefix[3].split('=')[1]
            p['size'] = prefix[4].split('=')[1]
            attr.append(p)
            for group in groups[1:]:
                for item in group.split('\n'):
                    p = {}
                    if item:
                        i = item.split('=')
                        p[i[0]] = i[1]
                        attr.append(p)
        d['properties'] = attr
        return d


class _Coord(Coord,_injector):
    def transform(self,from_prj,to_prj):
        trans = ProjTransform(from_prj,to_prj)
        return trans.forward(self)

class _Envelope(Envelope,_injector):
    def transform(self,from_prj,to_prj):
        trans = ProjTransform(from_prj,to_prj)
        return trans.forward(self)

if __name__ == '__main__':
    import doctest
    doctest.testmod()