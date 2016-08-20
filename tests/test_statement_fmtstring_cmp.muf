( Generated from test_statement_fmtstring_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    "foof" 8 "%*s." fmtstring
;

: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
