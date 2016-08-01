( Generated from test_dict_dual_subscript_assign_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    { "foo" { "fee" 0 "fie" 2 "foe" 7 "fum" 9 }dict "bar" { "fee" 2 "fie" 7 "foe" 3 "fum" 8 }dict }dict var! _a
    "FOO" _a @ { "foo" "fie" }list array_nested_set _a !
    _a @ "foo" [] "fie" []
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

