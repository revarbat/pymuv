( Generated from test_tuple_assign_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _gen[  -- ret ]
    var _i var _out
    0 _i !
    { }list _out !
    begin
        _i @ 4 <
    while
        _out @ { "Fee" "Fie" "Foe" "Fum" }list _i @ [] swap []<- _out !
        _i ++
    repeat
    _out @
;
: _listgen[  -- ret ]
    var _out var _i
    { }list _out !
    0 _i !
    begin
        _i @ dup ++ _i ! 10 <
    while
        _out @ _gen swap []<- _out !
    repeat
    _out @
;
: _main[ _arg -- ret ]
    var _a var _b var _c var _d
    _gen dup
    dup 0 [] _a ! dup 1 [] _b ! dup 2 [] _c ! dup 3 [] _d ! pop pop
    _gen dup
    dup 0 [] _d ! dup 1 [] _c ! dup 2 [] _b ! dup 3 [] _a ! pop pop
    _listgen foreach
        dup 0 [] _a ! dup 1 [] _b ! dup 2 [] _c ! dup 3 [] _d ! pop
        pop
        { _a @ _b @ }list array_interpret me @ swap notify 
    repeat
    { }list _listgen foreach
        dup 0 [] _a ! dup 1 [] _b ! dup 2 [] _c ! dup 3 [] _d ! pop
    pop
        _a @ _b @ strcmp if
            { _c @ _d @ }list array_interpret swap []<-
        then
    repeat
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
