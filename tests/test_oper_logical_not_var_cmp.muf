( Generated from test_oper_logical_not_var_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    0 var! _opts
    _opts @ not if
        exit
    then
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
