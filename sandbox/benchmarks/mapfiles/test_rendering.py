import timeit

CALL_NUMBER = 4

bbox = '-100.784857743 30.7021366722 -99.3786077672 31.6396366563'

i = timeit.Timer("shell_render.mapnik('%s')" % bbox,"import shell_render")
i_avg = sum(i.repeat(1, CALL_NUMBER))/CALL_NUMBER

p = timeit.Timer("shell_render.mapserver('%s')" % bbox,"import shell_render")
p_avg = sum(p.repeat(1, CALL_NUMBER))/CALL_NUMBER

#diff = i_min - p_min
#per_diff = diff/i_min * 100

# times faster...
print 'with %s iterations...' % CALL_NUMBER
print 'mapnik: %s, mapserver: %s' % (i_avg/1.0269035978804999,p_avg)
