from subprocess import call
import nik2img

# pulled from tilecache requests 
bboxes = [
'-20037508.34,-20037508.34,-10018754.170,-10018754.1704',
'-20037508.3428,-16213033.188,20038946.4359,16213801.0676',
'-20037508.34,10018754.17,-10018754.17,20037508.34',
'-20037508.34,0.0,0.0,20037508.34',
]

idx = 1
for bbox in bboxes:
  call('nik2img.py -s 256,256 -v -m mapnik_gdal.xml -o %s_gdal.png -r %s' % (idx,bbox),shell=True)
  call('nik2img.py -s 256,256 -v -m mapnik_raster.xml -o %s_rast.png -r %s' % (idx,bbox),shell=True)
  idx += 1

# Map('mapnik_gdal.xml','gdal_test.png',width=256,height=256,verbose=True,bbox_projected='-20037508.34,-20037508.34,-10018754.170,-10018754.1704').open()