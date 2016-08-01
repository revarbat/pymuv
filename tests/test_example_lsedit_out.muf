( Generated from test_example_lsedit_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )





lvar argparse__current_mode
lvar argparse__modes_list
lvar argparse__flags_map
lvar argparse__posargs_map
lvar argparse__remainder_map
: argparse__init[ -- ret ]
    "" argparse__current_mode !
    { }list argparse__modes_list !
    { }dict argparse__flags_map !
    { }dict argparse__posargs_map !
    { "" "remainder" }dict argparse__remainder_map !
    0
;
: argparse__parse_posargs[ _mode _posargs -- ret ]
    begin
        { _posargs @ "^([a-z0-9_]*)([^a-z0-9_])(.*)$" 1 regexp }list 0 [] var! _tok
        _tok @ if
            argparse__posargs_map @ _mode @ [] not if
                { }list argparse__posargs_map @ _mode @ ->[] argparse__posargs_map !
            then
            { _tok @ 1 [] tolower _tok @ 2 [] }list _mode @ argparse__posargs_map @ dup 3 pick [] 4 rotate swap []<- swap rot ->[] argparse__posargs_map !
            _tok @ 3 [] _posargs !
        else
            _posargs @ tolower argparse__remainder_map @ _mode @ ->[] argparse__remainder_map !
            break
        then
        1 not
    until
    0
;
: argparse__set_mode[ _name -- ret ]
    _name @ tolower _name !
    _name @ argparse__current_mode !
    0
;
: argparse__add_mode[ _name _flags _posargs -- ret ]
    _name @ tolower _name !
    _name @ argparse__modes_list @ []<- argparse__modes_list !
    { }list argparse__flags_map @ _name @ ->[] argparse__flags_map !
    { }list argparse__posargs_map @ _name @ ->[] argparse__posargs_map !
    _flags @ foreach
        var! _flag pop
        argparse__flags_map @ _name @ [] not if
            { }list argparse__flags_map @ _name @ ->[] argparse__flags_map !
        then
        _flag @ tolower _name @ argparse__flags_map @ dup 3 pick [] 4 rotate swap []<- swap rot ->[] argparse__flags_map !
    repeat
    _name @ _posargs @ argparse__parse_posargs pop
    0
;
: argparse__add_flag[ _name -- ret ]
    _name @ tolower _name !
    argparse__modes_list @ foreach
        var! _mode pop
        _mode @ tolower _mode !
        argparse__modes_list @ _mode @ array_findval not if
            _mode @ _name @ "ArgParse: Option '%s' declared as part of non-existent mode '%s'!" fmtstring abort
        then
        argparse__flags_map @ _mode @ [] not if
            { }list argparse__flags_map @ _mode @ ->[] argparse__flags_map !
        then
        _name @ _mode @ argparse__flags_map @ dup 3 pick [] 4 rotate swap []<- swap rot ->[] argparse__flags_map !
    repeat
    0
;
: argparse__add_posargs[ _posargs -- ret ]
    argparse__modes_list @ foreach
        var! _mode pop
        _mode @ tolower _mode !
        argparse__modes_list @ _mode @ array_findval not if
            _mode @ _mode @ "ArgParse: Option '%s' declared as part of non-existent mode '%s'!" fmtstring abort
        then
        _mode @ _posargs @ argparse__parse_posargs pop
    repeat
    0
;
: argparse__show_usage[ -- ret ]
    trig name ";" split pop strip var! _cmd
    "Usage:" me @ swap notify
    argparse__modes_list @ foreach
        var! _mode pop
        { }list argparse__flags_map @ _mode @ [] foreach
            var! _flag pop
            { "[#" _flag @ "]" }list array_interpret swap []<-
        repeat var! _flags
        { }list argparse__posargs_map @ _mode @ [] foreach
            var! _posarg pop
            { _posarg @ 0 [] toupper _posarg @ 1 [] }list array_interpret swap []<-
        repeat var! _posargs
        argparse__remainder_map @ _mode @ [] toupper _posargs @ "" array_join _flags @ if
            ""
        else
            ""
        then _flags @ "" array_join _mode @ _mode @ if
            "#"
        else
            ""
        then _cmd @ "%s %s%s %s%s%s%s" fmtstring var! _line
        _line @ me @ swap notify
    repeat
    0
;
: argparse__parse[ _line -- ret ]
    var _parts
    var _mode
    var _flag
    { }dict var! _opts
    0 var! _mode_given
    begin
        _line @ "#" stringpfx
    while
        { { _line @ 1 strcut }list 1 [] "" split }list _parts !
        _parts @ 0 [] var! _opt
        _opt @ tolower var! _lc_opt
        0 var! _found
        argparse__modes_list @ foreach
            _mode ! pop
            _mode @ _lc_opt @ stringcmp not if
                _mode @ argparse__current_mode !
                _found ++ pop
                break
            then
        repeat
        _found @ if
            _mode_given ++ pop
            _parts @ 1 [] _line !
            continue
        then
        argparse__flags_map @ argparse__current_mode @ [] foreach
            _flag ! pop
            _flag @ _lc_opt @ stringcmp not if
                _opt @ _opts @ _flag @ ->[] _opts !
                _found ++ pop
                break
            then
        repeat
        _found @ if
            _parts @ 1 [] _line !
            continue
        then
        argparse__modes_list @ foreach
            _mode ! pop
            _mode @ _lc_opt @ stringpfx if
                _mode @ argparse__current_mode !
                _found ++ pop
            then
        repeat
        argparse__flags_map @ argparse__current_mode @ [] foreach
            _flag ! pop
            _flag @ _lc_opt @ stringpfx if
                _opt @ _opts @ _flag @ ->[] _opts !
                _found ++ pop
            then
        repeat
        _found @ 1 = if
            _parts @ 1 [] _line !
            continue
        else
            _found @ 1 > if
                _opt @ "Option #%s is ambiguous." fmtstring me @ swap notify
            else
                _opt @ "Option #%s not recognized." fmtstring me @ swap notify
            then
        then
        argparse__show_usage pop
        { }list exit
    repeat
    _mode_given @ 1 > if
        "Cannot mix modes." me @ swap notify
        argparse__show_usage pop
        { }list exit
    then
    argparse__posargs_map @ argparse__current_mode @ [] foreach
        var! _posarg pop
        { _line @ _posarg @ 1 [] split }list _parts !
        _parts @ 0 [] _opts @ _posarg @ 0 [] ->[] _opts !
        _parts @ 1 [] _line !
    repeat
    _line @ _opts @ argparse__remainder_map @ argparse__current_mode @ [] ->[] _opts !
    argparse__current_mode @ _opts @ "mode" ->[] _opts !
    _opts @
;

