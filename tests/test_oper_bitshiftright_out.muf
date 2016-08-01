( Generated from test_oper_bitshiftright_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    42 2 -1 * bitshift
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

