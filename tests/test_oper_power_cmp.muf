( Generated from test_oper_power_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _ang -- ret ]
    2 var! _a
    3 var! _b
    _a @ _b @ pow var! _c
    8 var! _d
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
