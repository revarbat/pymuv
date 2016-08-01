( Generated from test_oper_bitshiftleftequals_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    var _a
    { 13 42 }list _a !
    _a @ 1 over over [] 3 bitshift rot rot ->[] _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
