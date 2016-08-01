( Generated from test_oper_plusequals_chained_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    var _a var _b
    { 13 42 }list _a !
    _a @ 1 over over [] 13 + dup 4 rotate 4 rotate ->[] _a ! _b !
    _b @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
