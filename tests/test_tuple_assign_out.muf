( Generated from test_tuple_assign_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )


: _gen[ -- ret ]
    0 var! _i
    { }list var! _out
    begin
        _i @ 4 <
    while
        { "Fee" "Fie" "Foe" "Fum" }list _i @ [] _out @ []<- _out !
        _i ++ pop
    repeat
    _out @
;
: _listgen[ -- ret ]
    { }list var! _out
    0 var! _i
    begin
        _i ++ 10 <
    while
        _gen _out @ []<- _out !
    repeat
    _out @
;
: _main[ _arg -- ret ]
    _gen 0 3 [..] array_vals pop
    var! _d var! _c var! _b var! _a
    _gen 0 3 [..] array_vals pop
    _a ! _b ! _c ! _d !
    _listgen foreach
        0 3 [..] array_vals pop
        _d ! _c ! _b ! _a ! pop
        { _a @ _b @ }list array_interpret me @ swap notify
    repeat
    { }list _listgen foreach
        0 3 [..] array_vals pop
        _d ! _c ! _b ! _a ! pop
        _a @ _b @ strcmp if
            { _c @ _d @ }list array_interpret swap []<-
        then
    repeat
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

