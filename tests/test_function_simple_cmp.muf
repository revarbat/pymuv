( Generated from test_function_simple_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _foo[ _a -- ret ]
    _a @ 1 +
;
: _bar[ -- ret ]
    2
;
: _main[ _arg -- ret ]
    2 _foo pop
    _bar pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

