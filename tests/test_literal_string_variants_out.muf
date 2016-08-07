( Generated from test_literal_string_variants_in.muv by the MUV compiler. )
(   https://github.com/revarbat/pymuv )

: _main[ _arg -- ret ]
    " ab " pop
    "a'b" pop
    "a\"b" pop
    "a\rb" pop
    "a\[b" pop
    "a'b" pop
    "a\\rb" pop
    " ab " pop
    "a\"b" pop
    "a'b)" pop
    "a\rb" pop
    "a\[b" pop
    "a\"b" pop
    "a\\rb" pop
    " ab " pop
    "a'b" pop
    "a\"b" pop
    "a\rb" pop
    "a\[b" pop
    " ab " pop
    "a\"b" pop
    "a\\rb" pop
    "a\r       b" pop
    " ab " pop
    "a'b" pop
    "a\"b" pop
    "a\rb" pop
    "a\[b" pop
    " ab " pop
    "a\"b" pop
    "a\\rb" pop
    "a\r       b" pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    _main
;
