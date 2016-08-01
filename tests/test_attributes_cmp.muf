
( Generated from test_attributes_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _sub[ _a _b _c -- ret ]
    { _a @ _b @ _c @ }list array_interpret
;
: _main[ _arg -- ret ]
    { "foo" { "fee" 2 "fie" 8 "foe" 7 "fum" 42 }dict "bar" { "blah" 1 "blat" 3 "bloo" 5 "bleh" 7 "boo" '_sub }dict "baz" '_sub }dict var! _arr
    _arr @ "foo" [] "fie" [] var! _b
    43 _arr @ { "bar" "bloo" }list array_nested_set _arr !
    7 { "bar" "blat" }list _arr @ dup 3 pick array_nested_get 4 rotate + swap rot array_nested_set _arr !
    8 { "bar" "blat" }list _arr @ dup 3 pick array_nested_get 4 rotate + swap rot array_nested_set _arr !
    9 { "bar" "blat" }list _arr @ dup 3 pick array_nested_get 4 rotate + swap rot array_nested_set _arr !
    5 4 3 _sub pop
    4 6 2 _arr @ "baz" [] execute pop
    4 6 2 _arr @ "bar" [] "boo" [] execute pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

