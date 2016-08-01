( Generated from test_oper_plusplus_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    var _a var _b
    42 _a !
    13 _b !
    _a @ dup ++ _a ! _b @ ++ dup _b ! +
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
