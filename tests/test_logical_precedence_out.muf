( Generated from test_logical_precedence_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    1 dup not if pop
        2 dup if pop
            3 not
        then
    then
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
