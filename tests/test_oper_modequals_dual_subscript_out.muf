( Generated from test_oper_modequals_dual_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    { 3 { 42 7 }list }list var! _a
    _a @ { 1 0 }list over over array_nested_get 13 % rot rot array_nested_set _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
