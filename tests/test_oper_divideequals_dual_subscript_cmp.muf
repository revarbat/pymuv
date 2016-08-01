( Generated from test_oper_divideequals_dual_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    var _a
    { 3 { 42 7 }list }list _a !
    _a @ { 1 0 }list over over array_nested_get 13 / rot rot array_nested_set _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
