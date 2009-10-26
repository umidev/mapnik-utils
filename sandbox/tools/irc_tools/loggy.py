#!/usr/bin/env python
"""
loggy.py - An IRC Logger
Author: Sean B. Palmer, inamidst.com
Source: http://inamidst.com/code/loggy.py
Cf. http://paste.lisp.org/display/28974
"""

import sys, re
import socket, asyncore, asynchat

class Origin(object): 
   source = re.compile(r'([^!]*)!?([^@]*)@?(.*)')

   def __init__(self, bot, source, args): 
      match = Origin.source.match(source or '')
      self.nick, self.user, self.host = match.groups()

      if len(args) > 1: 
         target = args[1]
      else: target = None

      mappings = {bot.nick: self.nick, None: None}
      self.sender = mappings.get(target, target)

class Bot(asynchat.async_chat): 
   line = re.compile(r'(?::([^ ]+) +)?((?:.(?! :))+.)(?: +:?(.*))?')

   def __init__(self, nick, channels=None): 
      asynchat.async_chat.__init__(self)
      self.set_terminator('\r\n')
      self.buffer = []

      self.nick = nick
      self.user = nick
      self.name = nick

      self.verbose = True
      self.channels = channels or []

   def run(self, host, port=6667): 
      if self.verbose: 
         message = "Connecting to %s:%s..." % (host, port)
         print >> sys.stderr, message,
      self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
      self.connect((host, port))
      asyncore.loop()

   def write(self, args, text=None): 
      if text is not None: 
         self.push(' '.join(args) + ' :' + text + '\r\n')
      else: self.push(' '.join(args) + '\r\n')

   def handle_connect(self): 
      if self.verbose: 
         print >> sys.stderr, "connected!"
      self.write(('NICK', self.nick))
      self.write(('USER', self.user, '+iw', self.nick), self.name)

   def collect_incoming_data(self, data): 
      self.buffer.append(data)

   def found_terminator(self): 
      match = Bot.line.match(''.join(self.buffer))
      self.buffer = []
      if not match: return

      source, argstr, text = match.groups()
      args = argstr.split()

      if args and (args[0] == 'PING'): 
         self.write(('PONG', text))
      elif args and (args[0] == '251'): 
         for channel in self.channels: 
            self.write(('JOIN', channel))

      origin = Origin(self, source, args)
      self.dispatch(origin, args, text)

   def dispatch(self, origin, args, text): 
      pass

   def filter(self, text): 
      return True

   def msg(self, recipient, text): 
      if isinstance(text, unicode): 
         try: text = text.encode('utf-8')
         except UnicodeEncodeError, e: 
            text = e.__class__ + ': ' + str(e)

      if self.filter(text): 
         self.write(('PRIVMSG', recipient), text)
      return text

import os, time

class Loggy(Bot): 
   def __init__(self, nick, channel): 
      Bot.__init__(self, nick, [channel])
      self.channel = channel
      self.offlog = '[off]'

   def logprivmsg(self, origin, command, channel, args, text): 
      if channel == self.channel: 
         if text.startswith('\x01ACTION ') and text.endswith('\x01'): 
            text = text[8:-1]
            if not text.startswith(self.offlog): 
               timestamp = self.log('* %s %s' % (origin.nick, text))
         elif not text.startswith(self.offlog): 
            timestamp = self.log('<%s> %s' % (origin.nick, text))

         if (text.startswith(self.nick + ': ') or 
             text.startswith(self.nick + ', ')): 
            request = text[len(self.nick) + 2:].rstrip('?!')

            if request in ('pointer', 'bookmark', 'uri'): 
               day = self.now('%Y-%m-%d')
               uri = self.loguri + day + '#T' + timestamp.replace(':', '-')
               self.msg(origin.sender, uri)

            elif request in ('ping', 'boing'): 
               reply = {'ping': 'pong', 'boing': 'boing!'}[request]
               self.msg(origin.sender, '%s: %s' % (origin.nick, reply))

            elif request in ('help', 'about'): 
               self.msg(origin.sender, 
                    ("I'm a Python IRC logging bot. " + 
                     "Source: http://inamidst.com/code/loggy.py " + 
                     "Logging to: " + self.loguri))

   def logjoin(self, origin, command, channel, args, text): 
      fargs = (origin.nick, origin.user, origin.host, self.channel)
      self.log('*** %s (%s@%s) has joined %s' % fargs)

   def logpart(self, origin, command, channel, args, text): 
      message = text
      msg = '*** %s has parted %s (%s)'
      self.log(msg % (origin.nick, self.channel, message))

   def logquit(self, origin, command, channel, args, text): 
      message = text
      self.log('*** %s has quit (%s)' % (origin.nick, message))

   def lognick(self, origin, command, channel, args, text): 
      old = origin.nick
      new = text
      self.log('*** %s is now known as %s' % (old, new))

   def logsettopic(self, origin, command, channel, args, text): 
      if args[1] == self.channel: 
         topic = text
         self.log('*** %s changed the topic to: "%s"' % (origin.nick, topic))

   def logtopic(self, origin, command, channel, args, text):
      topic = text
      channel = args[2]
      self.log('<%s> Topic for %s is: %s' % (origin.nick, channel, topic))

   def logusers(self, origin, command, channel, args, text): 
      users = text.strip(' ')
      # users = ' '.join(sorted(users.split(' ')))
      channel = args[3]
      self.log('<%s> Users on %s: %s' % (origin.nick, channel, users))

   def dispatch(self, origin, args, text): 
      if len(args) >= 2: 
         command, channel = args[0:2]
      elif len(args) >= 1: 
         command, channel = args[0], text
      else: command, channel = None, None

      commands = {
         'PRIVMSG': self.logprivmsg, 
         'JOIN': self.logjoin, 
         'PART': self.logpart, 
         'QUIT': self.logquit, 
         'NICK': self.lognick, 
         'TOPIC': self.logsettopic, 
         '332': self.logtopic, 
         '353': self.logusers
      }

      if commands.has_key(command): 
         commands[command](origin, command, channel, args, text)

   def msg(self, recipient, text): 
      text = Bot.msg(self, recipient, text)
      self.log('<%s> %s' % (self.nick, text))

   def log(self, line): 
      name = self.now('%Y-%m-%d.txt')
      logfile = os.path.join(self.logdir, name)

      try: 
         f = open(logfile, 'a')
         timenow = self.now('%H:%M:%S')
         print >> f, timenow, line
         f.close()
      except Exception, e: 
         print >> sys.stderr, str(e.__class__) + ': ' + str(e)

      return timenow

   def now(self, format): 
      offset = 0 # 131412
      return time.strftime(format, time.gmtime(time.time() + offset))

def main(): 
   usage = '%prog <nick> irc://<host>/<channel> <logdir> <loguri>'
   if len(sys.argv) != 5: 
      print 'Usage: ' + usage.replace('%prog', sys.argv[0])
      sys.exit()

   uri = sys.argv[2]
   scheme, _, host, channel = tuple(uri.split('/'))

   bot = Loggy(sys.argv[1], '#' + channel)
   bot.logdir = sys.argv[3]
   if not os.path.isdir(bot.logdir): 
      raise Exception("Not a directory: " + bot.logdir)
   bot.loguri = sys.argv[4]
   bot.run(host)

if __name__=="__main__": 
   main()
