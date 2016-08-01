( Generated from test_namespace2_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
lvar foo::fee
: foo::abc[ _a -- ret ]
    foo::fee @ _a @ +
;
: bar::abc[ _a -- ret ]
    13 _a @ +
;
: _main[ _arg -- ret ]
    3 foo::abc bar::abc pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    42 foo::fee !
    _main
;
