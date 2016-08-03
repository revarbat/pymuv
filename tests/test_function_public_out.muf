( Generated from test_function_public_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: loopy[ _count -- ret ]
    { "foo" "bar" "baz" }list var! _l
    _l @ foreach
        var! _v pop
        _v @ me @ swap notify
    repeat
    _l @ foreach
        var! _l2 pop
        _l2 @ var! _l3
        _l3 @ me @ swap notify
    repeat
    0
;
public loopy
$libdef loopy
: __start
    "me" match me ! me @ location loc ! trig trigger !
    loopy
;
