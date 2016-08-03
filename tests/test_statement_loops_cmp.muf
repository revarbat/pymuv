( Generated from test_statement_loops_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _loopy[ _count -- ret ]
    1 var! _i
    begin
        _i @ _count @ > not
    while
        _i @ intostr me @ swap notify
        _i ++
    repeat
    1 _i !
    begin
        _i @ _count @ <=
    while
        _i @ intostr me @ swap notify
        _i ++
    repeat
    1 _i !
    begin
        _i @ intostr me @ swap notify
        _i ++
        _i @ _count @ <= not
    until
    1 _i !
    begin
        _i @ intostr me @ swap notify
        _i ++
        _i @ _count @ >
    until
    1 _count @ 1 for
        var! _i2
        _i2 @ intostr me @ swap notify
    repeat
    _count @ 1 -1 for
        var! _i3
        _i3 @ intostr me @ swap notify
    repeat
    online_array foreach
        var! _val pop
        _val @ "%D" fmtstring me @ swap notify
    repeat
    online_array foreach
        var! _val2 var! _key
        { _key @ "= " _val2 @ }list array_interpret me @ swap notify
    repeat
    0
;
: _main[ -- ret ]
    10 _loopy pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

