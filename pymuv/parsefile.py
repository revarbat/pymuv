from __future__ import unicode_literals
from __future__ import print_function

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
        self.output = sys.stdout
        self.include_dir = None
        self.context = Context()

    def set_debug(self, val=True):
        self.context.debug = val

    def print_error(self, filename, line, col, msg):
        srclines = self.input_sources.split("\n")
        if filename:
            filename += " "
        else:
            filename = ""
        print(srclines[line-1], file=sys.stderr)
        print('%s^' % (' '*(col-1)), file=sys.stderr)
        print(
            "Error in %sline %d, col %d: %s" % (filename, line, col, msg),
            file=sys.stderr
        )

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

    def parse_string(self, src, grammar=program, filename=None):
        oldsrcs = self.input_sources
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
            return out
        except MuvError as e:
            line, col = parser.pos_to_linecol(e.position)
            self.print_error(filename, line, col, str(e))
            return None
        except NoMatch as e:
            line, col = parser.pos_to_linecol(e.position)
            expected = self.simplify_parse_error(e)
            self.print_error(filename, line, col, "Expected %s" % expected)
            return None
        finally:
            self.input_sources = oldsrcs
            self.context.parsers.pop()
            self.context.filenames.pop()

    def parse_file(self, infile):
        with open(infile) as f:
            src = f.read()
        out = self.parse_string(src, grammar=program, filename=infile)
        if out:
            print(out, file=self.output)

    def include_file(self, infile):
        self.context.scope_push()
        if infile.startswith('!'):
            infile = infile[1:]
            src = resource_string(__name__, "incls/%s" % infile)
            src = src.decode("utf-8", errors="strict")
        else:
            with open(infile) as f:
                src = f.read()
        try:
            out = self.parse_string(
                src, grammar=source_file, filename=infile)
            if out:
                print(out, file=self.output)
        finally:
            self.context.scope_pop()


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
