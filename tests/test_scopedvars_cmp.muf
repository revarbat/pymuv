( Generated from test_scopedvars_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _loopy[ _count -- ret ]
    var _l var _v var _l2 var _l3
    { "foo" "bar" "baz" }list _l !
    _l @ foreach
        _v ! pop
        _v @ me @ swap notify 
    repeat
    _l @ foreach
        _l2 ! pop
        _l2 @ _l3 !
        _l3 @ me @ swap notify 
    repeat
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _loopy
;
