( Generated from test_array_declare_three_strings_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { "abc" "def" "ghi" }list
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
