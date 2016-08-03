( Generated from test_oper_bitshiftrightequals_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    { 13 42 }list var! _a
    _a @ 1 over over [] 3 -1 * bitshift rot rot ->[] _a !
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

