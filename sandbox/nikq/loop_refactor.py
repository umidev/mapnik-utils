#!/usr/bin/env python

import sys
import psycopg2
import psycopg2.extras
from psycopg2 import ProgrammingError
#import psycopg2.OperationalError


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
        def __init__(self, default_params=None ):
            self.default_params = default_params
            self.settings = ['dbname','user','host']
            self.fatal_param = []
            self.values = {}
        
        def setup(self):
            if self.fatal_param:
                for item in self.fatal_param:
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
                        if line.endswith('\c'):
                            self.fatal_param.append('dbname')
                            self.setup()
                    else:
                        self.values[item] = self.default_params[item]
                        
        def connect(self):
            d,u,h = self.values['dbname'],self.values['user'],self.values['host']
            params = "dbname=%s user=%s host=%s" % (d,u,h)
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
                sql = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                return sql
           
class query(object):
        def __init__(self, cursor):
            self.cursor = cursor
            self.cmd_lines = []
            self.stop = False

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
               if line.endswith('\q'): sys.exit()
               if line.endswith('\c'):
                   self.fatal_param.append('dbname')
                   self.setup()

        
        def run(self):
            query = ' '.join(self.cmd_lines)
            try:
                self.cursor.execute("""%s;""" % query)
            except ProgrammingError, E:
                print E
                self.go() # run main again?
            #try:
            return self.cursor.fetchall()
            #except:
              # return '','',''
            #return query
               
        
if __name__ == "__main__":
  d = {'dbname':'cobi','user':'postgres','host':''}
  c = connection(d)
  c.setup()
  print c.values
  cursor = c.connect()
  q = query(cursor)
  try:
    while 1:
      #print 'nikq >>',
      #start = raw_input()
      q.go()
      #print q.cmd_lines
      all = q.run()
      print all
      if q.stop:
        break
      else:
        q.cmd_lines = []
        #q.go()
  except KeyboardInterrupt:
    sys.exit()