( Generated from test_dict_declare1_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { "abc" 9 "def" 2 "ghi" 7 }dict
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
