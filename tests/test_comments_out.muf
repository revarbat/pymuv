( Generated from test_comments_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
: _helloworld[ -- ret ]
    "Hello Harold!" me @ swap notify
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _helloworld
;

