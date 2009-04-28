import os
import sys
import optparse
import cascadenik
import tempfile
import mapnik

def main(file, dir):
    """ Given an input layers file and a directory, print the compiled
        XML file to stdout and save any encountered external image files
        to the named directory.
    """
    mmap = mapnik.Map(1, 1)
    cascadenik.load_map(mmap, file, dir)
    
    (handle, filename) = tempfile.mkstemp(suffix='.xml', prefix='cascadenik-mapnik-')
    os.close(handle)
    
    mapnik.save_map(mmap, filename)
    print open(filename, 'r').read()
    
    os.unlink(filename)
    return 0

parser = optparse.OptionParser(usage="""cascadenik-compile.py [options] <style file>""")

parser.add_option('-d', '--dir', dest='directory',
                  help='Write to output directory')

if __name__ == '__main__':
    (options, args) = parser.parse_args()

    if not args:
        parser.error('Please specify a .mml file')

    layersfile = args[0]

    if layersfile.endswith('.mss'):
        parser.error('Only accepts an .mml file')

    sys.exit(main(layersfile, options.directory))
