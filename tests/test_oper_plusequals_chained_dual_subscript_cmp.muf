( Generated from test_oper_plusequals_chained_dual_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    var _a var _b
    { 3 { 42 7 }list }list _a !
    _a @ { 1 0 }list over over array_nested_get 13 + dup
    4 rotate 4 rotate array_nested_set _a ! _b !
    _b @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
