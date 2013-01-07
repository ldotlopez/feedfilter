#!/usr/bin/env python

import sys
import optparse
import xml.dom.minidom as minidom

from filters.meneame import MeneameRewriteLink

def feedfilter(in_fh, out_fh, filters = ()):
    dom = minidom.parseString(in_fh.read())
    for f in filters:
        f.process(dom)

    out_fh.write(dom.toxml().encode('utf-8'))


if __name__ == '__main__':
    parser = optparse.OptionParser('Filter rss/atom/etc feeds')
    parser.add_option('-i', '--in', dest='input', metavar='INPUT',
                      action='store',
        help='Input filename or - for stdin')
    parser.add_option('-o', '--out', dest='output', metavar='OUTPUT',
                      action='store',
        help='Output filename or - for stdout')

    (options, args) = parser.parse_args(sys.argv[1:])
    _in  = options.input  or '-'
    _out = options.output or '-'

    in_fh  = open(_in) if _in != '-' else sys.stdin
    out_fh = open(_out, 'w+') if _out != '-' else sys.stdout

    feedfilter(in_fh, out_fh, (MeneameRewriteLink(),))

    out_fh.close()
