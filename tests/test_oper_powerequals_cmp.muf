( Generated from test_oper_powerequals_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    4 var! _a
    _a @ 2 pow dup _a !
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
