( Generated from test_namespace1_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
lvar foo::ltuaa
: foo::abc[ _a -- ret ]
    foo::ltuaa @ _a @ +
;
: foo::def[ _a -- ret ]
    _a @ 2 * foo::abc
;
: _main[ _arg -- ret ]
    3 foo::def
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    42 foo::ltuaa !
    _main
;
