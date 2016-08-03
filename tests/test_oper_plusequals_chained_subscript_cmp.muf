( Generated from test_oper_plusequals_chained_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    { 13 42 }list var! _a
    _a @ 1 over over [] 13 + dup -4 rotate rot rot ->[] _a ! var! _b
    _b @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

