( Generated from test_dict_subscript_assign_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    { }list var! _a
    "FOO" _a @ "foo" ->[] _a !
    _a @ "foo" []
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

