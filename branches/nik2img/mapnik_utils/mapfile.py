import os
import sys
from mapnik import Map, load_map, load_map_from_string
from os.path import exists, dirname, basename


class Load(object):
    def __init__(self,mapfile,variables={},from_string=False):
        self.mapfile = mapfile
        self.from_string = from_string
        self.variables = variables
        self.mapfile_types = {'xml':'XML mapfile','mml':'Mapnik Markup Language', 'py':'Python map variable'}
        if self.from_string:
            self.file_type = 'xml'
        else:
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
        if self.from_string:
            return load_map_from_string(m,self.mapfile)
        else:
            return load_map(m,self.mapfile)

    def load_mml(self,m):    
        from cascadenik import load_map as load
        return load(m,self.mapfile)

    def load_py(self,m,map_variable='m'):
        """
        Instanciate a Mapnik Map object from an external python script.
        """
        py_path = os.path.abspath(self.mapfile)
        sys.path.append(dirname(py_path))
        py_module = basename(py_path).rstrip('.py')
        #import pdb;pdb.set_trace()
        module = __import__(py_module)
        py_map = getattr(module,map_variable,None)
        py_map.width = m.width
        py_map.height = m.height
        return py_map

    def variable_replace(self):
        import tempfile
        if self.from_string:
            mapfile_string = mapfile
        else:
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
        return self.load_mapfile(m)