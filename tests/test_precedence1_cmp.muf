( Generated from test_precedence1_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    3 4 5 6 + * + 7 -
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
