from mapnik import forward_, inverse_, Map, Coord, Envelope, Projection, scale_denominator

TRANSFORM_ERROR = 'Only Mapnik >= 0.6.0 supports projected transforms, see: http://trac.mapnik.org/ticket/117'

class ProjTransform(object):
    def __init__(self,from_prj,to_prj):
        self.to_prj = to_prj
        self.from_prj = from_prj
    
    def forward(self,geom):
        if self.to_prj.geographic and self.from_prj.geographic:
            return geom
        elif not self.to_prj.geographic and self.from_prj.geographic:
            return forward_(geom,self.to_prj)
        elif self.to_prj.geographic and not self.from_prj.geographic:
            return inverse_(geom,self.to_prj)
        elif not self.to_prj.geographic and not self.from_prj.geographic:
            if self.to_prj.params() == self.from_prj.params():
                return geom
            else:
                raise AttributeError(TRANSFORM_ERROR)
        
    def backward(self,geom):
        if self.to_prj.geographic and self.from_prj.geographic:
            return geom
        elif not self.to_prj.geographic and self.from_prj.geographic:
            return inverse_(geom,self.to_prj)
        elif self.to_prj.geographic and not self.from_prj.geographic:
            return forward_(geom,self.to_prj)
        elif not self.to_prj.geographic and not self.from_prj.geographic:
            if self.to_prj.params() == self.from_prj.params():
                return geom
            else:
                raise AttributeError(TRANSFORM_ERROR)

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

    def scale_denominator(self):
        srs = Projection(self.srs)
        return scale_denominator(self,srs.geographic)
    
    def resize(self,w,h):
        self.width = w
        self.height = h

class _Coord(Coord,_injector):
    def forward(self,obj):
        return forward_(self,obj)
    def inverse(self,obj):
        return inverse_(self,obj)

class _Envelope(Envelope,_injector):
    def forward(self,obj):
        return forward_(self,obj)
    def inverse(self,obj):
        return inverse_(self,obj)