from pymuv.errors import MuvError


class LValue(object):
    def __init__(self, varname, indexing, pos, declare=False, readonly=False):
        self.varname = varname
        self.indexing = indexing
        self.declare = declare
        self.position = pos
        self.readonly = readonly

    def get_expr(self, ctx):
        """
        Returns the MUF needed to get the contents of the lvalue.
        Returned MUF will push the contained value onto the stack.
        """
        varname = ctx.lookup_variable(self.varname)
        if varname is None:
            val = ctx.lookup_constant(self.varname)
            if val:
                try:
                    return val.generate_code(ctx)
                except AttributeError:
                    return val
            raise MuvError(
                "Undeclared identifier '%s'." % self.varname,
                position=self.position
            )
        if len(self.indexing) == 0:
            return "{var} @".format(
                var=varname,
            )
        if len(self.indexing) == 1:
            return "{var} @ {idx} []".format(
                var=varname,
                idx=self.indexing[0],
            )
        return (
            "{var} @ {{ {idx} }}list array_nested_get".format(
                var=varname,
                idx=" ".join(str(x) for x in self.indexing),
            )
        )

    def set_expr(self, ctx):
        """
        Returns the MUF needed to do an assign on the lvalue. (=)
        Returned MUF expects a value to be on the stack.
        """
        if self.readonly:
            raise MuvError(
                "Cannot assign value to constant '%s'." % self.varname,
                position=self.position
            )
        if self.declare:
            varname = ctx.declare_variable(self.varname)
            if len(self.indexing) == 0:
                return "var! {var}".format(var=varname)
        else:
            varname = ctx.lookup_variable(self.varname)
            if varname is None:
                raise MuvError(
                    "Undeclared identifier '%s'." % self.varname,
                    position=self.position
                )
        if len(self.indexing) == 0:
            if ctx.assign_level > 1:
                return "dup {var} !".format(var=varname)
            else:
                return "{var} !".format(var=varname)
        if len(self.indexing) == 1:
            if ctx.assign_level > 1:
                fmt = "dup {var} @ {idx} ->[] {var} !"
            else:
                fmt = "{var} @ {idx} ->[] {var} !"
            return fmt.format(
                var=varname,
                idx=self.indexing[0].generate_code(ctx),
            )
        if ctx.assign_level > 1:
            fmt = "dup {var} @ {{ {idx} }}list array_nested_set {var} !"
        else:
            fmt = "{var} @ {{ {idx} }}list array_nested_set {var} !"
        return fmt.format(
            var=varname,
            idx=" ".join(x.generate_code(ctx) for x in self.indexing)
        )

    def oper_set_expr(self, ctx, oper, val):
        """
        Returns the MUF needed to do an oper-assign on the lvalue. (+=, etc.)
        """
        if self.readonly:
            raise MuvError(
                "Cannot assign value to constant '%s'." % self.varname,
                position=self.position
            )
        varname = ctx.lookup_variable(self.varname)
        if varname is None:
            raise MuvError(
                "Undeclared identifier '%s'." % self.varname,
                position=self.position
            )
        if len(self.indexing) == 0:
            if ctx.assign_level > 1:
                fmt = "{var} @ {val} {oper} dup {var} !"
            else:
                fmt = "{var} @ {val} {oper} {var} !"
            return fmt.format(
                var=varname,
                oper=oper,
                val=val.generate_code(ctx),
            )
        if len(self.indexing) == 1:
            if ctx.assign_level > 1:
                fmt = (
                    "{var} @ {idx} "
                    "over over [] {val} {oper} "
                    "dup -4 rotate "
                    "rot rot ->[] {var} !"
                )
            else:
                fmt = (
                    "{var} @ {idx} "
                    "over over [] {val} {oper} "
                    "rot rot ->[] {var} !"
                )
            return fmt.format(
                var=varname,
                oper=oper,
                val=val.generate_code(ctx),
                idx=self.indexing[0].generate_code(ctx),
            )
        if ctx.assign_level > 1:
            fmt = (
                "{var} @ {{ {idx} }}list "
                "over over array_nested_get {val} {oper} "
                "dup -4 rotate "
                "rot rot array_nested_set {var} !"
            )
        else:
            fmt = (
                "{var} @ {{ {idx} }}list "
                "over over array_nested_get {val} {oper} "
                "rot rot array_nested_set {var} !"
            )
        return fmt.format(
            var=varname,
            oper=oper,
            val=val.generate_code(ctx),
            idx=" ".join(
                x.generate_code(ctx)
                for x in self.indexing
            )
        )

    def unary_set_expr(self, ctx, oper, postoper=False):
        """
        Returns the MUF needed to do an unary operation on the lvalue. (++, --.)
        """
        if self.readonly:
            raise MuvError(
                "Cannot increment or decrement constant '%s'." % self.varname,
                position=self.position
            )
        varname = ctx.lookup_variable(self.varname)
        if varname is None:
            raise MuvError(
                "Undeclared identifier '%s'." % self.varname,
                position=self.position
            )
        if len(self.indexing) == 0:
            if postoper:
                fmt = "{var} @ {var} {oper}"
            else:
                fmt = "{var} dup {oper} @"
            return fmt.format(var=varname, oper=oper)
        if len(self.indexing) == 1:
            if postoper:
                fmt = (
                    "{idx} {var} @ "
                    "dup 3 pick [] "
                    "dup -4 rotate {oper} "
                    "swap rot ->[] {var} !"
                )
            else:
                fmt = (
                    "{idx} {var} @ "
                    "dup 3 pick [] {oper} "
                    "dup -4 rotate "
                    "swap rot ->[] {var} !"
                )
            return fmt.format(
                var=varname,
                oper=oper,
                idx=self.indexing[0].generate_code(ctx),
            )
        if postoper:
            fmt = (
                "{{ {idx} }}list {var} @ "
                "dup 3 pick array_nested_get "
                "dup -4 rotate {oper} "
                "swap rot array_nested_set {var} !"
            )
        else:
            fmt = (
                "{{ {idx} }}list {var} @ "
                "dup 3 pick array_nested_get {oper} "
                "dup -4 rotate "
                "swap rot array_nested_set {var} !"
            )
        return fmt.format(
            var=varname,
            oper=oper,
            idx=" ".join(
                x.generate_code(ctx)
                for x in self.indexing
            )
        )

    def del_expr(self, ctx):
        """
        Returns the MUF needed to delete a given lvalue. (ie: array item)
        Returned MUF will set a bare variable to 0, and will remove the
        given indexed item for an indexed array or dictionary.
        """
        if self.readonly:
            raise MuvError(
                "Cannot assign value to constant '%s'." % self.varname,
                position=self.position
            )
        varname = ctx.lookup_variable(self.varname)
        if varname is None:
            raise MuvError(
                "Undeclared identifier '%s'." % self.varname,
                position=self.position
            )
        if len(self.indexing) == 0:
            return "0 {var} !".format(var=varname)
        if len(self.indexing) == 1:
            return "{var} @ {idx} array_delitem {var} !".format(
                var=varname,
                idx=self.indexing[0].generate_code(ctx),
            )
        return "{var} @ {{ {idx} }}list array_nested_del {var} !".format(
            var=varname,
            idx=" ".join(x.generate_code(ctx) for x in self.indexing),
        )


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
