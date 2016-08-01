( Generated from test_oper_timesequals_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    42 var! _a
    13 _a @ * _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

