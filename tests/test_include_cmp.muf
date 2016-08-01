( Generated from test_include_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _bass[  -- ret ]
    "THUMP!"
;
: _foof[ _arg -- ret ]
    _bass
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _foof
;
