( Generated from test_literal_string_variants_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _quotes[ _arg -- ret ]
    var _a var _b var _c var _d var _e var _f var _g var _h
    var _i var _j var _k var _l var _m var _n var _o
    "Test('')" _a !
    "Test(\"\")" _b !
    "Test(\"\")" _c !
    "Test(\"\")" _d !
    "it's" _e !
    "it's" _f !
    "a\"b" _g !
    "a'b" _h !
    "abc\"def" _i !
    "abc\r               def" _j !
    "abc'def" _k !
    "abc\\rdef" _l !
    "abc\\rdef" _m !
    "abc\"\\r'def" _n !
    "abc\"\\r'def" _o !
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _quotes
;
