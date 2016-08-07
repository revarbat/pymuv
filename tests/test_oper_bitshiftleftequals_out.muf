( Generated from test_oper_bitshiftleftequals_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    42 var! _a
    _a @ 3 bitshift _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
