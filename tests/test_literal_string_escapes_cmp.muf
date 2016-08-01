( Generated from test_literal_string_escapes_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    "A string with\rnewlines and \[[1mstuff\[[0m."
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
