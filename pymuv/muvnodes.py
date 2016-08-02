#######################################################################
# Syntactic classes
#######################################################################

import re
import textwrap

from pymuv.errors import MuvError


def str_or_expr(x, ctx):
    if isinstance(x, MuvNode):
        return x.generate_code(ctx)
    return x


class MuvNode(object):
    def __init__(self, typ, pos):
        self.typename = typ
        self.position = pos
        self.children = []

    def append(self, child):
        self.children.append(child)

    def generate_code(self, ctx):
        out = " ".join(
            child.generate_code(ctx) for child in self.children
        )
        return out

    def indent(self, txt, ind='    '):
        return "\n".join((ind + l if l else l) for l in txt.split('\n'))


class MuvNodeNull(MuvNode):
    def __init__(self, pos):
        super(MuvNodeNull, self).__init__("NULL", pos)

    def generate_code(self, ctx):
        return ''


class MuvNodeInteger(MuvNode):
    def __init__(self, pos, val):
        super(MuvNodeInteger, self).__init__("INTEGER", pos)
        self.value = val
        self.valtype = "integer"

    def generate_code(self, ctx):
        return str(self.value)


class MuvNodeFloat(MuvNode):
    def __init__(self, pos, val):
        super(MuvNodeFloat, self).__init__("FLOAT", pos)
        self.value = val
        self.valtype = "float"

    def generate_code(self, ctx):
        return str(self.value)


class MuvNodeString(MuvNode):
    def __init__(self, pos, val):
        super(MuvNodeString, self).__init__("STRING", pos)
        self.value = val
        self.valtype = "string"

    def generate_code(self, ctx):
        out = self.value.replace('\x5c', '\x5c\x5c')
        out = out.replace('"', '\x5c"')
        out = out.replace('\r', '\x5cr')
        out = out.replace('\n', '\x5cr')
        out = out.replace('\x1b', '\x5c[')
        return '"%s"' % out


class MuvNodeDbRef(MuvNode):
    def __init__(self, pos, val):
        super(MuvNodeDbRef, self).__init__("DBREF", pos)
        self.value = val
        self.valtype = "dbref"

    def generate_code(self, ctx):
        return "#%d" % self.value


class MuvNodeKeyValPair(MuvNode):
    def __init__(self, pos, key, val):
        super(MuvNodeKeyValPair, self).__init__("KEYVAL_PAIR", pos)
        self.key = key
        self.val = val

    def generate_code(self, ctx):
        return "{key} {val}".format(
            key=self.key.generate_code(ctx),
            val=self.val.generate_code(ctx),
        )


class MuvNodeGlobalVar(MuvNode):
    def __init__(self, pos, name, initval=None):
        super(MuvNodeGlobalVar, self).__init__("GLOBAL_VAR", pos)
        self.name = name
        self.initval = initval

    def generate_code(self, ctx):
        realname = ctx.declare_global_var(self.name)
        if self.initval is not None:
            ctx.add_init(
                "{expr} {var} !".format(
                    expr=self.initval.generate_code(ctx),
                    var=realname
                )
            )
        return 'lvar %s' % realname


class MuvNodeGlobalConst(MuvNode):
    def __init__(self, pos, name, value):
        super(MuvNodeGlobalConst, self).__init__("GLOBAL_CONST", pos)
        self.name = name
        self.value = value

    def generate_code(self, ctx):
        ctx.declare_global_const(self.name, self.value)
        return ''


class MuvNodeFuncConst(MuvNode):
    def __init__(self, pos, name, value):
        super(MuvNodeFuncConst, self).__init__("FUNC_CONST", pos)
        self.name = name
        self.value = value

    def generate_code(self, ctx):
        ctx.declare_constant(self.name, self.value)
        return ''


class MuvNodeFuncVar(MuvNode):
    def __init__(self, pos, name):
        super(MuvNodeFuncVar, self).__init__("FUNC_VAR", pos)
        self.name = name

    def generate_code(self, ctx):
        realname = ctx.declare_variable(self.name)
        return "var {var}".format(var=realname)


class MuvNodeVarFetch(MuvNode):
    def __init__(self, pos, var):
        super(MuvNodeVarFetch, self).__init__("VAR_FETCH", pos)
        self.var = var

    def generate_code(self, ctx):
        return self.var.get_expr(ctx)


class MuvNodeVarAssign(MuvNode):
    def __init__(self, pos, var, expr):
        super(MuvNodeVarAssign, self).__init__("VAR_ASSIGN", pos)
        self.var = var
        self.expr = expr

    def generate_code(self, ctx):
        ctx.assign_level += 1
        out = "{expr} {setexp}".format(
            expr=self.expr.generate_code(ctx),
            setexp=self.var.set_expr(ctx),
        )
        ctx.assign_level -= 1
        return out


class MuvNodeVarOperAssign(MuvNode):
    def __init__(self, pos, var, oper, expr):
        super(MuvNodeVarOperAssign, self).__init__("VAR_OPER_ASSIGN", pos)
        self.var = var
        self.oper = oper
        self.expr = expr

    def generate_code(self, ctx):
        ctx.assign_level += 1
        out = self.var.oper_set_expr(ctx, self.oper, self.expr)
        ctx.assign_level -= 1
        return out


class MuvNodeVarDel(MuvNode):
    def __init__(self, pos, var):
        super(MuvNodeVarDel, self).__init__("VAR_DEL", pos)
        self.var = var

    def generate_code(self, ctx):
        return self.var.del_expr(ctx)


class MuvNodePostfixExpr(MuvNode):
    def __init__(self, pos, expr, oper):
        super(MuvNodePostfixExpr, self).__init__("POSTFIX_EXPR", pos)
        self.expr = expr
        self.oper = oper

    def generate_code(self, ctx):
        if isinstance(self.expr, MuvNodeVarFetch):
            lval = self.expr.var
            ctx.assign_level += 1
            out = lval.unary_set_expr(ctx, self.oper, postoper=True)
            ctx.assign_level -= 1
            return out
        return "{expr} {oper}".format(
            expr=self.expr.generate_code(ctx),
            oper=self.oper,
        )


class MuvNodePrefixExpr(MuvNode):
    def __init__(self, pos, oper, expr):
        super(MuvNodePrefixExpr, self).__init__("PREFIX_EXPR", pos)
        self.oper = oper
        self.expr = expr

    def generate_code(self, ctx):
        if self.oper in ['+', '-']:
            return "0 {expr} {oper}".format(
                expr=self.expr.generate_code(ctx),
                oper=self.oper,
            )
        if isinstance(self.expr, MuvNodeVarFetch):
            lval = self.expr.var
            ctx.assign_level += 1
            out = lval.unary_set_expr(ctx, self.oper)
            ctx.assign_level -= 1
            return out
        return "{expr} {oper}".format(
            expr=self.expr.generate_code(ctx),
            oper=self.oper,
        )


class MuvNodeBinaryExpr(MuvNode):
    def __init__(self, pos, expr1, oper, expr2):
        super(MuvNodeBinaryExpr, self).__init__("BINARY_EXPR", pos)
        self.expr1 = expr1
        self.oper = oper
        self.expr2 = expr2

    def generate_code(self, ctx):
        ctx.assign_level += 1
        out = "{expr1} {expr2} {oper}".format(
            expr1=self.expr1.generate_code(ctx),
            oper=self.oper,
            expr2=self.expr2.generate_code(ctx),
        )
        ctx.assign_level -= 1
        return out


class MuvNodeLogicalOr(MuvNode):
    def __init__(self, pos, expr1, expr2):
        super(MuvNodeLogicalOr, self).__init__("OR", pos)
        self.expr1 = expr1
        self.expr2 = expr2

    def generate_code(self, ctx):
        return (
            "{expr1} dup not if pop\n"
            "{expr2}\n"
            "then"
        ).format(
            expr1=self.expr1.generate_code(ctx),
            expr2=self.indent(self.expr2.generate_code(ctx)),
        )


class MuvNodeLogicalAnd(MuvNode):
    def __init__(self, pos, expr1, expr2):
        super(MuvNodeLogicalAnd, self).__init__("AND", pos)
        self.expr1 = expr1
        self.expr2 = expr2

    def generate_code(self, ctx):
        return (
            "{expr1} dup if pop\n"
            "{expr2}\n"
            "then"
        ).format(
            expr1=self.expr1.generate_code(ctx),
            expr2=self.indent(self.expr2.generate_code(ctx)),
        )


class MuvNodeExprList(MuvNode):
    def __init__(self, pos, *children):
        super(MuvNodeExprList, self).__init__("STATEMENTS", pos)
        self.children = list(children)

    def generate_code(self, ctx):
        return " ".join(
            str_or_expr(child, ctx) for child in self.children
        )


class MuvNodeStatements(MuvNode):
    def __init__(self, pos, *children):
        super(MuvNodeStatements, self).__init__("STATEMENTS", pos)
        self.children = []
        for child in children:
            if isinstance(child, MuvNodeStatements):
                for subchild in child.children:
                    self.children.append(subchild)
            else:
                self.children.append(child)

    def generate_code(self, ctx):
        ctx.scope_push()
        statements = [
            str_or_expr(child, ctx)
            for child in self.children
        ]
        out = "\n".join(x for x in statements if x)
        ctx.scope_pop()
        return out


class MuvNodeCommand(MuvNode):
    def __init__(self, pos, cmd, *children):
        super(MuvNodeCommand, self).__init__("COMMAND", pos)
        self.command = cmd
        self.children = children

    def generate_code(self, ctx):
        ctx.assign_level += 1
        outlist = [child.generate_code(ctx) for child in self.children]
        outlist.append(self.command)
        out = " ".join(x for x in outlist if x)
        ctx.assign_level -= 1
        return out


class MuvNodeWrappedExpr(MuvNode):
    def __init__(self, pos, pfx, sfx, *children):
        super(MuvNodeWrappedExpr, self).__init__("WRAPPED", pos)
        self.prefix = pfx
        self.suffix = sfx
        self.children = children

    def generate_code(self, ctx):
        return "{pfx} {infix}{sfx}".format(
            pfx=self.prefix,
            sfx=self.suffix,
            infix="".join(
                "%s " % x.generate_code(ctx)
                for x in self.children
            ),
        )


class MuvNodeIfElse(MuvNode):
    def __init__(
            self, pos,
            cond=None,
            ifclause=None,
            elseclause=None
    ):
        super(MuvNodeIfElse, self).__init__("IF", pos)
        self.conditional = cond
        self.ifclause = ifclause
        self.elseclause = elseclause

    def generate_code(self, ctx):
        ctx.scope_push()
        if self.elseclause:
            out = (
                "{cond} if\n"
                "{body}\n"
                "else\n"
                "{els}\n"
                "then"
            ).format(
                cond=self.conditional.generate_code(ctx),
                body=self.indent(self.ifclause.generate_code(ctx)),
                els=self.indent(self.elseclause.generate_code(ctx)),
            )
        else:
            out = (
                "{cond} if\n"
                "{body}\n"
                "then"
            ).format(
                cond=self.conditional.generate_code(ctx),
                body=self.indent(self.ifclause.generate_code(ctx)),
            )
        ctx.scope_pop()
        return out


class MuvNodeForLoop(MuvNode):
    def __init__(
            self, pos,
            var=None,
            start=None,
            end=None,
            stride=None,
            body=None
            ):
        super(MuvNodeForLoop, self).__init__("FOR", pos)
        self.var = var
        self.start = start
        self.end = end
        self.stride = stride

    def generate_code(self, ctx):
        ctx.scope_push()
        out = (
            "{start} {end} {stride} for\n"
            "{vexp}\n"
            "{body}\n"
            "repeat"
        ).format(
            start=self.start.generate_code(ctx),
            end=self.end.generate_code(ctx),
            stride=self.stride.generate_code(ctx),
            vexp=self.indent(self.var.set_expr(ctx)),
            body=self.indent(self.body.generate_code(ctx)),
        )
        ctx.scope_pop()
        return out


class MuvNodeForEachLoop(MuvNode):
    def __init__(self, pos, expr=None, keyvar=None, valvar=None, body=None):
        super(MuvNodeForEachLoop, self).__init__("FOREACH", pos)
        self.expr = expr
        self.keyvar = keyvar
        self.valvar = valvar
        self.body = body

    def generate_code(self, ctx):
        ctx.scope_push()
        out = (
            "{expr} foreach\n"
            "{vset} {kset}\n"
            "{body}\n"
            "repeat"
        ).format(
            expr=self.expr.generate_code(ctx),
            vset=self.indent(self.valvar.set_expr(ctx)),
            kset=self.keyvar.set_expr(ctx) if self.keyvar else "pop",
            body=self.indent(self.body.generate_code(ctx)),
        )
        ctx.scope_pop()
        return out


class MuvNodeWhile(MuvNode):
    def __init__(self, pos, cond=None, body=None):
        super(MuvNodeWhile, self).__init__("WHILE", pos)
        self.conditional = cond
        self.body = body

    def generate_code(self, ctx):
        ctx.scope_push()
        out = (
            "begin\n"
            "{cond}\n"
            "while\n"
            "{body}\n"
            "repeat"
        ).format(
            cond=self.indent(self.conditional.generate_code(ctx)),
            body=self.indent(self.body.generate_code(ctx)),
        )
        ctx.scope_pop()
        return out


class MuvNodeUntil(MuvNode):
    def __init__(self, pos, cond=None, body=None):
        super(MuvNodeUntil, self).__init__("UNTIL", pos)
        self.conditional = cond
        self.body = body

    def generate_code(self, ctx):
        ctx.scope_push()
        out = (
            "begin\n"
            "{cond} not\n"
            "while\n"
            "{body}\n"
            "repeat"
        ).format(
            cond=self.indent(self.conditional.generate_code(ctx)),
            body=self.indent(self.body.generate_code(ctx)),
        )
        ctx.scope_pop()
        return out


class MuvNodeDoWhile(MuvNode):
    def __init__(self, pos, body=None, cond=None):
        super(MuvNodeDoWhile, self).__init__("DO_WHILE", pos)
        self.body = body
        self.conditional = cond

    def generate_code(self, ctx):
        ctx.scope_push()
        out = (
            "begin\n"
            "{body}\n"
            "{cond} not\n"
            "until"
        ).format(
            cond=self.indent(self.conditional.generate_code(ctx)),
            body=self.indent(self.body.generate_code(ctx)),
        )
        ctx.scope_pop()
        return out


class MuvNodeDoUntil(MuvNode):
    def __init__(self, pos, body=None, cond=None):
        super(MuvNodeDoUntil, self).__init__("DO_UNTIL", pos)
        self.body = body
        self.conditional = cond

    def generate_code(self, ctx):
        ctx.scope_push()
        out = (
            "begin\n"
            "{body}\n"
            "{cond}\n"
            "until"
        ).format(
            cond=self.indent(self.conditional.generate_code(ctx)),
            body=self.indent(self.body.generate_code(ctx)),
        )
        ctx.scope_pop()
        return out


class MuvNodeSwitch(MuvNode):
    def __init__(self, pos, expr=None, var=None, cases=[]):
        super(MuvNodeSwitch, self).__init__("SWITCH", pos)
        self.expr = expr
        self.var = var
        self.children = cases

    def generate_code(self, ctx):
        ctx.scope_push()
        out = (
            "{expr} {setexp}\n"
            "begin\n"
            "{cases}\n"
            "repeat"
        ).format(
            expr=self.expr.generate_code(ctx),
            setexp=self.var.set_expr(ctx),
            cases=self.indent(
                "\n".join(
                    case.generate_code(ctx) for case in self.children
                )
            )
        )
        ctx.scope_pop()
        return out


class MuvNodeTryCatch(MuvNode):
    def __init__(self, pos, body, handler, var=None):
        super(MuvNodeTryCatch, self).__init__("TRY_CATCH", pos)
        self.body = body
        self.handler = handler
        self.settable = var

    def generate_code(self, ctx):
        ctx.scope_push()
        vexp = self.settable.set_expr(ctx) if self.settable else "pop"
        out = (
            "0 try\n"
            "{body}\n"
            "catch_detailed {vexp}\n"
            "{handler}\n"
            "endcatch"
        ).format(
            body=self.indent(self.body.generate_code(ctx)),
            handler=self.indent(self.handler.generate_code(ctx)),
            vexp=vexp,
        )
        ctx.scope_pop()
        return out


class MuvNodeNamespace(MuvNode):
    def __init__(self, pos, namespace, body):
        super(MuvNodeNamespace, self).__init__("NAMESPACE", pos)
        self.namespace = namespace
        self.body = body

    def generate_code(self, ctx):
        curr_ns = ctx.curr_namespace
        ctx.set_namespace(self.namespace)
        bodyparts = [
            item.generate_code(ctx)
            for item in self.body
        ]
        out = "\n".join(x for x in bodyparts if x)
        ctx.set_namespace(curr_ns)
        return out


class MuvNodeUsingNamespace(MuvNode):
    def __init__(self, pos, namespace):
        super(MuvNodeUsingNamespace, self).__init__("USING_NS", pos)
        self.namespace = namespace

    def generate_code(self, ctx):
        ctx.use_namespace(self.namespace)
        return ''


class MuvNodeExtern(MuvNode):
    def __init__(
                self, pos, extern,
                argcount=0,
                retcount=1,
                varargs=False,
                code=None
            ):
        super(MuvNodeExtern, self).__init__("NAMESPACE", pos)
        self.extern = extern
        self.argcount = argcount
        self.retcount = retcount
        self.varargs = varargs
        self.code = textwrap.dedent(code) if code else extern

    def generate_code(self, ctx):
        ctx.declare_function(
            self.extern,
            self.argcount,
            varargs=self.varargs,
            retcount=self.retcount,
            is_extern=True,
            code=self.code,
        )
        return ''


class MuvNodeFuncDef(MuvNode):
    def __init__(
                self, pos,
                funcname=None,
                args=[],
                body=None,
                varargs=False,
                public=False,
            ):
        super(MuvNodeFuncDef, self).__init__("FUNC_DEF", pos)
        self.funcname = funcname
        self.args = args
        self.public = public
        self.varargs = varargs
        if body and type(body) in [MuvNodeStatements, MuvNodeExprList]:
            last = body.children[-1]
            if not isinstance(last, MuvNodeCommand) or last.command != "exit":
                body.append(
                    MuvNodeCommand(
                        last.position, "exit",
                        MuvNodeInteger(last.position, 0)
                    )
                )
        last = body
        while last and type(last) in [MuvNodeStatements, MuvNodeExprList]:
            last = last.children[-1]
        if isinstance(last, MuvNodeCommand):
            last.command = ''
        self.body = body

    def generate_code(self, ctx):
        ctx.scope_push()
        actual = ctx.declare_function(
            self.funcname,
            len(self.args),
            varargs=self.varargs,
            is_public=self.public,
        )
        self.last_function = actual
        args = "".join(
            "%s " % ctx.declare_variable(v)
            for v in self.args
        )
        fmt = (
            ": {funcname}[ {args}-- ret ]\n"
            "{body}\n"
            ";"
        )
        if self.public:
            fmt += (
                "\npublic {funcname}"
                "\n$libdef {funcname}"
            )
        out = fmt.format(
            funcname=actual,
            args=args,
            body=self.indent(self.body.generate_code(ctx)),
        )
        ctx.scope_pop()
        ctx.reset_function_local_data()
        return out


class MuvNodeFuncAddr(MuvNode):
    def __init__(self, pos, funcname=None, args=[]):
        super(MuvNodeFuncAddr, self).__init__("FUNC_ADDR", pos)
        self.funcname = funcname

    def generate_code(self, ctx):
        finfo = ctx.lookup_function(self.funcname)
        if not finfo:
            raise MuvError(
                "function '{funcname}' not found.".format(
                    funcname=self.funcname,
                ),
                position=self.position,
            )
        if finfo.is_extern:
            raise MuvError(
                "Cannot get address of extern '{funcname}'.".format(
                    funcname=self.funcname,
                ),
                position=self.position,
            )
        out = "'{func}".format(func=finfo.code)
        return out


class MuvNodeIndex(MuvNode):
    def __init__(self, pos, expr=None, idx=None):
        super(MuvNodeIndex, self).__init__("INDEX", pos)
        self.expr = expr
        self.idx = idx

    def generate_code(self, ctx):
        out = "{expr} {idx} []".format(
            expr=self.expr.generate_code(ctx),
            idx=self.idx.generate_code(ctx),
        )
        return out


class MuvNodeAddrCall(MuvNode):
    def __init__(self, pos, expr=None, args=[]):
        super(MuvNodeAddrCall, self).__init__("ADDR_CALL", pos)
        self.expr = expr
        self.args = args

    def generate_code(self, ctx):
        args = [x.generate_code(ctx) for x in self.args]
        out = "{args}{expr} execute".format(
            args="".join("%s " % x for x in args if x),
            expr=self.expr.generate_code(ctx),
        )
        return out


class MuvNodeFuncCall(MuvNode):
    def __init__(self, pos, funcname=None, args=[]):
        super(MuvNodeFuncCall, self).__init__("FUNC_CALL", pos)
        self.funcname = funcname
        self.args = args

    def generate_code(self, ctx):
        finfo = ctx.lookup_function(self.funcname)
        if not finfo:
            raise MuvError(
                "function '{funcname}' not found.".format(
                    funcname=self.funcname,
                ),
                position=self.position,
            )
        expected = finfo.argcount
        foundcnt = len(self.args)
        ftype = "extern" if finfo.is_extern else "function"
        if finfo.varargs:
            expected -= 1
            if foundcnt < expected:
                raise MuvError(
                    "{ftype} '{funcname}' expected at least {exp} "
                    "argument(s), but found only {found}.".format(
                        funcname=self.funcname,
                        exp=expected,
                        found=foundcnt,
                        ftype=ftype
                    ),
                    position=self.position,
                )
        elif foundcnt != expected:
            raise MuvError(
                "{ftype} '{funcname}' expected {expected} argument(s), "
                "but found {found}.".format(
                    funcname=self.funcname,
                    expected=expected,
                    found=foundcnt,
                    ftype=ftype
                ),
                position=self.position,
            )
        args = []
        for arg in self.args[:expected]:
            args.append(arg.generate_code(ctx))
        if finfo.varargs:
            args.append(
                "{ %s}list" % "".join(
                    "%s " % x.generate_code(ctx)
                    for x in self.args[expected:]
                )
            )
        out = "{args}{cmd}".format(
            args="".join("%s " % x for x in args),
            cmd=finfo.code,
        )
        if finfo.retcount == 0:
            out += " 0"
        elif finfo.retcount > 1:
            out = "{ %s }list" % out
        return out


class MuvNodeProgram(MuvNode):
    def __init__(self, pos, *children):
        super(MuvNodeProgram, self).__init__("PROGRAM", pos)
        self.children = list(children)

    def generate_code(self, ctx):
        children = [
            child.generate_code(ctx)
            for child in self.children
        ]
        out = "\n".join(x for x in children if x)
        replacements = [
            (r' swap swap', r''),
            (r' 0 pop', r''),
            (r'swap \+', r'+'),
            (r'swap \*', r'*'),
            (r'swap bitor', r'bitor'),
            (r'swap bitxor', r'bitxor'),
            (r'swap bitand', r'bitand'),
            (r'(\w+) @ \1 (\+\+|--) pop', r'\1 \2'),
        ]
        for pat, repl in replacements:
            out = re.sub(pat, repl, out)
        return out


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
