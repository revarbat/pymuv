( Generated from test_statement_try_catch_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _trys[ -- ret ]
    var _bar
    0 try
        me @ desc _bar !
    catch_detailed var! _err
        _err @ me @ swap notify
    endcatch
    0 try
        me @ osucc _bar !
    catch_detailed pop

    endcatch
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _trys
;

