( Generated from test_oper_bitnot_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    13 -1 bitxor
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
