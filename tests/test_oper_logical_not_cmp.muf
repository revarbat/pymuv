( Generated from test_oper_logical_not_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    1 not
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
