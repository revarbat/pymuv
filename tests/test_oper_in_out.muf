( Generated from test_oper_in_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    3 { 2 3 4 5 }list swap array_findval
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
