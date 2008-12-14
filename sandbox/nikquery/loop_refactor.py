#!/usr/bin/env python

import sys
import psycopg2
import psycopg2.extras
from psycopg2 import ProgrammingError
#import psycopg2.OperationalError
import optparse

# pickle settings
# prompt to unpickle or overwrite

'''
http://proj.badc.rl.ac.uk/csml/browser/TI02-CSML/trunk/dbtesting/postgresDB.py
http://stackoverflow.com/questions/70797/python-and-user-input
http://www.python.org/doc/2.5.2/lib/module-cmd.html
http://www.python.org/doc/2.5.2/lib/module-fileinput.html
http://code.activestate.com/recipes/437932/
http://www.python.org/doc/2.5.2/lib/module-code.html

'''


class connection(object):
        def __init__(self, default_params={} ):
            self.default_params = default_params
            self.settings = ['dbname','user','host']
            self.fatal_param = []
            self.values = {}
            self.params = {}
            self.connection = None
            self.cursor = None
        
        def setup(self):
            if self.fatal_param:
                for item in self.fatal_param:
                    #print 'Invalid %s' % item
                    print 'try again: %s >>' % item,
                    line = raw_input()
                    if line.endswith('\q'): sys.exit()
                    self.values[item] = line
                    self.fatal_param.remove(item)
                    self.connect()
            else:
                for item in self.settings:
                    if not self.default_params.has_key(item):
                        print '%s >>' % item,
                        line = raw_input()
                        self.values[item] = line
                        if line.endswith('\q'): sys.exit()
                        if line.endswith('\c') or line.startswith('\c'):
                            self.fatal_param.append('dbname')
                            self.setup()
                    else:
                        self.values[item] = self.default_params[item]
                        
        def connect(self):
            d,u,h = self.values['dbname'],self.values['user'],self.values['host']
            self.params = "dbname=%s user=%s host=%s" % (d,u,h)
            try:
                connection = psycopg2.connect(params)
            except Exception, E:
                if E.message.find('role') > -1:
                    self.fatal_param.append('user')
            try:
                connection = psycopg2.connect(params)
            except Exception, E:
                if E.message.find('host') > -1:
                    self.fatal_param.append('host')
            try:
                connection = psycopg2.connect(params)
            except Exception, E:
                if E.message.find('database') > -1:
                    self.fatal_param.append('dbname')
            if self.fatal_param:
                self.setup()
            else:
                #return params
                self.connection = psycopg2.connect(self.params)
                print 'Connecting with: %s' % self.params
                self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                return self.cursor
                
           
class query(object):
        #def __init__(self, params):
        def __init__(self, cursor):
            #self.params = params
            #self.connection = psycopg2.connect(self.params)
            #self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.cursor = cursor
            self.cmd_lines = []
            self.stop = False
            self.reconnect = False

        def go(self):
            while 1:
               print 'sql >>',
               line = raw_input()
               if line.endswith(';'):
                 if not line == ';':
                   self.cmd_lines.append(line.rstrip(';'))
                 break
               else:
                 self.cmd_lines.append(line)
               if line.endswith('\q'):
                   print 'stop request....'
                   sys.exit()
               if line.endswith('\c') or line.startswith('\c'):
                   self.reconnect = line.strip('\c')
                   if not self.reconnect:
                     self.cmd_lines.remove(line)
                     print 'Please provide database name!'
                   else:
                     print 'changing...to %s' % self.reconnect
                     break
        
        def run(self):
            sql_statement = ' '.join(self.cmd_lines)
            try:
                self.cursor.execute("""%s;""" % sql_statement)
            except ProgrammingError, E:
                print E
                self.go() # run main again?
            #try:
            return self.cursor.fetchall()
            #except:
              # return '','',''
            #return query
               
        
if __name__ == "__main__":
    parser = optparse.OptionParser(usage="""python nikquery.py [shapefile]
    
    Usage:
        $ python nikquery.py /path/to/shapefile.shp

    """)
    
    #parser.add_option('-b', '--bbox', dest='bbox_projected')
    (options, args) = parser.parse_args()
    import sys
    if len(args):
      print '\nEntering shapefile query mode (leave blank for postgis connection)\n'
      print 'but... not supported yet, so leaving'
      sys.exit()
    else:
      print '\nEntering postgis query mode\n'
    
    kwargs = {}
    for k,v in vars(options).items():
      if v != None:
       kwargs[k] = v
       
    print kwargs
      
    d = {'dbname':'cobi','user':'postgres','host':''}
    con = connection(d)
    con.setup()
    #print con.values
    # initiate connection looping
    cursor = con.connect()
    
    # initiate query looping
    q = query(cursor)
    querying = True
    try:
      while querying:
        q.go()
        if q.stop:
          break
        elif q.reconnect:
          print 'reconnect caught'
          con.values['dbname'] = q.reconnect  
          # reinitiate query looping
          q.cursor = con.connect()
        else:
          all = q.run()
          q.cmd_lines = []
          #q.go()
    except KeyboardInterrupt:
      sys.exit()