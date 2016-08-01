( Generated from test_oper_logical_xor_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    1 1 xor
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
