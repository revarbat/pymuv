( Generated from test_precedence1_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    3 var! _a
    4 var! _b
    5 var! _c
    6 var! _d
    7 var! _e
    _a @ _b @ _c @ _d @ + * + _e @ - var! _f
    40
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
