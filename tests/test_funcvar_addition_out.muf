( Generated from test_funcvar_addition_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    42 var! _a
    _a @ 13 +
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
