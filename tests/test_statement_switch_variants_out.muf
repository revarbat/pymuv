( Generated from test_statement_switch_variants_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _a -- ret ]
    _a @ var! _swvar
    begin
        _swvar @ "1" strcmp not if
            "One" me @ swap notify break
        then
        _swvar @ "2" strcmp not if
            "Two" me @ swap notify break
        then
    repeat
    _a @ var! _swvar2
    begin
        _swvar2 @ "1" stringcmp not if
            "One" me @ swap notify break
        then
        _swvar2 @ "2" stringcmp not if
            "Two" me @ swap notify break
        then
    repeat
    _a @ var! _swvar3
    begin
        _swvar3 @ "1" strcmp not if
            "One" me @ swap notify break
        then
        _swvar3 @ "2" strcmp not if
            "Two" me @ swap notify break
        then
    repeat
    3 var! _swvar4
    begin
        _swvar4 @ 1 = if
            "One" me @ swap notify break
        then
        _swvar4 @ 2 = if
            "Two" me @ swap notify break
        then
    repeat
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
