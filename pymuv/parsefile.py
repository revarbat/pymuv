from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
from pkg_resources import resource_string

from arpeggio import (
    ParserPython, visit_parse_tree, NoMatch,
)

from pymuv.grammar import program, source_file, comment
from pymuv.errors import MuvError
from pymuv.context import Context
from pymuv.visitor import MuvVisitor


class MuvParser(object):
    def __init__(self):
        self.input_sources = ''
        self.output = ''
        self.error_cb = None
        self.error_found = False
        self.context = Context()
        self.debug = False
        self.optimization_level = False
        self.sysincludes_only = False
        self.wrapper_program = None

    def set_debug(self, val=True):
        self.debug = val
        self.context.debug = val

    def print_error(self, filename, line, col, msg):
        self.error_found = True
        srclines = self.input_sources.split("\n")
        if filename:
            filename += " "
        else:
            filename = ""
        err = "Error in %sline %d, col %d: %s" % (
            filename, line, col, msg
        )
        if self.error_cb:
            self.error_cb(err)
        else:
            print(srclines[line-1], file=sys.stderr)
            print("%s^" % (' '*(col-1)), file=sys.stderr)
            print(err, file=sys.stderr)

    def simplify_parse_error(self, e):
        groups = {
            "end-of-file": ["EOF"],
            "string-delimiter": [
                '"', "'", '"""', "'''",
                'r"', "r'", 'r"""', "r'''",
            ],
            "identifier": [r'[a-zA-Z_][a-zA-Z_0-9]*'],
            "variable-declaration": ['var', 'const'],
            "global-statement": [
                'func', 'public', 'extern', 'namespace',
                'using', 'include'
            ],
            "$directive": [
                "$author", "$echo", "$error", "$include",
                "$language", "$libversion", "$note",
                "$pragma", "$version", "$warn",
            ],
            "comparator": [
                '==', '!(?!=)', '<', '>', '<=', '>=', 'in', 'eq'
            ],
            "expression": [
                '%(?!=)', '&(?![&=])', '(', ')', '-(?![=-])',
                '/(?![/*=])', '<(?![=<])', '<<(?!=)', '>(?![=>])',
                '>>(?!=)', '\*(?![/*=])', '\*\*(?!=)', '\+(?![=+])',
                '\|(?![|=])', '^(?![^=])',
                '+', '-', '*', '/', '%', '**',
                '<<', '>>', '&', '|', '^', '~',
                '++', '--', '.', '[', '?',
                '&&', '||', '^^', '!',
                '0b', '0o', '0d', '0x', '#',
                'top', 'push', 'del', 'fmtstring', 'muf',
                r'[01_]+', r'[0-7_]+', r'[0-9a-fA-F_]+',
                r'[0-9_]+(?![.eE])', r'[+-]?(\d+\.\d*|\d*\.\d+)',
                r'[+-]?(\d+\.\d*|\d*\.\d+|\d)[eE][+-]?[0-9]+',
            ],
            "assignment": [
                '=(?![=>])',
                '=', '+=', '-=', '*=', '/=', '%=',
                '**=', '<<=', '>>=', '&=', '|=', '^=',
            ],
        }
        unique_rules = {}
        for rule in e.rules:
            if rule.rule_name == "EOF":
                expect = "EOF"
            else:
                expect = rule.to_match
            found = False
            for group, pats in groups.items():
                if expect in pats:
                    expect = group
                    found = True
            if not found:
                expect = "'%s'" % expect
            unique_rules[expect] = 1
        expected = " or ".join(sorted(list(unique_rules.keys())))
        return expected

    def get_parse_line(self, pos):
        line, col = self.context.parsers[-1].pos_to_linecol(pos)
        return line

    def parse_string(self, src, grammar=program, filename=None):
        oldsrcs = self.input_sources
        self.context.optimization_level = self.optimization_level
        self.input_sources = src
        parser = ParserPython(
            grammar,
            comment_def=comment,
            skipws=True,
            reduce_tree=False,
            memoization=True,
            debug=False,
        )
        self.context.parsers.append(parser)
        self.context.filenames.append(filename)
        try:
            parse_tree = parser.parse(self.input_sources)
            visitor = MuvVisitor(debug=False)
            visitor.muvparser = self
            parse_tree = visit_parse_tree(parse_tree, visitor)
            out = parse_tree.generate_code(self.context)
            if self.error_found:
                return False
            if len(self.context.filenames) == 1:
                if self.context.filenames[-1]:
                    filetext = " from {0}".format(
                        self.context.filenames[-1]
                    )
                else:
                    filetext = ''
                self.output = (
                    "( Generated{0} by the MUV compiler. )\n"
                    "(   https://github.com/revarbat/pymuv )\n"
                    "{1}\n"
                ).format(filetext, self.output)
            self.output += out
            if not self.error_found and len(self.context.filenames) == 1:
                if self.wrapper_program:
                    self.output = (
                        "@program {0}\n"
                        "1 99999 d\n"
                        "1 i\n"
                        "{1}\n"
                        ".\n"
                        "c\n"
                        "q\n"
                    ).format(self.wrapper_program, self.output)
            return True
        except MuvError as e:
            line, col = parser.pos_to_linecol(e.position)
            self.print_error(filename, line, col, str(e))
            return False
        except NoMatch as e:
            line, col = parser.pos_to_linecol(e.position)
            expected = self.simplify_parse_error(e)
            self.print_error(filename, line, col, "Expected %s" % expected)
            return False
        finally:
            self.input_sources = oldsrcs
            self.context.parsers.pop()
            self.context.filenames.pop()

    def parse_file(self, infile):
        currdir = os.getcwd()
        indir, infile = os.path.split(os.path.realpath(infile))
        try:
            os.chdir(indir)
            with open(infile) as f:
                src = f.read()
            return self.parse_string(
                src,
                grammar=program,
                filename=infile
            )
        finally:
            os.chdir(currdir)

    def include_file(self, infile, pos):
        currdir = os.getcwd()
        self.context.scope_push()
        if infile.startswith('!'):
            infile = infile[1:]
            src = resource_string(__name__, "incls/%s" % infile)
            src = src.decode("utf-8", errors="strict")
        elif self.sysincludes_only:
            line, col = self.context.parsers[-1].pos_to_linecol(pos)
            filename = self.context.filenames[-1]
            self.print_error(
                filename, line, col,
                "Non-system (!) includes disallowed."
            )
            return False
        else:
            indir, infile = os.path.split(os.path.realpath(infile))
            os.chdir(indir)
            with open(infile) as f:
                src = f.read()
        try:
            return self.parse_string(
                src,
                grammar=source_file,
                filename=infile
            )
        finally:
            self.context.scope_pop()
            os.chdir(currdir)


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
