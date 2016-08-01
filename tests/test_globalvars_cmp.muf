( Generated from test_globalvars_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
lvar _foo
lvar _bar
lvar _fee
: _main[ _arg -- ret ]
    { _foo @ " " _bar @ }list array_interpret _fee !
    _fee @ me @ swap notify 
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    23 _foo !
    43 _bar !
    _main
;
