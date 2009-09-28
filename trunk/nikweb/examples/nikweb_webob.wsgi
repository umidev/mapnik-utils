""" 
Example WSGI file for nikweb.
"""

# if nikweb is not on the pythonpath, add it here.
#import sys
#sys.path.append('/path/to/nikweb')

# define the path to your map definitions here
map_definitions_dir='/path/to/nikweb/examples'

# set up the WSGI app
from nikweb.http.webob_server import Nikweb
application = Nikweb(map_definitions_dir)
