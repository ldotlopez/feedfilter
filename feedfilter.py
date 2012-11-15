import sys
import argparse
import xml.dom.minidom as minidom

from filters.meneame import MeneameRewriteLink

def feedfilter(in_fh, out_fh, filters = ()):
    dom = minidom.parseString(in_fh.read())
    for f in filters:
        f.process(dom)

    out_fh.write(dom.toxml().encode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Filter rss/atom/etc feeds')
    parser.add_argument('-i', '--in', dest='input', metavar='INPUT',
        help='Input filename or - for stdin')
    parser.add_argument('-o', '--out', dest='output', metavar='OUTPUT',
        help='Output filename or - for stdout')

    args = parser.parse_args(sys.argv[1:])
    _out = args.output or '-'
    _in  = args.input  or '-'

    in_fh  = open(_in) if _in != '-' else sys.stdin
    out_fh = open(_out, 'w+') if _in != '-' else sys.stdout

    feedfilter(in_fh, out_fh, (MeneameRewriteLink(),))

    out_fh.close()
