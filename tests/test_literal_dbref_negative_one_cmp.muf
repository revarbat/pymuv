( Generated from test_literal_dbref_negative_one_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    #-1
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
