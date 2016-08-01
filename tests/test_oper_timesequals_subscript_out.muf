( Generated from test_oper_timesequals_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { 13 42 }list var! _a
    13 1 _a @ dup 3 pick [] 4 rotate * swap rot ->[] _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

