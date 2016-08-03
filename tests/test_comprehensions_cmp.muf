( Generated from test_comprehensions_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    var _k
    var _v
    { 3 4 5 6 7 8 9 }list var! _mylist
    { }list _mylist @ foreach
        _v ! pop
        _v @ _v @ * swap []<-
    repeat var! _squares
    { }list _mylist @ foreach
        _v ! pop
        _v @ 2 % if
            _v @ swap []<-
        then
    repeat var! _odds
    { }list _mylist @ foreach
        _v ! pop
        _v @ 2 % not if
            _v @ swap []<-
        then
    repeat var! _evens
    { "a" 1 "b" 2 "c" 3 "d" 4 }dict var! _mydict
    { }dict _mydict @ foreach
        _v ! _k !
        _k @ _v @ _v @ * rot rot ->[]
    repeat var! _squarevals
    { }dict _mydict @ foreach
        _v ! _k !
        _k @ "b" strcmp 0 > if
            _k @ _v @ _v @ * rot rot ->[]
        then
    repeat var! _foo
    { }dict _mydict @ foreach
        _v ! _k !
        _v @ 2 > not if
            _k @ _v @ _v @ * rot rot ->[]
        then
    repeat var! _bar
    var _obj
    { }list loc @ contents_array foreach
        _obj ! pop
        _obj @ player? dup if pop
            _obj @ awake?
        then if
            _obj @ name swap []<-
        then
    repeat var! _listeners
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

