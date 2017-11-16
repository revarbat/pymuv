( Generated from test_oper_minus_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    42 var! _a
    13 var! _b
    _a @ _b @ - var! _c
    29 var! _d
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
