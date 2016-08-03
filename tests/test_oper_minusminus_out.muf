( Generated from test_oper_minusminus_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    42 var! _a
    13 var! _b
    _a @ _a -- _b dup -- @ -
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
