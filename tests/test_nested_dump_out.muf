( Generated from test_nested_dump_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )

: _dump[ _arr _indent -- ret ]
    var _key
    var _val
    "" var! _out
    _arr @ foreach
        _val ! _key !
        _val @ array? dup not if pop
            _val @ dictionary?
        then if
            _key @ _indent @ "%s%~ => [" fmtstring me @ swap notify
            _val @ { _indent @ "" }list array_interpret _dump pop
            _indent @ "%s]" fmtstring me @ swap notify
        else
            _val @ _key @ _indent @ "%s%~ => %~" fmtstring me @ swap notify
        then
    repeat
    0
;
: _dictfunc[ -- ret ]
    { "one" "First" "two" "Second" "three" "Third" }dict var! _mydict
    _mydict @ "" _dump pop
    _mydict @ "two" [] var! _myvar
    _myvar @ me @ swap notify
    "Fifth" _mydict @ "five" ->[] _mydict !
    _mydict @ "three" array_delitem _mydict ! pop
    0
;
: _main[ -- ret ]
    { "First" "Second" "Third" "Forth" "Fifth" "Sixth" "Seventh" "Eighth" "Ninth" "Tenth" "Eleventh" }list var! _arr
    var _idx
    var _word
    _arr @ foreach
        _word ! pop
        _arr @ _idx @ [] me @ swap notify
    repeat
    { }list var! _empty
    _arr @ foreach
        _word ! _idx !
        me @ _word @ _idx @ "%d: %s" fmtstring notify
    repeat
    { { 1 2 3 4 }list { "a" "b" "c" "d" }list { "One" "Two" "Three" "Four" }list { { 3 1 4 }list { 9 1 16 }list { 81 1 256 }list }list }list var! _nested
    _nested @ 2 [] 1 [] me @ swap notify
    { "Fee" "Fie" "Foe" "Fum" }list _nested @ 1 ->[] _nested !
    23 _nested @ { 0 3 }list array_nested_set _nested !
    2 { 0 3 }list _nested @ dup 3 pick array_nested_get 4 rotate + swap rot array_nested_set _nested !
    "foo" 0 _nested @ dup 3 pick [] 4 rotate swap []<- swap rot ->[] _nested !
    "foo" { 3 1 }list _nested @ dup 3 pick array_nested_get 4 rotate swap []<- swap rot array_nested_set _nested !
    _nested @ 2 array_delitem _nested ! pop
    _nested @ "" _dump pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

