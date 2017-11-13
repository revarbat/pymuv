#!/usr/bin/env python3

from __future__ import unicode_literals
from __future__ import print_function

import sys
import argparse

from pymuv.parsefile import MuvParser


def main():
    parser = argparse.ArgumentParser(prog='pymuv')
    parser.add_argument("-d", "--debug",
                        help="Add debugging code/markers to output MUF.",
                        action="store_true")
    parser.add_argument("-c", "--check",
                        help="Don't output code.  Just check for errors.",
                        action="store_true")
    parser.add_argument("-n", "--no-optimization",
                        help="Disable code optimization.",
                        action="store_true")
    parser.add_argument("-T", "--target", choices=['fb6', 'fb7'], default="fb6",
                        help="Target MUF variant. Currently one of 'fb6' or 'fb7'.")
    parser.add_argument("-w", "--wrapper", type=str, default="",
                        help="Wrap code for upload into given program.")
    parser.add_argument("-s", "--sysincludes-only",
                        help="Only allow system ! includes.",
                        action="store_true")
    parser.add_argument("-o", "--output", type=str, default="",
                        help="File to write MUF output to.")
    parser.add_argument('infile', help='Input MUV sourcecode file.')
    opts = parser.parse_args()

    muvparser = MuvParser(
        debug=opts.debug,
        target=opts.target,
        optim=(0 if opts.no_optimization else 1),
        sysonly=opts.sysincludes_only,
        wrapper=opts.wrapper,
    )
    muvparser.parse_file(opts.infile)

    if not opts.check:
        try:
            outstream = sys.stdout
            if opts.output:
                outstream = open(opts.output, "w")
            if not muvparser.error_found:
                print(muvparser.output, file=outstream)
        finally:
            if opts.output:
                outstream.close()
    sys.exit(-1 if muvparser.error_found else 0)


if __name__ == "__main__":
    main()


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
