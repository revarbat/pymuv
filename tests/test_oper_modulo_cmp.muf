( Generated from test_oper_modulo_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    42 13 %
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
