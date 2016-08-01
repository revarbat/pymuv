( Generated from test_oper_logical_or_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    1 dup not if pop
        1
    then
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

