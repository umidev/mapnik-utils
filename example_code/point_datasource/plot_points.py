import mapnik

m = mapnik.Map(256,256,"+proj=latlong +ellps=WGS84")
m.background = mapnik.Color('white')

# create data points
pds = mapnik.PointDatasource()
pds.add_point(-122.3,47.3,'Name','yellow!')
pds.add_point(-122.5,47.5,'Name','yellow!')
pds.add_point(-122.7,47.7,'Name','blue!')
pds.add_point(-122.8,47.9,'Name','blue!')

# create label symbolizers
text = mapnik.TextSymbolizer('Name','DejaVu Sans Bold',12,mapnik.Color('black'))
text.allow_overlap = True
text.displacement(30,-30)

# create point symbolizer for blue icons
blue = mapnik.PointSymbolizer('b.png','png',50,50)
blue.allow_overlap = True

# create point symbolizer for yellow icons
yellow = mapnik.PointSymbolizer('y.png','png',50,50)
yellow.allow_overlap = True

s = mapnik.Style()
r = mapnik.Rule()
r.symbols.append(text)
s.rules.append(r)

s2 = mapnik.Style()
r2 = mapnik.Rule()
r2.symbols.append(blue)
r2.filter = mapnik.Filter("[Name] = 'blue!'")
s2.rules.append(r2)

r3 = mapnik.Rule()
r3.symbols.append(yellow)
r3.filter = mapnik.Filter("[Name] = 'yellow!'")
s2.rules.append(r3)

icons = mapnik.Layer('Memory Datasource')
icons.datasource = pds
icons.styles.append('Point Style')
m.layers.append(icons)

labels = mapnik.Layer('Memory Datasource')
labels.datasource = pds
labels.styles.append('Label Style')
m.layers.append(labels)


m.append_style('Label Style',s)
m.append_style('Point Style',s2)

m.zoom_to_box(pds.envelope()*2)
mapnik.render_to_file(m,'test.png')
import os
os.system('open test.png')
