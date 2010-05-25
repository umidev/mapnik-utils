import ConfigParser
import StringIO

source_options ={"shape" : dict(file=str,encoding=str),
                 "postgis" : dict(cursor_size=int,
                                  dbname=str,
                                  geometry_field=str,
                                  host=str,
                                  initial_size=int,
                                  max_size=int,
                                  multiple_geometries=bool,
                                  password=str,
                                  persist_connection=bool,
                                  port=int,
                                  row_limit=int,
                                  table=str,
                                  srid=str,
                                  user=str),
                "ogr" : dict(layer=str),
                "osm" : dict(file=str, parser=str, url=str, bbox=str),
                "global": dict(type=str, estimate_extent=bool, extent=str)               
               }

GLOBALS_CONF = "globals"

class ChainedConfigParser(ConfigParser.SafeConfigParser):
    def __init__(self, last):
        ConfigParser.SafeConfigParser.__init__(self)
        d = last.defaults()
        d.update(self._defaults)
        self._defaults = d 

def extract_datasources(textdata, config_parser=None):
    data = StringIO.StringIO(textdata)
    data.seek(0)
    if config_parser:
        config = ChainedConfigParser(config_parser)
    else:
        config = ConfigParser.SafeConfigParser()
    config.readfp(data)
    
    sources = {}
    bases = set([])
        
    for sect in config.sections():
        if sect == GLOBALS_CONF: continue
        options = {}
        name = sect
        typ = config.get(sect,"type") if config.has_option(sect, "type") else None
        base = config.get(sect,"base") if config.has_option(sect, "base") else None
        source_srs = config.get(sect,"source_srs") if config.has_option(sect, "source_srs") else None

        if typ:
            options['type'] = typ
        elif base:
            bases.add(base)
            typ = config.get(base,"type")
            
        if not typ:
            raise Exception("Section [%s] missing 'type'" % sect)
        
        for opt,opt_type in source_options[typ].items():
            opt_value = None
            try:
                if opt_type == int:
                    opt_value = config.getint(sect,opt)
                elif opt_type == float:
                    opt_value = config.getfloat(sect,opt)
                elif opt_type == bool:
                    opt_value = config.getboolean(sect,opt)
                else:
                    opt_value = config.get(sect,opt)
            except ConfigParser.NoOptionError:
                pass
            if opt_value is not None:
                options[opt] = opt_value
        
        conf = dict(parameters=options)
        if base:
            conf['base'] = base
        if source_srs:
            conf['source_srs'] = source_srs
        sources[name] = conf
    
    return config, bases, sources

if __name__ == "__main__":
    import sys
    config, bases, sources = extract_datasources(open(sys.argv[1]).read())
    
    print extract_datasources(open(sys.argv[2]).read(), config)