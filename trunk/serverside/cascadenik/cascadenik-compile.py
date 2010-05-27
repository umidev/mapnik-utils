#!/usr/bin/env python
 
import sys
import optparse
import cascadenik

def main(file, dir, move_local_files, expand_only):
    """ Given an input layers file and a directory, print the compiled
        XML file to stdout and save any encountered external image files
        to the named directory.
    """
    print cascadenik.compile(file, dir=dir, move_local_files=False, expand_only=expand_only)
    return 0

parser = optparse.OptionParser(usage="""cascadenik-compile.py [options] <style file>""")

parser.add_option('-d', '--dir', dest='directory',
                  help='Write to output directory')

parser.add_option('-m', '--move', dest='move_local_files',
                  help='Move local files to --dir location in addition to remote resources')

parser.add_option('-e', '--expand_only', dest='expand_only', default=False, action="store_true",
                  help='Expand data sources and map includes only; for debug purposes')
                  
if __name__ == '__main__':
    (options, args) = parser.parse_args()
    if not args:
        parser.error('Please specify a .mml file')
    layersfile = args[0]
    if layersfile.endswith('.mss'):
        parser.error('Only accepts an .mml file')
    sys.exit(main(layersfile, options.directory, options.move_local_files, options.expand_only))
