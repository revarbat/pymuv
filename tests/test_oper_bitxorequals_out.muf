( Generated from test_oper_bitxorequals_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    42 var! _a
    _a @ 13 bitxor _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
