import pickle
from mapnik import *
from StringIO import StringIO
from copy import copy

# Have pickling
# Map, Envelope, Paramaters, Color
# Remain:
'''
'Coord','Datasource','Feature', 'Featureset', 'Filter','Layer','Query','Rule','Style', 'Symbolizer', 'Symbolizers'
'''

# 0 is ASCII, 1 is old binary, 2 is new binary
PROTOCOL = 2

def pack_mem(obj):
    return pickle.loads(pickle.dumps(obj,protocol=PROTOCOL))

def pack_file(obj):
    file_out = open('obj.pkl', 'wb')
    pickle.dump(obj,file_out,protocol=PROTOCOL)
    file_out.close()
    file_in = pickle.load(open('obj.pkl', 'rb'))
    return file_in

def pack_stream(obj):
    stream_out = StringIO()
    pickle.dump(m,stream_out,protocol=PROTOCOL)
    stream_out.flush()
    stream_in = StringIO(stream_out.getvalue())
    stream = pickle.loads(stream_in.getvalue())
    return stream

def pack_em(obj):
    packed = pack_mem(obj),pack_file(obj),pack_stream(obj)
    return list(packed)

def test_equivalence(pickles):
    failed = False
    while pickles:
        for one_pickle in pickles:
            maps = [p for p in pickles if isinstance(p,Map)]
            for other in maps:
                if isinstance(one_pickle,Map) and not one_pickle.__getstate__() ==  other.__getstate__():
                  print '%s and %s objects do not appear equivalent...' % (one_pickle,other)
                  failed = True
            non_maps = [p for p in pickles if not isinstance(p,Map)]
            for other in non_maps:
                if not isinstance(one_pickle,Map) and not one_pickle.__getinitargs__() ==  other.__getinitargs__():
                  print '%s and %s objects do not appear equivalent...' % (one_pickle,other)
                  failed = True
        pickles.remove(one_pickle)
        if not failed:
            print '%s is functionally equivalent to other %s %s  objects' % (repr(one_pickle),len(pickles),repr(pickles))

#
## mapnik::Map
#

maps = []
m = Map(45,45)
#m.background = Color(0,0,0)
m.buffer_size = 10

maps.extend(pack_em(m))

import pdb;pdb.set_trace()
#
## mapnik::color
#

colors = []
obj = Color('steelblue')
obj.a = 0
colors.append(pickle.loads(pickle.dumps(obj,protocol=PROTOCOL)))

obj = Color(70,130,180,0)
colors.append(pickle.loads(pickle.dumps(obj,protocol=PROTOCOL)))

#layers = []
#lyr = Layer('test')
#layers.extend(pack_em(lyr))

coords = []
coord = Coord(-122,48)
#coords.append(pack_em(coord))

def main():
    global tests
    test_equivalence(maps)
    test_equivalence(colors)
    #test_equivalence(layer)

if __name__ == '__main__':
    main()
