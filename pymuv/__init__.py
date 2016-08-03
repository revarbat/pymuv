#!/usr/bin/env python3

from __future__ import unicode_literals
from __future__ import print_function

import argparse

from pymuv.parsefile import MuvParser


def main():
    parser = argparse.ArgumentParser(prog='pymuv')
    parser.add_argument("-d", "--debug",
                        help="Add debugging code to output MUF.",
                        action="store_true")
    parser.add_argument("-I", "--include-dir", type=str, default="",
                        help="Specify directory to look for include files.")
    parser.add_argument("-o", "--output", type=str, default="",
                        help="File to write MUF output to.")
    parser.add_argument('infile', help='Input MUV sourcecode file.')
    opts = parser.parse_args()

    muvparser = MuvParser()
    muvparser.set_debug(opts.debug)
    muvparser.include_dir = opts.include_dir
    try:
        if opts.output:
            muvparser.output = open(opts.output, "w")
        muvparser.parse_file(opts.infile)
    finally:
        if opts.output:
            muvparser.output.close()


if __name__ == "__main__":
    main()


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
