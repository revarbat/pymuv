( Generated from test_oper_ternary_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ _arg -- ret ]
    1 if "T" else "F" then
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
