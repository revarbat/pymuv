( Generated from test_oper_logical_and_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    1 dup if pop
        1
    then
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
