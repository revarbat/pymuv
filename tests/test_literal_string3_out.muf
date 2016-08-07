( Generated from test_literal_string3_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    "This\ris\ra\rtest" var! _foo
    { _foo @ "Hello \\World!\r" "\[[1;" "Hello, \"" _arg @ "\"!" "\[[0;\r" "Hello All!" }list array_interpret me @ swap notify
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
