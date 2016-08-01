( Generated from test_oper_minusequals_dual_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { 3 { 42 7 }list }list var! _a
    13 { 1 0 }list _a @ dup 3 pick array_nested_get 4 rotate - swap rot array_nested_set _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

