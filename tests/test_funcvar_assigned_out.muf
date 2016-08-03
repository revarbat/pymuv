( Generated from test_funcvar_assigned_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )
: _main[ _arg -- ret ]
    42 var! _a
    _a @
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
