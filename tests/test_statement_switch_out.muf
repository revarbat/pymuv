( Generated from test_statement_switch_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )

: _complex_match[ _v1 _v2 -- ret ]
    _v1 @ number? dup if pop
        _v2 @ number?
    then if
        _v1 @ _v2 @ = exit
    then
    _v1 @ string? dup if pop
        _v2 @ int?
    then if
        _v1 @ _v2 @ intostr strcmp not exit
    then
    _v1 @ "%?" fmtstring _v2 @ "%?" fmtstring strcmp not if
        0 exit
    then
    _v1 @ string? if
        _v1 @ tolower _v2 @ tolower strcmp not exit
    then
    0
;
: _main[ _arg -- ret ]
    2 var! _i
    _i @ var! _swvar
    begin
        _swvar @ 1 "=" if
            "One." me @ swap notify
        then
        _swvar @ 2 "=" if
            "Two." me @ swap notify
        then
        _swvar @ 3 "=" if
            "Three." me @ swap notify
        then
    repeat
    _arg @ var! _swvar2
    begin
        _swvar2 @ "greet" strcmp if
            "Hello." me @ swap notify
        then
        _swvar2 @ "who" strcmp if
            "I'm called MUV." me @ swap notify
        then
        _swvar2 @ "what" strcmp if
            "I'm a nicer language to use than MUF." me @ swap notify
        then
        "I don't understand." me @ swap notify break
    repeat
    _arg @ var! _swvar3
    begin
        _swvar3 @ "fee" complex_match if
            "Fee selected!" me @ swap notify
        then
        _swvar3 @ 1 complex_match if
            "One selected!" me @ swap notify
        then
        _swvar3 @ "" complex_match if
            "None selected!" me @ swap notify
        then
    repeat
    "foo" var! _a
    42 var! _swvar4
    begin
        _swvar4 @ 99 > if
            "A" me @ swap notify
        then
        _swvar4 @ 50 > if
            "B" me @ swap notify
        then
        _swvar4 @ 25 > if
            "C" me @ swap notify
        then
        _swvar4 @ 10 > if
            "D" me @ swap notify
        then
    repeat
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

