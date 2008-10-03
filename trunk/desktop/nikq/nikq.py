#!/usr/bin/env python

import os
import sys
import psycopg2
import psycopg2.extras
from mapnik import *
from sqlparse import parse
from random import *

UNIQUE = True

# Database settings
DBNAME = 'geographic_admin'
USER= 'postgres'
PASSWORD = ''
HOST = 'localhost'


def get_geom_ref(table):
    connection = psycopg2.connect("dbname=%s user=%s host=%s" % (DBNAME,USER,HOST))
    sql = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "select f_geometry_column, srid, type from geometry_columns where f_table_name = '%s'" % table
    sql.execute("""%s;""" % query)
    try:
        return sql.fetchall()[0]
    except:
        return '','',''

def get_feat_count(table):
    connection = psycopg2.connect("dbname=%s user=%s host=%s" % (DBNAME,USER,HOST))
    sql = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if GROUP_BY:
        query = "select count(*) from (%s group by %s)" % (query_strip, GROUP_BY)
        print query
        sys.exit()
    else:
        query = "select count(*) from %s" % (table)
    sql.execute("""%s;""" % query)
    return sql.fetchall()[0][0]

def output_definition(table):
    connection = psycopg2.connect("dbname=%s user=%s host=%s" % (DBNAME,USER,HOST))
    sql = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query =  """SELECT a.attname
     FROM pg_class c, pg_attribute a, pg_type t
     WHERE c.relname = '%s'
     AND a.attnum > 0
     AND a.attrelid = c.oid
     AND a.atttypid = t.oid """ % (table)
    sql.execute("""%s;""" % query)
    print sql.fetchall()

try:
    query = sys.argv[1]
except:
    print
    print "Usage: %s 'select * from world_worldborders order by pop2005 desc limit 100'" % sys.argv[0]
    print
    sys.exit()

if query.find('group by') > -1:
    idx = query.find('group by')
    query_strip = query[:idx]
    GROUP_BY = query[(int(idx)+9):]
    print query_strip
    table = parse(query_strip).tables[0].lower()
    
else:

    table = parse(query).tables[0].lower()

if not query.find('*') > -1 and not query.find('geom') > -1:
    output_definition(table)
        
else:

    name, srid, type = get_geom_ref(table)
    m = Map(800,600)
    m.background = Color('transparent')
    

         
    if query.find('limit') > -1:
        idx = query.find('limit') + 6
        features = int(query[idx:])
    else:
        features = get_feat_count(table)
    
    def random_rgb():
      return int(random() * 255)
    
    def generate_unique_values(features):
      s = Style()
      if UNIQUE:
          for feat in range(1,features+1):
            r=Rule('%s' % feat)
            condition = '[id]=%s' % (feat)
            r.filter = Filter(condition)
            rgb = '%s%s,%s%s,%s%s' % (random_rgb(),'%',random_rgb(),'%',random_rgb(),'%')
            r.symbols.append(PolygonSymbolizer(Color('rgb(%s)' % rgb)))
            r.symbols.append(LineSymbolizer(Color('black'),.1))
            s.rules.append(r)
      else:
          r=Rule()
          if type.find('STRING') > -1:
              pass
          else:
              r.symbols.append(PolygonSymbolizer(Color('green')))
          if type.find('STRING') > -1 or type.find('POLYGON') > -1:
              r.symbols.append(LineSymbolizer(Color('black'),.3))
          s.rules.append(r)  
      return s
    
    m.append_style('My Style',generate_unique_values(features))
    lyr = Layer('shape')
    
    TABLE = '(%s) as t' % query
    lyr.datasource = PostGIS(host=HOST,user=USER,password=PASSWORD,dbname=DBNAME,table=TABLE)
    lyr.styles.append('My Style')
    
    m.layers.append(lyr)
    
    m.zoom_to_box(lyr.envelope())
    render_to_file(m,'test.png')
    os.system('open test.png')