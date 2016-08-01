( Generated from test_literal_string1_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    "A String"
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
