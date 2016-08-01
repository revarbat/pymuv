( Generated from test_function_varargs_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _sub[ _a -- ret ]
    _a @ 0 []
;
: _main[ _arg -- ret ]
    { "Foo" "Bar" }list _sub
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
