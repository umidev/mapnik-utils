__all__ = ("NikwebHttp",)

import os
import time
import logging

from nikweb.render import NikwebRenderFactory

class NikwebHttp(object):
    L = logging.getLogger('nikweb.http')
    
    def __init__(self, map_definitions, **kwargs):
        if not os.path.exists(map_definitions):
            raise ValueError("Map definitions directory doesn't exist: %s" % map_definitions)
        
        self.render_factory = NikwebRenderFactory(**kwargs)
        
        # preload the map definitions
        self.map_def_path = os.path.abspath(os.path.normpath(map_definitions))
        self.preload_definitions()
        
    def preload_definitions(self):
        self.L.info("Using map definitions from: %s", self.map_def_path)
        map_files = filter(lambda x: x.endswith('.xml'), os.listdir(self.map_def_path))
        t_start = time.time()
        for map_file in map_files:
            self.L.info("Loading %s ...", os.path.splitext(os.path.split(map_file)[1])[0])
            try:
                self.render_factory.getMap(os.path.join(self.map_def_path, map_file))
            except Exception, e:
                self.L.warn("Couldn't load %s: %s", map_file, e)
        t_end = time.time()
        self.L.info("Loaded %d maps in %0.2f seconds.", len(map_files), (t_end-t_start))
    
    def index(self):
        map_files = filter(lambda x: x.endswith('.xml'), os.listdir(self.map_def_path))
        map_defs = map(lambda x: os.path.splitext(x)[0], map_files)
        return map_defs
    
    def render(self, map_name, json_data):
        map_file = os.path.abspath(os.path.join(self.map_def_path, map_name + ".xml"))
        if not map_file.startswith(self.map_def_path):
            raise ValueError('Map tries to break out of map definitions path: map=%s path=%s' % (map_name, map_file))
        if not os.path.exists(map_file):
            raise KeyError('No such map definition: %s' % map)
        
        map_request = self.render_factory.requestFromJSON(map_file, json_data)
        
        # Render it
        t_start = time.time()
        try:
            image = map_request.render()
        except:
            self.L.exception("Error rendering map")
            raise
        t_end = time.time()
        
        return (image, map_request.format.encode('utf-8'), t_end-t_start)
