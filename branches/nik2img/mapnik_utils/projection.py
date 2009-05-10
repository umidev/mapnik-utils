import re
import mapnik
import urllib
import socket

socket.setdefaulttimeout(6)

MERC_PROJ4 = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'

class EasyProjection(mapnik.Projection):
    def __init__(self,srs):
        self.srs = srs
        self.srid = None
        self.method, self.proj = self.get_proj(self.srs)
        try:
            mapnik.Projection.__init__(self,self.proj)
        except RuntimeError, E:
            if self.method == 'epsg srid':
                sr_org = 'http://spatialreference.org/ref'
                srs_types = ['epsg','esri','sr-org','iau2000']
                for provider in srs_types:
                    url = '%s/%s/%s/' % (sr_org,provider, self.srs)       
                    print url
                    proj = self.get_from_sr_org(url)
                    if proj:
                        continue
                if proj:
                    self.srid = self.srs
                    mapnik.Projection.__init__(self,proj)
                else:
                    raise RuntimeError('Sorry, that projection was not found:' + E)
    
    @property
    def proj_obj(self):
        return mapnik.Projection(self.proj)

    def get_from_sr_org(self,srs):
        # http://trac.osgeo.org/gdal/changeset/11772
        url = '%s/proj4/' % srs.strip('/')
        resp = urllib.urlopen(url).read()
        if len(resp) > 1000:
            return None
        return resp
            
    def get_proj(self,srs):
        if isinstance(srs,(str,unicode)):
            if srs.isdigit():
                srs = int(srs)
        if isinstance(srs,int):
            self.srid = self.srs
            if srs == 900913 or srs == 3785:
                return 'custom proj4 stored in nik2img', MERC_PROJ4
            else:
                return 'epsg srid', '+init=epsg:%s' % srs
        elif re.match('^\+proj=.+$', srs):
            return 'proj4 literal', srs
        elif srs.startswith('http://'):
            proj4 = self.get_from_sr_org(srs)
            if not proj4:
                raise RuntimeError('%s failed to return a proj4 value' % srs)
            return 'proj4 from http://spatialreference.org', proj4
        elif re.match('^\+init=epsg:\d+$', srs.lower()):
            self.srid = self.srs
            return 'epsg srid', srs
        elif re.match('^epsg:\d+$', srs.lower()):
            self.srid = self.srs
            if srs == "epsg:900913" or srs == "epsg:3785":
                return 'custom proj4 stored in nik2img', MERC_PROJ4
            else:
                return 'epsg srid','+init=%s' % srs
        else:
            raise RuntimeError('failed to initialize EasyProjection with: %s' % srs)