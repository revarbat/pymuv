( Generated from test_array_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    { 42 13 7 }list var! _a
    _a @ 1 []
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
