#!/usr/bin/env python

# /home/dane/src/mapnik-utils/serverside/cascadenik/openstreetmap/style.xml

import sys
import werkzeug as z
from mimetypes import guess_type
import mapnik
import optparse
import os
import random
from subprocess import call

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
    <link rel="stylesheet" type="text/css" href="/js?f=mapfish/mfbase/ext/resources/css/ext-all.css" />
    <script type="text/javascript" src="/js?f=mapfish/mfbase/openlayers/lib/Firebug/firebug.js"></script>
    <!--<script type="text/javascript" src="/js?f=mapfish/mfbase/openlayers/lib/OpenLayers.js"></script>-->
    <script type="text/javascript" src="/js?f=mapfish/mfbase/ext/adapter/ext/ext-base.js"></script>
    <script type="text/javascript" src="/js?f=mapfish/mfbase/ext/ext-all-debug.js"></script>
    <script type="text/javascript">
      // Because of a bug in Firefox 2 we need to specify the MapFish base path.
      // See https://bugzilla.mozilla.org/show_bug.cgi?id=351282
      var gMfLocation = "/js?f=mapfish/mfbase/mapfish/";
    </script>
    <script type="text/javascript" src="/js?f=mapfish/mfbase/mapfish/MapFish.js"></script>
    <script type="text/javascript" src="/js?f=mapfish/examples/examples.js"></script>
 
    
	<style type="text/css">
	html, body {
        margin: 0;
        padding: 0;
        border: 0 none;
        overflow: hidden;
        height: 100%;
        }        
        
        #mapfileContainer {
            width: 100%;
            height: 100%;
        }
        #mapContainer {
            width: 48%;
            height: 95%;
            border: 1px solid gray;
        }
    </style>
    
<script language="Javascript" type="text/javascript" src="/js?f=edit_area/edit_area_full.js"></script>
<script language="Javascript" type="text/javascript">
        // initialisation
        editAreaLoader.init({
            id: "mapfileContainer"    // id of the textarea to transform        
            ,start_highlight: true    // if start with highlight
            ,allow_resize: "both"
            ,allow_toggle: true
            ,language: "en"
            ,syntax: "xml"
            ,syntax_selection_allow: "xml,css,python"
            ,font_size: "9"
			,font_family: "Lucida Grande, monospace"
			,toolbar: "new_document, save, load, fullscreen, |, search, go_to_line, |, undo, redo, |, select_font, |, syntax_selection, |,change_smooth_selection, highlight, reset_highlight, |, help"
			,save_callback: "postMapfile"
			,load_callback: "reloadMapfile" 
        });

    </script>
    
<script src="/js?f=openlayers/OpenLayers.js"></script>
<script type="text/javascript">
        var map, osm_official_tiles, mapnik;
        
        function postMapfile(id, content){
           var xml_string = content
           new OpenLayers.Request.POST({url:'.', data:xml_string, callback: refreshMap })
           //var current_extent = map.getExtent();
           //map.zoomIn(5)
           //map.zoomOut(5)
		}
        
        function refreshMap(request) {
		   var c = map.getCenter();
           var z = map.getZoom()
           mapnik.redraw(true);
           //map.removeLayer('mapnik');
           //map.addLayer('mapnik');
           map.setCenter(c,z)
           map.zoomIn(5)
           map.zoomOut(5)
		}
			
		function writeMapfile(request) {
    		var response = request.responseText;
    		editAreaLoader.setValue("mapfileContainer",'');
    		editAreaLoader.setValue("mapfileContainer",response);
    		var new_file= {id: "Mapfile", text: response, syntax: 'xml', title: 'beautiful title'};
    		editAreaLoader.openFile('Mapfile from command line', new_file);
            //$('mapfile') = response
		}

		function reloadMapfile() {
            new OpenLayers.Request.GET({url:'/mapfile',callback: writeMapfile})
            refreshMap();
		}
				
		function getMapfile() {
            new OpenLayers.Request.GET({url:'/mapfile',callback: writeMapfile})
		}

        OpenLayers.ImgPath = "/js?f=openlayers/img/";
        // reference local blank image
            Ext.BLANK_IMAGE_URL = '../../mfbase/ext/resources/images/default/s.gif';
          
            Ext.onReady(function() {

            var options = { 
                maxResolution: 156543.0339,
                units: 'm',
                theme : '/js?f=openlayers/style.css',
                projection: new OpenLayers.Projection("EPSG:900913"),
                maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34, 20037508.34, 20037508.34),
                };
            map = new OpenLayers.Map('mapContainer', options);
            
            mapnik = wms = new OpenLayers.Layer.WMS("Mapnik WMS","http://localhost:8000/tiles?", 
                {format:'image/png'},
                {
                //singleTile:true,
                //transitionEffect: "resize"
                } );                     
            
            map.addLayers([mapnik]);
            
            var mapcomponent = new mapfish.widgets.MapComponent({map: map});
       
            var viewport = new Ext.Viewport({
                layout:'border',
                    items: [
                        {
                            region: 'center',
                            contentEl: 'mapContainer',
                            minWidth: 200,
                            title: 'Mapnik Mapfish Viewer'
                        },{
                            region: 'east',
                            width: '45%',
                            contentEl: 'mapfileContainer',
                            split: true,
                            collapsible: true,
                            collapseMode: 'mini',
                            minWidth: 400,
                            title: 'EditArea Mapnik XML and CSS editor'
                        }]
            });
            
            map.addControl(new OpenLayers.Control.Scale());
            map.addControl(new OpenLayers.Control.MousePosition());
            map.addControl(new OpenLayers.Control.Navigation()); 
            map.addControl(new OpenLayers.Control.PanZoom());
            map.zoomToMaxExtent();
            });
    </script>
  </head>
  <body onload="getMapfile();">
     <!--<h2 style="position:absolute; z-index:10000; left: 100px;"><a href="/about/">nikserv</a></h2>-->
     <!--<h2 style="position:absolute; z-index:10000; right: 100px;"><a href="/tiles">Debugger</a></h2>-->
    <div id="mapContainer">
    </div>
    
    <div id="mapfileContainer">
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
        
        response = z.Response(image, status=200, mimetype=self.mime)
        response.content_length = len(image)
        return response

def not_found(req):
    return z.Response(u'<h1>Page Not Found</h1>', status=404, mimetype='text/html')

def openlayers(req,path='ol_merc.html'):
    global html
    if not html:
        try:
            f = open(path, 'rb')
            html = f.read()
            f.close()
        except IOError:
            return z.Response('Openlayers HTML/JS file not found: %s' % path,status=404, mimetype='text/html')
    
    return z.Response(html, status=200, mimetype='text/html')

def about(req):
    return z.Response(u'''<h1>Nikserv</h1>
        <p>Docs will go here.</p>
    ''', mimetype='text/html')

def getmapfile(req):
    global MAP_CACHE
    global mapfile
    
    #import pdb;pdb.set_trace()
    if not MAP_CACHE:
      mapfile_string = open(mapfile).read()
    else:
      mapfile_string = open(MAP_CACHE.mapfile).read()
      print 'reading from MAP_CACHE'
    return z.Response(mapfile_string,status=200, mimetype='text/xml')

def get_resource(request, filename):
    """Return a static resource from the js folder."""
    if not filename:
      return z.Response('Not Found no filename', status=404)
    else:
      filename = os.path.join(os.path.dirname(__file__), 'js', filename)

    if os.path.isfile(filename):
        mimetype = guess_type(filename)[0] or 'application/octet-stream'
        f = file(filename, 'rb')
        try:
            return z.Response(f.read(), mimetype=mimetype)
        finally:
            f.close()
    return z.Response('Not Found: %s' % filename, status=404)
        
views = {
    '/':        openlayers,
    '/about':   about,
    '/mapfile': getmapfile,
     
}

def application(environ, start_response):
    """
    """
    global mapfile
    #global kwargs
    global MAP_CACHE
    req = z.Request(environ)

    
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

    if req.path in views:
        resp = views[req.path](req)
    elif req.path == '/tiles':
        # Used cached map and projection if instance exists
        if not MAP_CACHE:
          MAP_CACHE = MapResponse(req.values,mapfile)
        resp = MAP_CACHE(req.values)
    elif req.path.rstrip('/').endswith('/js'):
            arg = req.args.get('f')
            resp = get_resource(req, arg)
    elif req.path.startswith('/images'):
            #import pdb;pdb.set_trace()
            resp = get_resource(req, req.path.lstrip('/'))
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
      
    application = z.DebuggedApplication(application, evalex=True)
      
    #call('open http://localhost:8000/ -a safari',shell=True)
    z.run_simple('localhost', 8000, application)