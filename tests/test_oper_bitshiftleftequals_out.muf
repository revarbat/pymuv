( Generated from test_oper_bitshiftleftequals_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    42 var! _a
    3 _a @ swap bitshift _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

