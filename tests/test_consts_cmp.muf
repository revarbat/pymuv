( Generated from test_consts_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    3.14159 2.71828 /
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
