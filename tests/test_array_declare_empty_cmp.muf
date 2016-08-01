( Generated from test_array_declare_empty_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { }list
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
