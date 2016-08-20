#######################################################################
# Visitor translation class
#######################################################################


from __future__ import unicode_literals
from __future__ import print_function

import re

from arpeggio import PTNodeVisitor
from pymuv.errors import MuvError
from pymuv.lvalue import LValue
from pymuv.settable import Settable
import pymuv.muvnodes as mn


class MuvVisitor(PTNodeVisitor):
    def __init__(self, *args, **kwargs):
        super(MuvVisitor, self).__init__(*args, **kwargs)

    def indent(self, txt, ind='    '):
        return "\n".join((ind + l if l else l) for l in txt.split('\n'))

    def left_associate_tree(self, arr):
        out = arr[0]
        arr = arr[1:]
        while len(arr) > 1:
            oper, expr = arr[:2]
            arr = arr[2:]
            out = mn.MuvNodeBinaryExpr(expr.position, out, oper, expr)
        return out

    def visit_ows(self, node, children):
        return None

    def visit_ws(self, node, children):
        return None

    def visit_SEMICOLON(self, node, children):
        return None

    def visit_kwend(self, node, children):
        return None

    def visit_numsign(self, node, children):
        if str(children[0]) == "-":
            return "-"
        return None

    def visit_bin_integer(self, node, children):
        chars = children[0].replace('_', '')
        val = 0
        for ch in chars:
            val *= 2
            val += int(ch)
        return mn.MuvNodeInteger(node.position, val)

    def visit_oct_integer(self, node, children):
        chars = children[0].replace('_', '')
        val = 0
        for ch in chars:
            val *= 8
            val += int(ch)
        return mn.MuvNodeInteger(node.position, val)

    def visit_dec_integer(self, node, children):
        chars = children[-1].replace('_', '')
        val = 0
        for ch in chars:
            val *= 10
            val += int(ch)
        return mn.MuvNodeInteger(node.position, val)

    def visit_hex_integer(self, node, children):
        chars = children[0].replace('_', '')
        val = 0
        for ch in chars:
            val *= 16
            val += "0123456789abcdef".index(str(ch).lower())
        return mn.MuvNodeInteger(node.position, val)

    def visit_unsigned_integer(self, node, children):
        return children[0]

    def visit_intnum(self, node, children):
        val = children[-1]
        if children[0] == "-":
            val.value *= -1
        return val

    def visit_raw_dquote_string(self, node, children):
        return children[0][2:-1]

    def visit_raw_squote_string(self, node, children):
        return children[0][2:-1]

    def visit_raw_dquote3_string(self, node, children):
        return children[0][4:-3]

    def visit_raw_squote3_string(self, node, children):
        return children[0][4:-3]

    def visit_dquote_string(self, node, children):
        return children[0][1:-1]

    def visit_squote_string(self, node, children):
        return children[0][1:-1]

    def visit_dquote3_string(self, node, children):
        return children[0][3:-3]

    def visit_squote3_string(self, node, children):
        return children[0][3:-3]

    def decode_string(self, txt):
        out = ''
        while txt:
            if '\\' not in txt:
                out += txt
                break
            pre, txt = txt.split('\\', 1)
            out += pre
            ch = txt[0]
            txt = txt[1:]
            if ch == '\n':
                continue
            elif ch == 'r' or ch == 'n':
                ch = '\r'
            elif ch == 'e' or ch == '[':
                ch = '\033'
            out += ch
        return out

    def visit_raw_string_literal(self, node, children):
        return children[0]

    def visit_esc_string_literal(self, node, children):
        return self.decode_string(children[0])

    def visit_string_literal(self, node, children):
        return mn.MuvNodeString(node.position, children[0])

    def visit_dbref(self, node, children):
        return mn.MuvNodeDbRef(node.position, children[0].value)

    def visit_floatnum(self, node, children):
        res = float("".join(children))
        return mn.MuvNodeFloat(node.position, res)

    def visit_OPER_INCR(self, node, children):
        return "++"

    def visit_OPER_DECR(self, node, children):
        return "--"

    def visit_OPER_PLUS(self, node, children):
        return "+"

    def visit_OPER_MINUS(self, node, children):
        return "-"

    def visit_OPER_MULT(self, node, children):
        return "*"

    def visit_OPER_DIV(self, node, children):
        return "/"

    def visit_OPER_MOD(self, node, children):
        return "%"

    def visit_OPER_POWER(self, node, children):
        return "pow"

    def visit_OPER_BITLEFT(self, node, children):
        return "bitshift"

    def visit_OPER_BITRIGHT(self, node, children):
        return "-1 * bitshift"

    def visit_OPER_BITAND(self, node, children):
        return "bitand"

    def visit_OPER_BITOR(self, node, children):
        return "bitor"

    def visit_OPER_BITXOR(self, node, children):
        return "bitxor"

    def visit_OPER_BITNOT(self, node, children):
        return "-1 bitxor"

    def visit_ASGN_PLUS(self, node, children):
        return "+"

    def visit_ASGN_MINUS(self, node, children):
        return "-"

    def visit_ASGN_MULT(self, node, children):
        return "*"

    def visit_ASGN_DIV(self, node, children):
        return "/"

    def visit_ASGN_MOD(self, node, children):
        return "%"

    def visit_ASGN_POWER(self, node, children):
        return "pow"

    def visit_ASGN_BITLEFT(self, node, children):
        return "bitshift"

    def visit_ASGN_BITRIGHT(self, node, children):
        return "-1 * bitshift"

    def visit_ASGN_BITAND(self, node, children):
        return "bitand"

    def visit_ASGN_BITOR(self, node, children):
        return "bitor"

    def visit_ASGN_BITXOR(self, node, children):
        return "bitxor"

    def visit_COMP_LT(self, node, children):
        return "<"

    def visit_COMP_GT(self, node, children):
        return ">"

    def visit_COMP_LTE(self, node, children):
        return "<="

    def visit_COMP_GTE(self, node, children):
        return ">="

    def visit_COMP_EQ(self, node, children):
        return "="

    def visit_COMP_NEQ(self, node, children):
        return "= not"

    def visit_COMP_STREQ(self, node, children):
        return "strcmp not"

    def visit_COMP_IN(self, node, children):
        return "swap array_findval"

    def visit_LOGICAL_AND(self, node, children):
        return None

    def visit_LOGICAL_OR(self, node, children):
        return None

    def visit_LOGICAL_XOR(self, node, children):
        return "xor"

    def visit_LOGICAL_NOT(self, node, children):
        return "not"

    def visit_paren_expr(self, node, children):
        return children[0]

    def visit_tuple_parts(self, node, children):
        return Settable(*children)

    def visit_settable(self, node, children):
        return children[0]

    def visit_declared_lvalue(self, node, children):
        varname = str(children[0])
        return LValue(varname, [], node.position, declare=True)

    def visit_indexed_lvalue(self, node, children):
        varname = str(children[0])
        indexing = children[1:]
        return LValue(varname, indexing, node.position)

    def visit_lvalue(self, node, children):
        return children[0]

    def visit_leaf_variable(self, node, children):
        varname = "".join(children)
        return mn.MuvNodeVarFetch(
            node.position,
            LValue(varname, [], node.position)
        )

    def visit_variable(self, node, children):
        return children[0]

    def visit_for_expr(self, node, children):
        stride = mn.MuvNodeInteger(node.position, 1)
        if len(children) > 3:
            lvalue, start, end, stride = children
        else:
            lvalue, start, end = children
        return mn.MuvNodeForLoop(
            node.position,
            var=lvalue,
            start=start,
            end=end,
            stride=stride,
        )

    def visit_foreach_expr(self, node, children):
        if len(children) > 2:
            keysettable, valsettable, expr = children
        else:
            valsettable, expr = children
            keysettable = None
        return mn.MuvNodeForEachLoop(
            node.position,
            expr=expr,
            keyvar=keysettable,
            valvar=valsettable,
        )

    def visit_compr_for(self, node, children):
        return children[0]

    def visit_compr_cond_if(self, node, children):
        return mn.MuvNodeIfElse(children[0].position, cond=children[0])

    def visit_compr_cond_unless(self, node, children):
        return mn.MuvNodeIfElse(
            children[0].position,
            cond=mn.MuvNodeCommand(children[0].position, 'not', children[0])
        )

    def visit_compr_cond(self, node, children):
        return children[0]

    def visit_keyval_pair(self, node, children):
        return mn.MuvNodeKeyValPair(node.position, children[0], children[1])

    def visit_dictlist(self, node, children):
        return children

    def visit_dict_initialization(self, node, children):
        vals = []
        if children:
            vals = children[0]
            if vals == ['=>']:
                vals = []
        return mn.MuvNodeWrappedExpr(
            node.position,
            "{", "}dict",
            *vals
        )

    def visit_list_initialization(self, node, children):
        vals = []
        if children:
            vals = children[0]
        return mn.MuvNodeWrappedExpr(
            node.position,
            "{", "}list",
            *vals
        )

    def visit_dict_comprehension(self, node, children):
        cond = None
        if len(children) > 2:
            loop, cond, body = children
        else:
            loop, body = children
        body = mn.MuvNodeCommand(body.position, "rot rot ->[]", body)
        if cond:
            cond.ifclause = body
            body = cond
        loop.body = body
        return mn.MuvNodeExprList(node.position, "{ }dict", loop)

    def visit_list_comprehension(self, node, children):
        cond = None
        if len(children) > 2:
            loop, cond, body = children
        else:
            loop, body = children
        body = mn.MuvNodeCommand(body.position, "swap []<-", body)
        if cond:
            cond.ifclause = body
            body = cond
        loop.body = body
        return mn.MuvNodeExprList(node.position, "{ }list", loop)

    def visit_comprehension(self, node, children):
        return children[0]

    def visit_leaf_expr(self, node, children):
        return children[0]

    def visit_attribute(self, node, children):
        attr = str(children[0])
        return mn.MuvNodeString(node.position, attr)

    def visit_index_part(self, node, children):
        return children[0]

    def visit_index_oper(self, node, children):
        idx = children[0]
        out = mn.MuvNodeIndex(node.position, idx=idx)
        return out

    def visit_addrcall_oper(self, node, children):
        args = children[0]
        out = mn.MuvNodeAddrCall(node.position, args=args)
        return out

    def visit_subscript_expr(self, node, children):
        out = children[0]
        for oper in children[1:]:
            oper.expr = out
            out = oper
        return out

    def visit_postfix_expr(self, node, children):
        if len(children) == 1:
            return children[0]
        return mn.MuvNodePostfixExpr(
            node.position,
            children[0],
            children[1],
        )

    def visit_unary_expr(self, node, children):
        if len(children) == 1:
            return children[0]
        oper = str(children[0])
        if oper == "+":
            return children[1]
        if oper == "-":
            return mn.MuvNodeBinaryExpr(
                node.position,
                children[1], "*", mn.MuvNodeInteger(node.position, -1)
            )
        if oper in ["++", "--"]:
            return mn.MuvNodePrefixExpr(node.position, oper, children[1])
        return mn.MuvNodeExprList(node.position, children[1], oper)

    def visit_power_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_multiplicative_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_additive_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_shift_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_relational_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_equality_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_bitand_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_bitxor_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_bitor_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_logical_and_expr(self, node, children):
        out = children[-1]
        for expr in reversed(children[:-1]):
            out = mn.MuvNodeLogicalAnd(expr.position, expr, out)
        return out

    def visit_logical_xor_expr(self, node, children):
        return self.left_associate_tree(children)

    def visit_logical_or_expr(self, node, children):
        out = children[-1]
        for expr in reversed(children[:-1]):
            pos = node.position
            if hasattr(expr, 'position'):
                pos = expr.position
            out = mn.MuvNodeLogicalOr(pos, expr, out)
        return out

    def visit_conditional_expr(self, node, children):
        if len(children) == 1:
            return children[0]
        return mn.MuvNodeIfElse(
            node.position,
            cond=children[0],
            ifclause=children[1],
            elseclause=children[2],
        )

    def visit_asgn_expr(self, node, children):
        lvalue, oper, value = children[:3]
        return mn.MuvNodeVarAssign(node.position, lvalue, value)

    def visit_asgn_append_expr(self, node, children):
        lvalue, oper, value = children[:3]
        return mn.MuvNodeVarOperAssign(
            node.position, lvalue, "swap []<-", value
        )

    def visit_asgn_oper_expr(self, node, children):
        lvalue, oper, value = children[:3]
        return mn.MuvNodeVarOperAssign(node.position, lvalue, oper, value)

    def visit_assignment_expr(self, node, children):
        return children[0]

    def visit_expr(self, node, children):
        if len(children) == 1:
            return children[0]
        out = mn.MuvNodeStatements(node.position)
        for child in children[:-1]:
            out.append(mn.MuvNodeCommand(child.position, "pop", child))
        out.append(children[-1])
        return out

    def visit_stmt_return(self, node, children):
        if len(children):
            return mn.MuvNodeCommand(node.position, "exit", children[0])
        return mn.MuvNodeCommand(node.position, "exit")

    def visit_stmt_break(self, node, children):
        return mn.MuvNodeStatements(node.position, "break")

    def visit_stmt_continue(self, node, children):
        return mn.MuvNodeStatements(node.position, "continue")

    def visit_stmt_expr(self, node, children):
        expr = children[0]
        if type(expr) not in [mn.MuvNodeVarAssign, mn.MuvNodeVarOperAssign]:
            expr = mn.MuvNodeExprList(expr.position, expr, "pop")
        return expr

    def visit_simple_statement(self, node, children):
        return children[0]

    def visit_stmt_do_if(self, node, children):
        return mn.MuvNodeIfElse(
            node.position,
            cond=children[1],
            ifclause=children[0],
        )

    def visit_stmt_do_unless(self, node, children):
        return mn.MuvNodeIfElse(
            node.position,
            cond=mn.MuvNodeCommand(children[1].position, "not", children[1]),
            ifclause=children[0],
        )

    def visit_stmt_simple(self, node, children):
        return children[0]

    def visit_statements(self, node, children):
        if not children:
            return mn.MuvNodeNull(node.position)
        return mn.MuvNodeStatements(node.position, *children)

    def visit_statement(self, node, children):
        if not children:
            return mn.MuvNodeNull(node.position)
        return children[0]

    def visit_stmt_for(self, node, children):
        forloop, body = children
        forloop.body = body
        return forloop

    def visit_stmt_foreach(self, node, children):
        forloop, body = children
        forloop.body = body
        return forloop

    def visit_stmt_if_else(self, node, children):
        if len(children) > 2:
            return mn.MuvNodeIfElse(
                node.position,
                cond=children[0],
                ifclause=children[1],
                elseclause=children[2],
            )
        return mn.MuvNodeIfElse(
            node.position,
            cond=children[0],
            ifclause=children[1],
        )

    def visit_stmt_while(self, node, children):
        return mn.MuvNodeWhile(
            node.position,
            cond=children[0],
            body=children[1],
        )

    def visit_stmt_until(self, node, children):
        return mn.MuvNodeUntil(
            node.position,
            cond=children[0],
            body=children[1],
        )

    def visit_stmt_do_while(self, node, children):
        return mn.MuvNodeDoWhile(
            node.position,
            body=children[0],
            cond=children[1],
        )

    def visit_stmt_do_until(self, node, children):
        return mn.MuvNodeDoUntil(
            node.position,
            body=children[0],
            cond=children[1],
        )

    def visit_stmt_try(self, node, children):
        settable = None
        if len(children) > 2:
            body, settable, handler = children
        else:
            body, handler = children
        return mn.MuvNodeTryCatch(
            node.position,
            body=body,
            handler=handler,
            var=settable,
        )

    def visit_usable_comparator(self, node, children):
        return children[0]

    def visit_using_comparator(self, node, children):
        comp = children[0]
        if str(comp) in ["strcmp", "stringcmp"]:
            return mn.MuvNodeExprList(node.position, comp, "not")
        return mn.MuvNodeExprList(node.position, comp)

    def visit_using_raw_muf(self, node, children):
        return mn.MuvNodeStatements(node.position, children[0])

    def visit_using_function(self, node, children):
        return mn.MuvNodeStatements(node.position, children[0])

    def visit_expr_using(self, node, children):
        if len(children) == 1:
            children.append(mn.MuvNodeExprList(node.position, "="))
        return children

    def visit_case_clause(self, node, children):
        return children

    def visit_case_clauses(self, node, children):
        return children

    def visit_default_clause(self, node, children):
        return children[0]

    def visit_switch_default(self, node, children):
        if children:
            return mn.MuvNodeExprList(
                node.position,
                children[0],
                "break",
            )
        return None

    def visit_stmt_switch(self, node, children):
        if len(children) == 2:
            children.append('')
        (expr, using_clause), case_clauses, dflt_clause = children
        if type(using_clause) == str:
            using_clause = mn.MuvNodeString(node.position, using_clause)
        cases = []
        vname = "swvar"
        for val, stmt in case_clauses:
            cases.append(
                mn.MuvNodeIfElse(
                    val.position,
                    cond=mn.MuvNodeExprList(
                        val.position,
                        mn.MuvNodeVarFetch(
                            val.position,
                            LValue(vname, [], val.position)
                        ),
                        val,
                        using_clause,
                    ),
                    ifclause=mn.MuvNodeExprList(
                        stmt.position, stmt, "break"
                    )
                )
            )
        if dflt_clause:
            cases.append(dflt_clause)
        lvalue = LValue(vname, [], expr.position, declare=True)
        return mn.MuvNodeSwitch(
            node.position,
            expr=expr,
            var=lvalue,
            cases=cases,
        )

    def visit_gstmt_include(self, node, children):
        filename = children[0].value
        muvparser = self.muvparser
        if muvparser.debug:
            line = muvparser.get_parse_line(children[0].position)
            muvparser.output += '\n(MUV:L%d) ' % line
        muvparser.include_file(filename, children[0].position)
        return None

    def visit_KW_TOP(self, node, children):
        return mn.MuvNodeStatements(node.position, '(top)')

    def visit_del_expr(self, node, children):
        lvalue = children[0]
        return mn.MuvNodeVarDel(node.position, lvalue)

    def visit_push_expr(self, node, children):
        return mn.MuvNodeExprList(node.position, *children)

    def visit_fmtstring_expr(self, node, children):
        args = children[0]
        fmt = args[0]
        if isinstance(fmt, mn.MuvNodeString):
            pos = fmt.position
            fmt = fmt.value.replace('%%', '')
            pats = re.findall(r'%[| +-]?[\d\*]*\.?[\d\*]*[isdDlefg~?]', fmt)
            acount = 0
            for pat in pats:
                acount += len(pat.split('*'))
            if len(args) - 1 != acount:
                raise MuvError(
                    (
                        "fmtstring(fmt, ...) format string "
                        "expects {exp} args, but got {found}."
                    ).format(
                        exp=acount,
                        found=len(args) - 1,
                    ),
                    position=pos,
                )
            errfmt = (
                "fmtstring(fmt, ...) format expected "
                "{exp} arg, but got {found} ({num})."
            )
            literals = [
                mn.MuvNodeInteger,
                mn.MuvNodeFloat,
                mn.MuvNodeDbRef,
                mn.MuvNodeString,
            ]
            fmt_types = {
                "i": ("integer", mn.MuvNodeInteger),
                "d": ("dbref", mn.MuvNodeDbRef),
                "D": ("dbref", mn.MuvNodeDbRef),
                "e": ("float", mn.MuvNodeFloat),
                "f": ("float", mn.MuvNodeFloat),
                "g": ("float", mn.MuvNodeFloat),
                "s": ("string", mn.MuvNodeString),
            }
            num = 0
            for pat in pats:
                num += 1
                for i in range(len(pat.split('*'))-1):
                    val = args[num]
                    if type(val) in literals:
                        if not isinstance(val, mn.MuvNodeInteger):
                            raise MuvError(
                                errfmt.format(
                                    exp="integer",
                                    found=val.valtype,
                                    num=num,
                                ),
                                position=val.position,
                            )
                    num += 1
                val = args[num]
                if type(val) in literals:
                    basepat = pat[-1]
                    typname, typ = fmt_types[basepat]
                    if not isinstance(val, typ):
                        raise MuvError(
                            errfmt.format(
                                exp=typname,
                                found=val.valtype,
                                num=num,
                            ),
                            position=val.position,
                        )
        args = list(reversed(list(args)))
        return mn.MuvNodeCommand(node.position, "fmtstring", *args)

    def visit_raw_muf(self, node, children):
        raw = children[0].value
        return mn.MuvNodeStatements(node.position, raw)

    def visit_stmt_raw_muf(self, node, children):
        return children[0]

    def visit_gstmt_const(self, node, children):
        cname, oper, expr = children
        return mn.MuvNodeGlobalConst(
            node.position,
            cname, expr
        )
        return None

    def visit_stmt_const(self, node, children):
        cname, oper, expr = children
        return mn.MuvNodeFuncConst(
            node.position,
            cname, expr
        )

    def visit_stmt_var(self, node, children):
        vname = children[0]
        return mn.MuvNodeFuncVar(node.position, vname)

    def visit_arglist(self, node, children):
        return children

    def visit_NS_SEP(self, node, children):
        return '::'

    def visit_ns_parts(self, node, children):
        return "".join(children)

    def visit_NS_IDENT(self, node, children):
        return "".join(children)

    def visit_VAR_IDENT(self, node, children):
        return "".join(children)

    def visit_CONST_IDENT(self, node, children):
        return "".join(children)

    def visit_FUNC_IDENT(self, node, children):
        return "".join(children)

    def visit_function_addr(self, node, children):
        funcname = children[1]
        return mn.MuvNodeFuncAddr(node.position, funcname)

    def visit_function_call(self, node, children):
        if len(children) < 2:
            children.append([])
        funcname, argslist = children[:2]
        return mn.MuvNodeFuncCall(
            node.position, funcname, argslist
        )

    def visit_dir_language(self, node, children):
        if children[0].value != "muv":
            raise MuvError(
                'Only $language "muv" allowed.',
                position=node.position,
            )
        return None

    def visit_dir_version(self, node, children):
        return mn.MuvNodeStatements(
            node.position,
            "$version %.3f\n" % children[0].value
        )

    def visit_dir_libversion(self, node, children):
        return mn.MuvNodeStatements(
            node.position,
            "$lib-version %.3f\n" % children[0].value
        )

    def visit_dir_author(self, node, children):
        return mn.MuvNodeStatements(
            node.position,
            "$author %s\n" % children[0].value
        )

    def visit_dir_note(self, node, children):
        return mn.MuvNodeStatements(
            node.position,
            "$note %s\n" % children[0].value
        )

    def visit_dir_echo(self, node, children):
        return mn.MuvNodeStatements(
            node.position,
            "$echo %s\n" % children[0].value
        )

    def visit_dir_pragma(self, node, children):
        return mn.MuvNodeStatements(
            node.position,
            "$pragma %s\n" % children[0].value
        )

    def visit_dir_include(self, node, children):
        return mn.MuvNodeStatements(
            node.position,
            "$include %s\n" % children[0].value
        )

    def visit_dir_error(self, node, children):
        raise MuvError(
            children[0].value,
            position=node.position,
        )
        return None

    def visit_dir_warn(self, node, children):
        print(children[0])
        return None

    def visit_KW_VOID(self, node, children):
        return 0

    def visit_KW_SINGLE(self, node, children):
        return 1

    def visit_KW_MULTIPLE(self, node, children):
        return 99

    def visit_gstmt_var_declinit(self, node, children):
        return mn.MuvNodeGlobalVar(node.position, children[0], children[2])

    def visit_gstmt_var_declonly(self, node, children):
        return mn.MuvNodeGlobalVar(node.position, children[0])

    def visit_simple_extern(self, node, children):
        extern_type, extern_name, (argvars, varargs) = children
        argcnt = len(argvars)
        return mn.MuvNodeExtern(
            node.position,
            extern_name,
            retcount=extern_type,
            argcount=argcnt,
            varargs=varargs,
        )

    def visit_raw_muf_extern(self, node, children):
        extern_type, extern_name, (argvars, varargs), oper, code = children
        argcnt = len(argvars)
        return mn.MuvNodeExtern(
            node.position,
            extern_name,
            retcount=extern_type,
            argcount=argcnt,
            varargs=varargs,
            code=code.value,
        )

    def visit_KW_PUBLIC(self, node, children):
        return "public"

    def visit_opt_public(self, node, children):
        return children

    def visit_declist(self, node, children):
        return children

    def visit_VARARG_MARKER(self, node, children):
        return "..."

    def visit_argvar_list(self, node, children):
        if len(children) == 0:
            return ([], False)
        if len(children) == 1:
            return (children[0], False)
        return (children[0], True)

    def visit_gstmt_func(self, node, children):
        pub = False
        if len(children) > 3:
            children = children[1:]
            pub = True
        funcname, (arglist, varargs), body = children
        return mn.MuvNodeFuncDef(
            node.position,
            funcname=funcname,
            args=arglist,
            body=body,
            varargs=varargs,
            public=pub,
        )

    def visit_gstmt_using_ns(self, node, children):
        ns = children[0]
        return mn.MuvNodeUsingNamespace(node.position, ns)

    def visit_nsdecl(self, node, children):
        namespace, body = children
        return mn.MuvNodeNamespace(node.position, namespace, body)

    def visit_global_statements(self, node, children):
        return children

    def visit_source_file(self, node, children):
        children = children[0]
        return mn.MuvNodeSourceFile(node.position, *children)

    def visit_program(self, node, children):
        return mn.MuvNodeProgram(node.position, children[0])


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
