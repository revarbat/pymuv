( Generated from test_literal_int_negative_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    -42
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
