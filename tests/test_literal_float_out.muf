( Generated from test_literal_float_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    {
        0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 -0.0 -1.0
        -2.0 -3.0 -4.0 -5.0 -6.0 -7.0
    }list
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
