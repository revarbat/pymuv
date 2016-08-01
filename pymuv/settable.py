from __future__ import unicode_literals

from pymuv.errors import MuvError


class Settable(object):
    def __init__(self, *lvalues):
        self.settables = lvalues[1:-1]

    def get_expr(self, ctx):
        raise MuvError(
            "Cannot use tuple in right side expression.",
            position=self.settables[0].position
        )

    def set_expr(self, ctx):
        cnt = len(self.settables)
        out = "0 {cnt} [..] array_vals pop\n{exprs}".format(
            cnt=cnt-1,
            exprs=" ".join(
                x.set_expr(ctx)
                for x in reversed(list(self.settables))
            )
        )
        return out

    def oper_set_expr(self, ctx):
        raise MuvError(
            "Cannot use tuple in left side of operator-assignment expression.",
            position=self.settables[0].position
        )

    def del_expr(self, ctx):
        raise MuvError(
            "Cannot use tuple in del expression.",
            position=self.settables[0].position
        )


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
