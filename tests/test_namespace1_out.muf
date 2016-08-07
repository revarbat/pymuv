( Generated from test_namespace1_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

lvar foo__ltuaa
: foo__abc[ _a -- ret ]
    foo__ltuaa @ _a @ +
;
: foo__def[ _a -- ret ]
    _a @ 2 * foo__abc
;
: _main[ _arg -- ret ]
    3 foo__def
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    42 foo__ltuaa !
    _main
;
