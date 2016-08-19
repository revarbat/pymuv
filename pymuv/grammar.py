#######################################################################
# Arpeggio PEG Grammar for MUV
#######################################################################

from __future__ import unicode_literals

from arpeggio import (
    Optional, ZeroOrMore, OneOrMore, EOF, Kwd
)
from arpeggio import RegExMatch as _


def comment_line():
    return _(r'//.*?$', str_repr='comment')


def comment_multi():
    return _(r'/\*(?ms).*?\*/', str_repr='comment')


def comment():
    return [comment_line, comment_multi]


def DIR_AUTHOR():
    return "$author"


def DIR_ECHO():
    return "$echo"


def DIR_ERROR():
    return "$error"


def DIR_INCLUDE():
    return "$include"


def DIR_LANGUAGE():
    return "$language"


def DIR_LIBVERSION():
    return "$libversion"


def DIR_NOTE():
    return "$note"


def DIR_PRAGMA():
    return "$pragma"


def DIR_VERSION():
    return "$version"


def DIR_WARN():
    return "$warn"


def KW_BREAK():
    return Kwd("break")


def KW_BY():
    return Kwd("by")


def KW_CASE():
    return Kwd("case")


def KW_CATCH():
    return Kwd("catch")


def KW_CONST():
    return Kwd("const")


def KW_CONTINUE():
    return Kwd("continue")


def KW_DEFAULT():
    return Kwd("default")


def KW_DEL():
    return Kwd("del")


def KW_DO():
    return Kwd("do")


def KW_ELSE():
    return Kwd("else")


def KW_EXTERN():
    return Kwd("extern")


def KW_FMTSTRING():
    return Kwd("fmtstring")


def KW_FOR():
    return Kwd("for")


def KW_FUNC():
    return Kwd("func")


def KW_IF():
    return Kwd("if")


def KW_IN():
    return Kwd("in")


def KW_INCLUDE():
    return Kwd("include")


def KW_MUF():
    return Kwd("muf")


def KW_MULTIPLE():
    return Kwd("multiple")


def KW_NAMESPACE():
    return Kwd("namespace")


def KW_PUBLIC():
    return Kwd("public")


def KW_PUSH():
    return Kwd("push")


def KW_RETURN():
    return Kwd("return")


def KW_SINGLE():
    return Kwd("single")


def KW_SWITCH():
    return Kwd("switch")


def KW_TOP():
    return Kwd("top")


def KW_TRY():
    return Kwd("try")


def KW_UNLESS():
    return Kwd("unless")


def KW_UNTIL():
    return Kwd("until")


def KW_USING():
    return Kwd("using")


def KW_VAR():
    return Kwd("var")


def KW_VOID():
    return Kwd("void")


def KW_WHILE():
    return Kwd("while")


def VARARG_MARKER():
    return "*"


def KEYVAL():
    return "=>"


def DOT():
    return "."


def COMMA():
    return ","


def COLON():
    return ":"


def SEMICOLON():
    return ";"


def PAREN():
    return "("


def ENDPAR():
    return ")"


def BRACE():
    return "{"


def ENDBRACE():
    return "}"


def BRACKET():
    return "["


def ENDBRACKET():
    return "]"


def ASGN():
    return _(r'=(?![=>])', str_repr='=')


def ASGN_PLUS():
    return "+="


def ASGN_MINUS():
    return "-="


def ASGN_MULT():
    return "*="


def ASGN_DIV():
    return "/="


def ASGN_MOD():
    return "%="


def ASGN_POWER():
    return "**="


def ASGN_BITAND():
    return "&="


def ASGN_BITOR():
    return "|="


def ASGN_BITXOR():
    return "^="


def ASGN_BITLEFT():
    return "<<="


def ASGN_BITRIGHT():
    return ">>="


def OPER_PLUS():
    return _(r'\+(?![=+])', str_repr='+')


def OPER_MINUS():
    return _(r'-(?![=-])', str_repr='-')


def OPER_MULT():
    return _(r'\*(?![/*=])', str_repr='*')


def OPER_DIV():
    return _(r'/(?![/*=])', str_repr='/')


def OPER_MOD():
    return _(r'%(?!=)', str_repr='%')


def OPER_POWER():
    return _(r'\*\*(?!=)', str_repr='**')


def OPER_BITAND():
    return _(r'&(?![&=])', str_repr='&')


def OPER_BITOR():
    return _(r'\|(?![|=])', str_repr='|')


def OPER_BITXOR():
    return _(r'\^(?![=^])', str_repr='^')


def OPER_BITNOT():
    return "~"


def OPER_BITLEFT():
    return _(r'<<(?!=)', str_repr='<<')


def OPER_BITRIGHT():
    return _(r'>>(?!=)', str_repr='>>')


def OPER_INCR():
    return "++"


def OPER_DECR():
    return "--"


def OPER_TERNARY():
    return "?"


def LOGICAL_AND():
    return "&&"


def LOGICAL_OR():
    return "||"


def LOGICAL_XOR():
    return "^^"


def LOGICAL_NOT():
    return _(r'!(?!=)', str_repr='!')


def COMP_EQ():
    return "=="


def COMP_NEQ():
    return "!="


def COMP_LT():
    return _(r'<(?![=<])', str_repr='<')


def COMP_GT():
    return _(r'>(?![=>])', str_repr='>')


def COMP_LTE():
    return "<="


def COMP_GTE():
    return ">="


def COMP_IN():
    return "in"


def COMP_STREQ():
    return "eq"


def NS_SEP():
    return "::"


def identifier():
    return _(r'(?i)[a-z_]\w*', str_repr='ident')


def ns_parts():
    return Optional(NS_SEP), ZeroOrMore(identifier, NS_SEP)


def ATTR_IDENT():
    return identifier


def NS_IDENT():
    return ns_parts, identifier


def FUNC_IDENT():
    return ns_parts, identifier, Optional("?")


def DECL_VAR_IDENT():
    return identifier


def VAR_IDENT():
    return ns_parts, identifier


def CONST_IDENT():
    return ns_parts, identifier


def numsign():
    return ["+", "-"]


def bin_integer():
    return "0b", _(r'[01_]+', str_repr='binary-number')


def oct_integer():
    return "0o", _(r'[0-7_]+', str_repr='octal-number')


def dec_integer():
    return Optional("0d"), _(r'[0-9_]+(?![.eE])', str_repr='decimal-number')


def hex_integer():
    return "0x", _(r'[0-9a-fA-F_]+', str_repr='hex-integer')


def unsigned_integer():
    return [hex_integer, oct_integer, bin_integer, dec_integer]


def intnum():
    return Optional(numsign), unsigned_integer


def floatnum():
    return [
        _(r'[+-]?(\d+[.]\d*|\d*[.]\d+|\d+)[eE][+-]?[0-9]+', str_repr='float'),
        _(r'[+-]?(\d+[.]\d*|\d*[.]\d+)', str_repr='float'),
    ]


def number():
    return [floatnum, intnum]


def dbref():
    return "#", intnum


def raw_dquote_string():
    return [_('r".*?"', str_repr='string')]


def raw_squote_string():
    return [_("r'.*?'", str_repr='string')]


def raw_dquote3_string():
    return [_('(?ms)r""".*?"""', str_repr='string')]


def raw_squote3_string():
    return [_("(?ms)r'''.*?'''", str_repr='string')]


def dquote_string():
    return [_(r'"([^"\\]|\\.|\\$)*"', str_repr='string')]


def squote_string():
    return [_(r"'([^'\\]|\\.|\\$)*'", str_repr='string')]


def dquote3_string():
    return [_(r'(?ms)"""([^"\\]|\\.|"(?!""))*"""', str_repr='string')]


def squote3_string():
    return [_(r"(?ms)'''([^'\\]|\\.|'(?!''))*'''", str_repr='string')]


def raw_string_literal():
    return [
        raw_dquote3_string,
        raw_squote3_string,
        raw_dquote_string,
        raw_squote_string,
    ]


def esc_string_literal():
    return [
        dquote3_string,
        squote3_string,
        dquote_string,
        squote_string
    ]


def string_literal():
    return [raw_string_literal, esc_string_literal]


def declist():
    return DECL_VAR_IDENT, ZeroOrMore(COMMA, DECL_VAR_IDENT)


def argvar_list():
    return [
        (PAREN, ENDPAR),
        (PAREN, declist, Optional(VARARG_MARKER), ENDPAR)
    ]


def arglist():
    return assignment_expr, ZeroOrMore(COMMA, assignment_expr)


def paren_expr():
    return PAREN, expr, ENDPAR


def extern_type():
    return [KW_VOID, KW_SINGLE, KW_MULTIPLE]


def keyval_pair():
    return assignment_expr, KEYVAL, assignment_expr


def dictlist():
    return [
        KEYVAL,
        (keyval_pair, ZeroOrMore(COMMA, keyval_pair))
    ]


def compr_cond_if():
    return KW_IF, paren_expr


def compr_cond_unless():
    return KW_UNLESS, paren_expr


def compr_cond():
    return [compr_cond_if, compr_cond_unless]


def compr_for():
    return [for_expr, foreach_expr]


def raw_muf():
    return KW_MUF, PAREN, string_literal, ENDPAR


def stmt_raw_muf():
    return raw_muf, SEMICOLON


def gstmt_const():
    return KW_CONST, CONST_IDENT, ASGN, expr, SEMICOLON


def gstmt_using_ns():
    return KW_USING, KW_NAMESPACE, NS_IDENT, SEMICOLON


def gstmt_include():
    return KW_INCLUDE, string_literal, SEMICOLON


def gstmt_var_declinit():
    return KW_VAR, DECL_VAR_IDENT, ASGN, expr, SEMICOLON


def gstmt_var_declonly():
    return KW_VAR, DECL_VAR_IDENT, SEMICOLON


def gstmt_var():
    return [gstmt_var_declinit, gstmt_var_declonly]


def simple_extern():
    return KW_EXTERN, extern_type, FUNC_IDENT, argvar_list, SEMICOLON


def raw_muf_extern():
    return (
        KW_EXTERN, extern_type, FUNC_IDENT, argvar_list,
        ASGN, string_literal, SEMICOLON
    )


def opt_public():
    return Optional(KW_PUBLIC)


def gstmt_func():
    return opt_public, KW_FUNC, FUNC_IDENT, argvar_list, statements


def nsdecl():
    return KW_NAMESPACE, NS_IDENT, BRACE, global_statements, ENDBRACE


def global_statement():
    return [
        directive,
        stmt_raw_muf,
        gstmt_using_ns,
        gstmt_include,
        gstmt_const,
        gstmt_var,
        simple_extern,
        raw_muf_extern,
        gstmt_func
    ]


def variable():
    return VAR_IDENT


def declared_lvalue():
    return KW_VAR, variable


def indexed_lvalue():
    return variable, ZeroOrMore(index_part)


def lvalue():
    return [declared_lvalue, indexed_lvalue]


def tuple_parts():
    return COMP_LT, lvalue, ZeroOrMore(COMMA, lvalue), COMP_GT


def subscript():
    return BRACKET, expr, ENDBRACKET


def attribute():
    return DOT, ATTR_IDENT


def index_part():
    return [subscript, attribute]


def settable():
    return [tuple_parts, lvalue]


def stmt_return():
    return KW_RETURN, Optional(expr)


def stmt_break():
    return KW_BREAK


def stmt_continue():
    return KW_CONTINUE


def stmt_expr():
    return expr


def simple_statement():
    return [
        stmt_return,
        stmt_break,
        stmt_continue,
        stmt_expr,
    ]


def stmt_var():
    return KW_VAR, DECL_VAR_IDENT, SEMICOLON


def stmt_const():
    return KW_CONST, CONST_IDENT, ASGN, expr, SEMICOLON


def stmt_do_if():
    return simple_statement, KW_IF, paren_expr, SEMICOLON


def stmt_do_unless():
    return simple_statement, KW_UNLESS, paren_expr, SEMICOLON


def stmt_simple():
    return simple_statement, SEMICOLON


def stmt_if_else():
    return [
        (KW_IF, paren_expr, statement, KW_ELSE, statement),
        (KW_IF, paren_expr, statement),
    ]


def stmt_while():
    return KW_WHILE, paren_expr, statement


def stmt_until():
    return KW_UNTIL, paren_expr, statement


def stmt_do_while():
    return KW_DO, statement, KW_WHILE, paren_expr, SEMICOLON


def stmt_do_until():
    return KW_DO, statement, KW_UNTIL, paren_expr, SEMICOLON


def for_expr():
    return (
        KW_FOR, PAREN,
        lvalue, KW_IN,
        expr, KEYVAL, expr, Optional(KW_BY, expr),
        ENDPAR
    )


def foreach_expr():
    return (
        KW_FOR, PAREN,
        settable, Optional(KEYVAL, settable),
        KW_IN, expr,
        ENDPAR
    )


def stmt_for():
    return for_expr, statement


def stmt_foreach():
    return foreach_expr, statement


def stmt_try():
    return (
        KW_TRY, statement,
        KW_CATCH, PAREN, Optional(settable), ENDPAR,
        statement
    )


def function_name():
    return FUNC_IDENT


def usable_comparator():
    return [
        COMP_EQ,
        COMP_NEQ,
        COMP_LT,
        COMP_GT,
        COMP_LTE,
        COMP_GTE,
        COMP_IN,
        COMP_STREQ,
        "strcmp",
        "stringcmp",
    ]


def using_comparator():
    return KW_USING, usable_comparator


def using_raw_muf():
    return KW_USING, raw_muf


def using_function():
    return KW_USING, function_name


def expr_using():
    return [
        (expr, using_comparator),
        (expr, using_raw_muf),
        (expr, using_function),
        expr,
    ]


def case_clause():
    return KW_CASE, paren_expr, statement


def case_clauses():
    return OneOrMore(case_clause)


def default_clause():
    return KW_DEFAULT, statement


def switch_default():
    return Optional(default_clause)


def stmt_switch():
    return (
        KW_SWITCH, PAREN, expr_using, ENDPAR,
        BRACE, case_clauses, switch_default, ENDBRACE
    )


def statements():
    return BRACE, ZeroOrMore(statement), ENDBRACE


def statement():
    return [
        SEMICOLON,
        stmt_const,
        stmt_var,
        stmt_do_if,
        stmt_do_unless,
        stmt_simple,
        stmt_if_else,
        stmt_while,
        stmt_until,
        stmt_do_while,
        stmt_do_until,
        stmt_for,
        stmt_foreach,
        stmt_try,
        stmt_switch,
        statements,
    ]


def del_expr():
    return KW_DEL, PAREN, lvalue, ENDPAR


def push_expr():
    return KW_PUSH, PAREN, arglist, ENDPAR


def fmtstring_expr():
    return KW_FMTSTRING, PAREN, arglist, ENDPAR


def function_addr():
    return OPER_BITAND, FUNC_IDENT


def function_call():
    return FUNC_IDENT, PAREN, Optional(arglist), ENDPAR


def postfix_oper():
    return [OPER_INCR, OPER_DECR]


def unary_oper():
    return [
        OPER_INCR, OPER_DECR,
        OPER_PLUS, OPER_MINUS,
        OPER_BITNOT, LOGICAL_NOT
    ]


def power_oper():
    return [OPER_POWER]


def multiplicative_oper():
    return [OPER_MULT, OPER_DIV, OPER_MOD]


def additive_oper():
    return [OPER_PLUS, OPER_MINUS]


def shift_oper():
    return [OPER_BITLEFT, OPER_BITRIGHT]


def relational_oper():
    return [COMP_LTE, COMP_GTE, COMP_LT, COMP_GT, COMP_IN]


def equality_oper():
    return [COMP_EQ, COMP_NEQ, COMP_STREQ]


def assignment_oper():
    return [
        ASGN_MULT, ASGN_DIV, ASGN_MOD,
        ASGN_PLUS, ASGN_MINUS,
        ASGN_BITLEFT, ASGN_BITRIGHT,
        ASGN_BITAND, ASGN_BITXOR, ASGN_BITOR
    ]


def dict_comprehension():
    return BRACKET, compr_for, Optional(compr_cond), keyval_pair, ENDBRACKET


def list_comprehension():
    return BRACKET, compr_for, Optional(compr_cond), expr, ENDBRACKET


def dict_initialization():
    return BRACKET, dictlist, ENDBRACKET


def list_initialization():
    return [
        (BRACKET, ENDBRACKET),
        (BRACKET, arglist, ENDBRACKET)
    ]


def comprehension():
    return [
        dict_comprehension,
        list_comprehension,
        dict_initialization,
        list_initialization,
    ]


def leaf_variable():
    return variable


def leaf_expr():
    return [
        paren_expr,
        comprehension,
        number,
        dbref,
        string_literal,
        fmtstring_expr,
        KW_TOP,
        del_expr,
        push_expr,
        raw_muf,
        function_addr,
        function_call,
        leaf_variable,
    ]


def index_oper():
    return index_part


def addrcall_oper():
    return PAREN, Optional(arglist), ENDPAR


def subscript_expr():
    return leaf_expr, ZeroOrMore([index_oper, addrcall_oper])


def postfix_expr():
    return [
        (subscript_expr, postfix_oper),
        subscript_expr
    ]


def unary_expr():
    return [
        postfix_expr,
        (unary_oper, unary_expr)
    ]


def power_expr():
    return unary_expr, ZeroOrMore(power_oper, unary_expr)


def multiplicative_expr():
    return power_expr, ZeroOrMore(multiplicative_oper, power_expr)


def additive_expr():
    return multiplicative_expr, ZeroOrMore(additive_oper, multiplicative_expr)


def shift_expr():
    return additive_expr, ZeroOrMore(shift_oper, additive_expr)


def relational_expr():
    return shift_expr, ZeroOrMore(relational_oper, shift_expr)


def equality_expr():
    return relational_expr, ZeroOrMore(equality_oper, relational_expr)


def bitand_expr():
    return equality_expr, ZeroOrMore(OPER_BITAND, equality_expr)


def bitxor_expr():
    return bitand_expr, ZeroOrMore(OPER_BITXOR, bitand_expr)


def bitor_expr():
    return bitxor_expr, ZeroOrMore(OPER_BITOR, bitxor_expr)


def logical_and_expr():
    return bitor_expr, ZeroOrMore(LOGICAL_AND, bitor_expr)


def logical_xor_expr():
    return logical_and_expr, ZeroOrMore(LOGICAL_XOR, logical_and_expr)


def logical_or_expr():
    return logical_xor_expr, ZeroOrMore(LOGICAL_OR, logical_xor_expr)


def conditional_expr():
    return [
        (
            logical_or_expr,
            OPER_TERNARY, assignment_expr,
            COLON, assignment_expr
        ),
        logical_or_expr
    ]


def asgn_expr():
    return settable, ASGN, assignment_expr


def asgn_append_expr():
    return settable, BRACKET, ENDBRACKET, ASGN, assignment_expr


def asgn_oper_expr():
    return lvalue, assignment_oper, assignment_expr


def assignment_expr():
    return [
        asgn_expr,
        asgn_append_expr,
        asgn_oper_expr,
        conditional_expr
    ]


def expr():
    return assignment_expr, ZeroOrMore(COMMA, assignment_expr)


def dir_language():
    return DIR_LANGUAGE, string_literal


def dir_version():
    return DIR_VERSION, floatnum


def dir_libversion():
    return DIR_LIBVERSION, floatnum


def dir_author():
    return DIR_AUTHOR, string_literal


def dir_note():
    return DIR_NOTE, string_literal


def dir_echo():
    return DIR_ECHO, string_literal


def dir_pragma():
    return DIR_PRAGMA, string_literal


def dir_include():
    return DIR_INCLUDE, string_literal


def dir_error():
    return DIR_ERROR, string_literal


def dir_warn():
    return DIR_WARN, string_literal


def directive():
    return [
        dir_author,
        dir_echo,
        dir_error,
        dir_include,
        dir_language,
        dir_libversion,
        dir_note,
        dir_pragma,
        dir_version,
        dir_warn,
    ]


def global_statements():
    return ZeroOrMore([global_statement, nsdecl])


def source_file():
    return global_statements, EOF


def program():
    return [source_file]


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
