( Generated from test_nested_dump_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _dump[ _arr _indent -- ret ]
    var _key var _val var _out
    "" _out !
    _arr @ foreach
        _val ! _key !
        _val @ array? dup not if pop _val @ dictionary? then if
            _key @ _indent @ "%s%~ => [" fmtstring me @ swap notify 
            _val @ { _indent @ "  " }list array_interpret _dump pop
            _indent @ "%s]" fmtstring me @ swap notify 
        else
            _val @ _key @ _indent @ "%s%~ => %~" fmtstring
            me @ swap notify 
        then
    repeat
    0
;
: _dictfunc[  -- ret ]
    var _mydict var _myvar
    { "one" "First" "two" "Second" "three" "Third" }dict _mydict !
    _mydict @ "" _dump pop
    _mydict @ "two" [] _myvar !
    _myvar @ me @ swap notify 
    "Fifth" dup _mydict @ "five" ->[] _mydict ! pop
    _mydict @ "three" array_delitem _mydict ! 
    0
;
: _main[  -- ret ]
    var _arr var _idx var _word var _empty var _nested
    {
        "First" "Second" "Third" "Forth" "Fifth" "Sixth" "Seventh"
        "Eighth" "Ninth" "Tenth" "Eleventh"
    }list _arr !
    _arr @ foreach
        _word ! pop
        _arr @ _idx @ [] me @ swap notify 
    repeat
    { }list _empty !
    _arr @ foreach
        _word ! _idx !
        me @ _word @ _idx @ "%d: %s" fmtstring notify 
    repeat
    {
        { 1 2 3 4 }list { "a" "b" "c" "d" }list
        { "One" "Two" "Three" "Four" }list
        { { 3 1 4 }list { 9 1 16 }list { 81 1 256 }list }list
    }list _nested !
    _nested @ { 2 1 }list array_nested_get me @ swap notify 
    { "Fee" "Fie" "Foe" "Fum" }list dup
    _nested @ 1 ->[] _nested ! pop
    23 dup _nested @ { 0 3 }list array_nested_set _nested ! pop
    _nested @ { 0 3 }list over over array_nested_get 2 + rot rot array_nested_set _nested !
    _nested @ 0 over over [] "foo" swap []<- rot rot ->[] _nested !
    _nested @ { 3 1 }list over over array_nested_get "foo" swap
    []<- rot rot array_nested_set _nested !
    _nested @ 2 array_delitem _nested ! 
    _nested @ "" _dump pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
