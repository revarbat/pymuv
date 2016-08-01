
( Generated from test_externs_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _main[ -- ret ]
    var _v
    voidfoo 0 _v !
    singlefoo _v !
    { multfoo }list _v !
    qux _v !
    { "Fee" "Fie" "Foe" }list array_interpret _v !
    "%d: %s" { 5 "Fum" }list 2 try
        array_explode 1 + rotate fmtstring
        depth 0 swap - rotate depth 1 - popn
    catch abort
    endcatch _v !
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;

