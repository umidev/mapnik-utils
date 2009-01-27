#!/usr/bin/env python

# /home/dane/src/mapnik-utils/serverside/cascadenik/openstreetmap/style.xml

import os
import sys
import mapnik
import optparse
import random
from subprocess import call
from werkzeug import Response, Request, DebuggedApplication,  run_simple

sys.stdout = sys.stderr

MAP_CACHE = None
#mapfile = None
mapfile = ''
#kwargs = {}

html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <title>Test</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style type="text/css">
        html, body { height: 98%; }
        
        #xml {
            float:right;
            width: 50%;
            height: 95%;
        }
        
        #mapfile {
            height: 700px;
            width: 100%;
        }
        #map {
            width: 48%;
            height: 95%;
            border: 1px solid gray;
        }
    </style>
    
<script language="Javascript" type="text/javascript" src="http://www.cdolivet.net/editarea/editarea/edit_area/edit_area_full.js"></script>
<!--<script language="Javascript" type="text/javascript" src="http://localhost/edit_area/edit_area_full.js"></script>-->
<script language="Javascript" type="text/javascript">
        // initialisation
        editAreaLoader.init({
            id: "mapfile"    // id of the textarea to transform        
            ,start_highlight: true    // if start with highlight
            ,allow_resize: "both"
            ,allow_toggle: true
            ,language: "en"
            ,syntax: "xml"
            ,syntax_selection_allow: "xml,css,python"
            ,font_size: "9"
			,font_family: "Lucida Grande, monospace"
			,toolbar: "save, fullscreen, |, search, go_to_line, |, undo, redo, |, select_font, |, syntax_selection, |,change_smooth_selection, highlight, reset_highlight, |, help"
			,save_callback: "postMapfile"   
        });

    </script>
    
<script src="http://dev.openlayers.org/nightly/OpenLayers.js"></script>
<script type="text/javascript">
        var map, osm_official_tiles, mapnik;
        
        function postMapfile(id, content){
           var xml_string = content
           new OpenLayers.Request.POST({url:'.', data:xml_string,callback: refreshMap })
           //var current_extent = map.getExtent();
           //map.zoomIn(5)
           //map.zoomOut(5)
		}
		
		function refreshMap(request) {
		   console.log('called')
		   var c = map.getCenter();
           var z = map.getZoom()
           mapnik.redraw(true);
           //map.removeLayer('mapnik');
           //map.addLayer('mapnik');
           map.setCenter(c,z)
           map.zoomIn(5)
           map.zoomOut(5)
		}
		
        function postMapfile2() {
           var xml_string = $('mapfile').value
           new OpenLayers.Request.POST({url:'.', data:xml_string, callback: refreshMap })
                      
        }
        
        function init() {
            var options = { 
                maxResolution: 156543.0339,
                units: 'm',
                projection: new OpenLayers.Projection("EPSG:900913"),
                maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34, 20037508.34, 20037508.34),
                };
            map = new OpenLayers.Map("map", options);
            mapnik = wms = new OpenLayers.Layer.WMS("Mapnik WMS","http://localhost:8000/tiles?", 
                {format:'image/png'},
                {
                //singleTile:true,
                //transitionEffect: "resize"
                } );                     
            map.addLayers([mapnik]);
            map.addControl(new OpenLayers.Control.Scale());
            map.addControl(new OpenLayers.Control.MousePosition());
            map.addControl(new OpenLayers.Control.Navigation()); 
            map.addControl(new OpenLayers.Control.PanZoom());
            map.zoomToMaxExtent();
            }
    </script>
  </head>
  <body onload="init()">
     <!--<h2 style="position:absolute; z-index:10000; left: 100px;"><a href="/about/">nikserv</a></h2>-->
     <!--<h2 style="position:absolute; z-index:10000; right: 100px;"><a href="/tiles">Debugger</a></h2>-->
    <div id="xml">
     <textarea id="mapfile" name="mapfile" class="xml">
<?xml version="1.0" encoding="utf-8"?>
<!-- http://spatialreference.org/ref/epsg/2163/ -->
<Map bgcolor="#8cb6d3" srs="+init=epsg:900913">
    <Style name="states_outlines">
        <Rule>
            <LineSymbolizer>
                <CssParameter name="stroke-width">0.3</CssParameter>
            </LineSymbolizer>
        </Rule>
    </Style>
    <Style name="states_shp_labels">
        <Rule>
            <TextSymbolizer name="STATE_ABBR" face_name="DejaVu Sans Book" size="12" fill="#000000"></TextSymbolizer>
        </Rule>
    </Style>
    <Style name="states_shp_styles" srs="+init=epsg:900913">
        <Rule>
            <Filter>([PERSONS]&lt;2000000)</Filter>
            <PolygonSymbolizer>
                <CssParameter name="fill">#6CAE4C</CssParameter>
            </PolygonSymbolizer>
        </Rule>        
        <Rule>
            <Filter>(([PERSONS]&gt;2000000) and ([PERSONS]&lt;4000000))</Filter>
            <PolygonSymbolizer>
                <CssParameter name="fill">#3B7AB3</CssParameter>
            </PolygonSymbolizer>
        </Rule>
        <Rule>
            <Filter>([PERSONS]&gt;4000000)</Filter>
            <PolygonSymbolizer>
                <CssParameter name="fill">#88000F</CssParameter>
            </PolygonSymbolizer>
        </Rule>
    </Style>
    <Layer name="states" status="1">
        <StyleName>states_shp_styles</StyleName>
        <StyleName>states_outlines</StyleName>
        <StyleName>states_shp_labels</StyleName>
        <Datasource>
            <Parameter name="file">/Users/spring/projects/utils/sandbox/wsgimap/us_states_merc</Parameter>
            <Parameter name="type">shape</Parameter>
        </Datasource>
    </Layer>
</Map>

</textarea>
     <!--<textarea id="example_1" style="height: 350px; width: 100%;" name="test_1">asd</textarea>
     <input type="submit" value="Render" name="Render" onclick="javascript:postMapfile()"/>-->
    </div>
    <div id="map">
    </div>
 </body>
</html>
"""

class MapResponse(object):
    """
    """
    def __init__(self, req, mapfile, *kwargs):    
        """
        """
        self.mapnik_map = None
        self.mapfile = mapfile
        self.projection = None
        self.singletile = False
        self.width = None
        self.height = None
        self.srs = None
        
        if int(req.get('WIDTH')):
          self.width = int(req.get('WIDTH'))
        if int(req.get('HEIGHT')):
          self.height = int(req.get('HEIGHT'))       
        if str(req.get('FORMAT')):
          self.mime = str(req.get('FORMAT'))
        if req.get('SRS'):
          self.srs = req.get('SRS')
        
        self.load_map()
    
    def load_map(self):
        self.mapnik_map = mapnik.Map(self.width,self.height)
        mapnik.load_map(self.mapnik_map, self.mapfile)

        if self.srs:
            proj_init = str('+init=%s' % self.srs).lower()
            self.projection = mapnik.Projection(proj_init)
            self.mapnik_map.srs = self.projection.params()

    def __call__(self,req):
        """
        """
        print
        print 'Using %s' % self.mapfile
        print
        bbox = req.get('BBOX')
        env = map(float,bbox.split(','))
        bbox = mapnik.Envelope(*env)
        
        if self.singletile:
          self.mapnik_map.width,self.mapnik_map.height = int(req.get('WIDTH')),int(req.get('HEIGHT'))

        self.mapnik_map.zoom_to_box(bbox)
        draw = mapnik.Image(self.mapnik_map.width,self.mapnik_map.height)
        mapnik.render(self.mapnik_map,draw)
        image = draw.tostring('png256')
        
        response = Response(image, status=200, mimetype=self.mime)
        response.content_length = len(image)
        return response

def not_found(req):
    return Response(u'<h1>Page Not Found</h1>', status=404, mimetype='text/html')

def openlayers(req,path='ol_merc.html'):
    global html
    if not html:
        try:
            f = open(path, 'rb')
            html = f.read()
            f.close()
        except IOError:
            return Response('Openlayers HTML/JS file not found: %s' % path,status=404, mimetype='text/html')
    
    return Response(html, status=200, mimetype='text/html')

def about(req):
    return Response(u'''<h1>Nikserv</h1>
        <p>Docs will go here.</p>
    ''', mimetype='text/html')

views = {
    '/':        openlayers,
    '/about':   about
}

def application(environ, start_response):
    """
    """
    global mapfile
    #global kwargs
    global MAP_CACHE
    req = Request(environ)

    
    if req.method == 'POST' and not req.data == 'Paste mapfile here':
      #import pdb;pdb.set_trace()
      xml_string = req.data
      mapfile = '/tmp/mapfile%s.xml' % random.random()
      tmp = open(mapfile, 'w+b')
      tmp.write(xml_string)
      tmp.seek(0)
      tmp.close()
      MAP_CACHE.mapfile = mapfile
      MAP_CACHE.load_map()
      print 'assigning mapfile!!!'
    else:
      print 'NOPE....%s' % req.data

    if req.path in views:
        resp = views[req.path](req)
    elif req.path == '/tiles':
        # Used cached map and projection if instance exists
        if not MAP_CACHE:
          MAP_CACHE = MapResponse(req.values,mapfile)
        resp = MAP_CACHE(req.values)
    else:
        resp = not_found(req)
    
      
    return resp(environ, start_response)


if __name__ == '__main__':
    
    parser = optparse.OptionParser(usage="""python nikserv.py <mapfile.xml> [options]
    
    Usage:
        $ python nikserv.py /path/to/mapfile.xml
    """)
    
    #parser.add_option('-b', '--bbox', dest='bbox_projected')
    
    (options, args) = parser.parse_args()
    import sys
    if len(args) < 1:
      if not mapfile:
        sys.exit('\nPlease provide the path to a mapnik mml or xml \n')
    else:
      mapfile = args[0]
    
    # set up for optional command line args from nik2img
    #for k,v in vars(options).items():
    #  if v != None:
    #   kwargs[k] = v
       
    #print kwargs
      
    application = DebuggedApplication(application, evalex=True)
      
    #call('open http://localhost:8000/ -a safari',shell=True)
    run_simple('localhost', 8000, application)