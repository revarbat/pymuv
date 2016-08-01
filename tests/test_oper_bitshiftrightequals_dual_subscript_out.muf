( Generated from test_oper_bitshiftrightequals_dual_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { 3 { 42 7 }list }list var! _a
    3 { 1 0 }list _a @ dup 3 pick array_nested_get 4 rotate -1 * bitshift swap rot array_nested_set _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

