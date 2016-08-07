( Generated from test_dict_subscript_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    { "foo" "FOO" "bar" "BAR" "baz" "BAZ" }dict var! _a
    _a @ "bar" []
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
