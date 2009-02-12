import os
import sys

try:
    import cairo
except ImportError:
    print 'Cairo not installed, skipping test.'
    sys.exit()

from mapnik import *

def read_pages(fn):
    # Poor man's PS parser.
    try:
        f = open(fn, 'r')
    except IOError:
        return -1
    for l in f:
        if not l.startswith('%'):
            # Headers done, and we did not see a '%%Pages'
            break
        if l.startswith('%%Pages:'):
            try:
                p = int(l.split()[1])
            except ValueError:
                return -1
    else:
        # In the unlikely event the file consists only of
        # headers except for a Pages header, if this happens
        # the Cairo installation is probably seriously broken.
        return -1
    return p

show_fn = 'show_test.ps'
no_show_fn = 'no_show_test.ps'

def test():
    m = Map(256, 256)
    s_show = cairo.PSSurface(show_fn, 256, 256)
    s_no_show = cairo.PSSurface(no_show_fn, 256, 256)
    print "Saving", show_fn
    render(m, s_show, True)
    print "Saving", no_show_fn
    render(m, s_no_show, False)

    # The second render should not have called
    # show_page(), if we draw something now on this
    # map it appears still on the first page; on
    # s_show it should appear on the second page.
    for s in [s_show, s_no_show]:
        ctx = cairo.Context(s)
        ctx.set_source_rgba(0, 0, 0, 1)
        ctx.set_line_width(3.0)
        ctx.move_to(128, 128)
        ctx.rel_line_to(256, 0)
        ctx.stroke()
        # Make sure it is written to file.
        s.finish()
    p_show = read_pages(show_fn)
    p_no_show = read_pages(no_show_fn)
    success = (p_show == 2 and p_no_show == 1)

    for f in [show_fn, no_show_fn]:
        if os.path.exists(f):
            print "Removing", f
            os.remove(f)

    print "======================================================="
    print "Status:",
    if success:
        print "SUCCESS"
    else:
        print "FAILED"
    print "======================================================="

    return success

if __name__ == "__main__":
    if not cairo.HAS_PS_SURFACE:
        print 'No PostScript support in Cairo'
        sys.exit(1)

    if test():
        sys.exit(0)
    else:
        sys.exit(1)
