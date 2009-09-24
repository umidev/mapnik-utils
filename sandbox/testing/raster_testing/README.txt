http://openlayers.org/pipermail/tilecache/2008-November/001430.html

http://openlayers.org/pipermail/tilecache/2008-November/001438.html

http://lists.osgeo.org/pipermail/gdal-dev/2008-November/018987.html


On Mon, Oct 27, 2008 at 3:58 PM, Dane Springmeyer <blake@hailmail.net> wrote:
Roger,

Yes, I can replicate the 'edge' effect you describe in Mapnik as well, by either viewing a TileCache Mapnik layer in OL or specifically requesting of mapnik (using nik2img) the BBOX that tilecache requests.

The lines (actually missing pixel rows it seems) appear on the bottom edge of tile where the raster data is unrendered but not where vector data is effectively rendered.

These two bbox's trigger a one-pixel red line(where the raster file is not rendered) at the bottom of the image:

1) -20037508.34,10018754.17,-10018754.17,20037508.34
2) -20037508.34,0.0,0.0,20037508.34

...when requested as 256x256 tiles, while requesting a 255,256 tile will clip off the missing pixel row.


Sample image attached (not the upper red band is truly lacking data while the single pixel row on the bottom is the un-rendered data)

Dane



On Oct 27, 2008, at 11:58 AM, Roger André wrote:

Hi Dane,

A sample image will be too large to upload - it's just under 300 MB, but I've attached a mapfile.  I can send a .tfw for anyone who isn't able to add georeferencing to the image after they have created it.  

I would be interested in knowing from you whether a WMS request of the same nature, but made to Mapnik, will yield the same results.  And I have already posted the same question to the GeoServer list as well.

Thanks,

Roger
--

On Mon, Oct 27, 2008 at 10:54 AM, Dane Springmeyer <blake@hailmail.net> wrote:
Roger,

Uploading a test case with a sample image and sample mapfile prepackaged would be really useful to speed testing and keep consistent.

Dane



On Oct 27, 2008, at 9:40 AM, Roger André wrote:

Hi,

I'd like to ask for some help from a couple people running MapServer.  I would like to know if others are able to replicate some strange behavior I have noticed lately, and what versions of MapServer they are using.  Below are the steps needed, they don't take very long.

Step 1.  Create a large rectangular image of Size 14400 x 7200.

Step 2.  Assign georeferencing to the image:
gdal_translate -a_ullr -180 90 180 -90 -a_srs "EPSG:4326" big_black.tif wgs84_big_black.tif

Step 3. Load this image into a MapServer layer and set a contrasting IMAGECOLOR in the mapfile (red works well).

Step 4. Make sure you have a spherical mercator projection defined in your epsg file.
<900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs <>

Step 5. Make a WMS request for a tile that replicates one that TileCache makes:
http://localhost/cgi-bin/mapserv?map=/var/www/mapfiles/test/test.map
&layers=imagery
&srs=EPSG%3A900913
&version=1.1.1
&bbox=-20037508.34%2C-
20037508.34%2C-10018754.1704%2C-10018754.1704
&service=WMS
&width=256
&styles=
&format=image%2Fpng
&request=GetMap
&height=256

Step 6. Look at your resulting tile. Is it full of data from top to bottom, or is there a band of IMAGECOLOR at the bottom?

Step 7.  Let me know your results.

Thanks very much!

Roger
--

_______________________________________________
FWTools mailing list
FWTools@lists.maptools.org
http://lists.maptools.org/mailman/listinfo/fwtools
http://fwtools.maptools.org/


<bug.map>

