( Generated from test_oper_bitand_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    42 13 bitand
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
