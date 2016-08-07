#######################################################################
# Utility classes
#######################################################################

from __future__ import unicode_literals
from __future__ import print_function

from pymuv.errors import MuvExceptionAlreadyDeclared


class FuncInfo(object):
    def __init__(
                self, pos, funcname,
                argcount=0,
                varargs=False,
                retcount=1,
                is_extern=False,
                code=None,
            ):
        self.position = pos
        self.funcname = funcname
        self.argcount = argcount
        self.varargs = varargs
        self.retcount = retcount
        self.is_extern = is_extern
        self.is_extern = is_extern
        self.code = code if code else funcname


class Scope(object):
    def __init__(self):
        self.variables = {}
        self.constants = {}

    def lookup_constant(self, name):
        if name not in self.constants:
            return None
        return self.constants[name]

    def lookup_variable(self, name):
        if name not in self.variables:
            return None
        return self.variables[name]

    def declare_constant(self, name, val):
        if name in self.constants:
            raise MuvExceptionAlreadyDeclared()
        self.constants[name] = val

    def declare_variable(self, name, realname):
        if name in self.variables:
            raise MuvExceptionAlreadyDeclared()
        self.variables[name] = realname


class Context(object):
    def __init__(self):
        self.parsers = []
        self.filenames = []
        self.debug = False
        self.scopes = [Scope()]
        self.func_realvars = {}
        self.curr_namespace = '::'
        self.using_namespaces = []
        self.global_consts = {}
        self.global_vars = {}
        self.init_statements = []
        self.functions = {}
        self.last_function = None
        self.last_func_pos = None
        self.assign_level = 0
        self.optimization_level = 1

        # Standard Global Variables
        self.declare_global_var("me", sys=True)
        self.declare_global_var("loc", sys=True)
        self.declare_global_var("trigger", sys=True)
        self.declare_global_var("command", sys=True)

        # Global Initialiations
        self.add_init('"me" match me ! me @ location loc ! trig trigger !')

        # Standard Builtin Functions
        self.declare_function(
            "abort", 1, retcount=0, is_extern=True, code="abort")
        self.declare_function(
            "throw", 1, retcount=0, is_extern=True, code="abort")
        self.declare_function(
            "tell", 1, retcount=0, is_extern=True, code="me @ swap notify")
        self.declare_function(
            "count", 1, retcount=1, is_extern=True, code="array_count")
        self.declare_function(
            "cat", 1, varargs=True, retcount=1, is_extern=True,
            code="array_interpret"
        )
        self.declare_function(
            "haskey", 2, retcount=1, is_extern=True,
            code="swap 1 array_make array_extract"
        )

        # Global Constants
        self.declare_global_const("true", "1")
        self.declare_global_const("false", "0")

    # Misc ###################################################

    def scope_push(self):
        self.scopes.append(Scope())

    def scope_pop(self):
        self.scopes.pop()

    def add_init(self, expstr):
        self.init_statements.append(expstr)

    # NameSpaces #############################################

    def set_namespace(self, ns):
        if ns.startswith('::'):
            self.curr_namespace = ns
        else:
            if self.curr_namespace != "::":
                self.curr_namespace += '::'
            self.curr_namespace += ns

    def use_namespace(self, ns):
        if not ns.startswith('::'):
            oldns = self.curr_namespace
            if oldns == "::":
                oldns = ''
            ns = '%s::%s' % (oldns, ns)
        self.using_namespaces.append(ns)

    def canonical_name(self, name):
        if name.startswith('::'):
            return name
        ns = self.curr_namespace
        if ns == "::":
            ns = ""
        out = "{ns}::{name}".format(ns=ns, name=name)
        while '::::' in ns:
            ns = ns.replace('::::', '::')
        return out

    def actualize_name(self, name):
        name = self.canonical_name(name)
        name = name.strip(':').replace('::', '__')
        if "__" not in name:
            name = "_" + name
        return name

    def possible_canonicals(self, name):
        out = []
        if name.startswith('::'):
            return [name]
        for ns in self.using_namespaces:
            if ns == '::':
                ns = ''
            canonical = "%s::%s" % (ns, name)
            out.append(canonical)
        ns = self.curr_namespace
        while True:
            if ns == '::':
                ns = ''
            canonical = "%s::%s" % (ns, name)
            out.append(canonical)
            if not ns:
                break
            ns = ns.rsplit('::', 1)[0]
        return out

    # Constants ##############################################

    def lookup_constant(self, name):
        for scope in reversed(self.scopes):
            found = scope.lookup_constant(name)
            if found:
                return found
        for name in self.possible_canonicals(name):
            if name in self.global_consts:
                return self.global_consts[name]
        return None

    def declare_constant(self, name, val):
        self.scopes[-1].declare_constant(name, val)

    def declare_global_const(self, name, val):
        name = self.canonical_name(name)
        self.global_consts[name] = val

    # Variables ##############################################

    def lookup_variable(self, name):
        for scope in reversed(self.scopes):
            found = scope.lookup_variable(name)
            if found:
                return found
        for name in self.possible_canonicals(name):
            if name in self.global_vars:
                return self.global_vars[name]
        return None

    def declare_variable(self, name):
        realname = name
        if "__" not in realname:
            realname = "_%s" % realname
        for i in range(2, 99):
            if realname not in self.func_realvars:
                break
            realname = "%s%d" % (name, i)
            if "__" not in realname:
                realname = "_%s" % realname
        self.scopes[-1].declare_variable(name, realname)
        self.func_realvars[realname] = name
        return realname

    def declare_global_var(self, name, sys=False):
        realname = name
        name = self.canonical_name(name)
        if not sys:
            realname = self.actualize_name(name)
        self.global_vars[name] = realname
        return realname

    # Functions ##############################################

    def lookup_function(self, name):
        for name in self.possible_canonicals(name):
            if name in self.functions:
                return self.functions[name]
        return None

    def declare_function(
                self, name, argcount,
                varargs=False,
                retcount=1,
                is_extern=False,
                code=None,
                is_public=False,
                pos=None
            ):
        canonical = self.canonical_name(name)
        actual = self.actualize_name(name)
        if is_public and actual.startswith("_"):
            actual = actual[1:]
        if not code:
            code = actual
        self.functions[canonical] = FuncInfo(
            pos, actual,
            argcount=argcount,
            varargs=varargs,
            retcount=retcount,
            is_extern=is_extern,
            code=code
        )
        self.last_function = actual
        self.last_func_pos = pos
        return actual

    def reset_function_local_data(self):
        self.scopes = [Scope()]
        self.func_realvars = {}


# vim: set ts=4 sw=4 et ai hlsearch nowrap :
