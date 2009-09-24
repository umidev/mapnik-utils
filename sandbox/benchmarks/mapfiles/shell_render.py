import os

ms = 'shp2img -m pg_tiger.map -o mapserver.png -l tiger_pg -e %s -s 600 400'

mk = 'nik2img.py pg_tiger.xml mapnik.png -e %s --no-open'

def mapnik(bbox):
    cmd = mk % bbox
    print cmd
    os.system(cmd)  

def mapserver(bbox):
    cmd = ms % bbox
    print cmd
    os.system(cmd)        
