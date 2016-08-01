( Generated from test_function_one_arg_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _sub[ _a -- ret ]
    _a @
;
: _main[ _arg -- ret ]
    "Foo" _sub
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
