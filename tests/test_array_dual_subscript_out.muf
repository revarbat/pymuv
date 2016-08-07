( Generated from test_array_dual_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    { { 42 13 }list { 13 7 }list { 7 42 }list }list var! _a
    _a @ 1 [] 0 []
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
