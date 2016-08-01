( Generated from test_array_declare_single_int_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { 42 }list
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
