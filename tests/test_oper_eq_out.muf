( Generated from test_oper_eq_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    "Foo" var! _s
    _s @ "bar" strcmp not
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
