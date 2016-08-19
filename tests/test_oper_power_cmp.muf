( Generated from test_oper_power_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _ang -- ret ]
    2 3 pow
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
