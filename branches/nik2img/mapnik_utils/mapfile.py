import sys
from mapnik import Map, load_map
from os.path import exists, dirname, basename


class Load(object):
    def __init__(self,mapfile,variables={},paths_relative_to_xml=True):
        self.mapfile = mapfile
        self.paths_relative_to_xml = paths_relative_to_xml
        self.variables = variables
        self.mapfile_types = {'xml':'XML mapfile','mml':'Mapnik Markup Language', 'py':'Python map variable'}
        self.file_type = self.mapfile.split('.')[-1]
        self.validate()
        
    def validate(self):
        if not exists(self.mapfile):
            raise AttributeError('Mapfile not found')
        if not self.file_type in self.mapfile_types:
            raise AttributeError('Invalid mapfile type: only these extension allowed: %s' % ', '.join(self.mapfile_types.keys()))
        return True

    def get_type_desc(self):
        if self.mapfile.endswith('xml'):
            return self.mapfile_types['xml']
        elif self.mapfile.endswith('mml'):
            return self.mapfile_types['mml']
        elif self.mapfile.endswith('py'):
            return self.mapfile_types['py']
        else:
            return None

    def load_xml(self,m):
        try:
            return load_map(m,self.mapfile,False,self.paths_relative_to_xml,False)
        except Exception, E:
            #sys.stderr.write('Warning: %s' % E)
            return load_map(m,self.mapfile)

    def load_mml(self,m):    
        from cascadenik import load_map as load
        return load(m,self.mapfile)

    def load_py(self,m,map_variable='m'):
        """
        Instanciate a Mapnik Map object from an external python script.
        """
        py_path = dirname(self.mapfile)
        os.path.append(py_path)
        py_module = basename(os.path).split('.')[0]
        module = __import__(py_module)
        py_map = getattr(module,map_variable,None)
        py_map.width = self.m.width
        py_map.height = self.m.height
        return py_map

    def variable_replace(self):
        import tempfile
        mapfile_string = open(self.mapfile).read()
        for line in mapfile_string.splitlines():
            for key,value in self.variables.items():
                line.replace(key,value)
        tmp = tempfile.NamedTemporaryFile(suffix='.xml', mode = 'w')
        tmp.write(mapfile_string)
        tmp.flush()
        return tmp.name
          
    def load_mapfile(self,m):
        if self.variables:
            self.mapfile = self.variable_replace()
        load = getattr(self,'load_%s' % self.file_type)
        return load(m)

    def build_map(self,width,height):
        m = Map(width,height)
        self.load_mapfile(m)
        return m