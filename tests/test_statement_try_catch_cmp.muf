( Generated from test_statement_try_catch_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _trys[  -- ret ]
    var _bar var _err
    0 try
        me @ desc _bar !
    catch_detailed _err !
        _err @ me @ swap notify 
    endcatch
    0 try me @ osucc _bar ! catch pop  endcatch
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _trys
;
