#!/usr/bin/env python

import os, sys
import math
import pprint
import urllib
import urlparse
import tempfile
import StringIO
import os.path
import zipfile
import itertools
import re
import ConfigParser

try:
    import lxml.etree as ElementTree
    from lxml.etree import Element, tostring
except ImportError:
    try:
        import xml.etree.ElementTree as ElementTree
        from xml.etree.ElementTree import Element, tostring
    except ImportError:
        import elementtree.ElementTree as ElementTree
        from elementtree.ElementTree import Element, tostring
        
def convert(src, outmml, outconfig):
    if os.path.exists(src): # local file
        # using 'file:' enables support on win32
        # for opening local files with urllib.urlopen
        # Note: this must only be used with abs paths to local files
        # otherwise urllib will think they are absolute, 
        # therefore in the future it will likely be
        # wiser to just open local files with open()
        if os.path.isabs(src) and sys.platform == "win32":
            src = 'file:%s' % src

    
    doc = ElementTree.parse(urllib.urlopen(src))
    map = doc.getroot()
    
    defaults = {}
    sources = {}
    
    all_srs = {}
    num_srs = 0
    
    name_filter = re.compile("\W")
    
    for layer in map.findall("Layer"):
        srs = layer.attrib['srs']
        srs_name = all_srs.get(srs)
        if not srs_name:
            srs_name = "srs%d"%num_srs
            defaults[srs_name] = srs
            all_srs[srs] = srs_name
            num_srs += 1

        id = layer.attrib.get('id')
        classes = layer.attrib.get('class') 
        keys = []
        if id:
            keys.append("%s_" % id)
        if classes:
            keys.extend(classes.split(" "))
        ds_name = name_filter.sub("_", " ".join(keys))
        
        
        params = {}
        for param in layer.find("Datasource").findall("Parameter"):
            params[param.attrib['name']] = param.text
        
        params.update(layer.find("Datasource").attrib)
        params['source_srs'] = "%%(%s)s" % srs_name
        sources[ds_name] = params
        
        layer.attrib['source_name'] = ds_name
        del layer.attrib['srs']
        layer.remove(layer.find("Datasource"))

    # now generate unique bases
    pg_params = {}
    
    for name, params in sources.items():
        if params.get('type') != 'postgis':
            continue
        pgp = {}
        for p in ("port","host","user","source_srs","password","type","dbname","estimate_extent","extent"):
            if p in params:
                pgp[p] = params[p]
                del params[p]
        pgp_name,pgp_data = pg_params.get(repr(pgp),(None,None))        
        if not pgp_name:
            pgp_name = "postgis_conn_%d" % len(pg_params)
            pg_params[repr(pgp)] = pgp_name,pgp
        
        params['base'] = pgp_name
        
    config = ConfigParser.RawConfigParser(defaults)        
    
    for name,params in itertools.chain(pg_params.values(), sources.items()):
        config.add_section(name)
        for pn,pv in params.items():
            config.set(name,pn,pv)
    
    with open(outconfig,"w") as oc:
        config.write(oc)
    
    map.insert(0,Element("DataSourcesConfig", src=outconfig))
    doc.write(outmml,"utf8")

    
        
        
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "usage: %s <source.mml> <output.mml> <output.cfg>" % sys.argv[0]
        exit(1)
    inmml, outmml, outcfg = sys.argv[1:4]
    convert(inmml, outmml, outcfg)

        