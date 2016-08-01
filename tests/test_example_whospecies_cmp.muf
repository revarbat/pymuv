( Generated from test_example_whospecies_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )



: _showspecies[ -- ret ]
    loc @ contents_array foreach
        var! _obj pop
        _obj @ player? if
            _obj @ "species" getpropstr _obj @ "sex" getpropstr _obj @ "%-30D %-10s %-30s" fmtstring me @ swap notify
        then
    repeat
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _showspecies
;

