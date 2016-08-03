( Generated from test_namespace_consts_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    reg_all
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

