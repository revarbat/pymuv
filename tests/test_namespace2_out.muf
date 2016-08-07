( Generated from test_namespace2_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

lvar foo__fee
: foo__abc[ _a -- ret ]
    foo__fee @ _a @ +
;
: bar__abc[ _a -- ret ]
    13 _a @ +
;
: _main[ _arg -- ret ]
    3 foo__abc bar__abc pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    42 foo__fee !
    _main
;
