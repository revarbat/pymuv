( Generated from test_statement_switch_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _complex_match[ _v1 _v2 -- ret ]
    _v1 @ number? dup if pop _v2 @ number? then if
        _v1 @ _v2 @ = exit
    then
    _v1 @ string? dup if pop _v2 @ int? then if
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
    var _i var _a
    2 _i !
    0 begin pop (switch)
        _i @
        dup 1 = if "One." me @ swap notify  break then
        dup 2 = if "Two." me @ swap notify  break then
        dup 3 = if "Three." me @ swap notify  break then
        break
    repeat pop
    0 begin pop (switch)
        _arg @
        dup "greet" strcmp not if
            "Hello." me @ swap notify  break
        then
        dup "who" strcmp not if
            "I'm called MUV." me @ swap notify  break
        then
        dup "what" strcmp not if
            "I'm a nicer language to use than MUF." me @ swap notify 
            break
        then
        (default)
        "I don't understand." me @ swap notify  break
    repeat pop
    0 begin pop (switch)
        _arg @
        dup "fee" _complex_match if
            "Fee selected!" me @ swap notify  break
        then
        dup 1 _complex_match if
            "One selected!" me @ swap notify  break
        then
        dup "" _complex_match if
            "None selected!" me @ swap notify  break
        then
        break
    repeat pop
    "foo" _a !
    0 begin pop (switch)
        42
        dup 99 > if "A" me @ swap notify  break then
        dup 50 > if "B" me @ swap notify  break then
        dup 25 > if "C" me @ swap notify  break then
        dup 10 > if "D" me @ swap notify  break then
        break
    repeat pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
