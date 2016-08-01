( Generated from test_example_listedit_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
lvar argparse::current_mode
lvar argparse::modes_list
lvar argparse::flags_map
lvar argparse::posargs_map
lvar argparse::remainder_map
: argparse::init[  -- ret ]
    "" argparse::current_mode !
    { }list argparse::modes_list !
    { }dict argparse::flags_map !
    { }dict argparse::posargs_map !
    { "" "remainder" }dict argparse::remainder_map !
    0
;
: argparse::parse_posargs[ _mode _posargs -- ret ]
    var _tok
    begin
        { _posargs @ "^([a-z0-9_]*)([^a-z0-9_])(.*)$" 1 regexp }list 0 []
        _tok !
        _tok @ if
            argparse::posargs_map @ _mode @ [] not if
                { }list dup
                argparse::posargs_map @ _mode @ ->[] argparse::posargs_map ! pop
            then
            argparse::posargs_map @ _mode @ over over []
            { _tok @ 1 [] tolower _tok @ 2 [] }list swap []<- rot rot ->[] argparse::posargs_map !
            _tok @ 3 [] _posargs !
        else
            _posargs @ tolower dup
            argparse::remainder_map @ _mode @ ->[] argparse::remainder_map ! pop
            break
        then
    repeat
    0
;
: argparse::set_mode[ _name -- ret ]
    _name @ tolower _name !
    _name @ argparse::current_mode !
    0
;
: argparse::add_mode[ _name _flags _posargs -- ret ]
    var _flag
    _name @ tolower _name !
    argparse::modes_list @ _name @ swap []<- argparse::modes_list !
    { }list dup
    argparse::flags_map @ _name @ ->[] argparse::flags_map ! pop
    { }list dup
    argparse::posargs_map @ _name @ ->[] argparse::posargs_map ! pop
    _flags @ foreach
        _flag ! pop
        argparse::flags_map @ _name @ [] not if
            { }list dup
            argparse::flags_map @ _name @ ->[] argparse::flags_map ! pop
        then
        argparse::flags_map @ _name @ over over [] _flag @ tolower
        swap []<- rot rot ->[] argparse::flags_map !
    repeat
    _name @ _posargs @ argparse::parse_posargs pop
    0
;
: argparse::add_flag[ _name -- ret ]
    var _mode
    _name @ tolower _name !
    argparse::modes_list @ foreach
        _mode ! pop
        _mode @ tolower _mode !
        argparse::modes_list @ _mode @ array_findval not if
            _mode @ _name @
            "ArgParse: Option '%s' declared as part of non-existent mode '%s'!"
            fmtstring abort 
        then
        argparse::flags_map @ _mode @ [] not if
            { }list dup
            argparse::flags_map @ _mode @ ->[] argparse::flags_map ! pop
        then
        argparse::flags_map @ _mode @ over over [] _name @ swap []<-
        rot rot ->[] argparse::flags_map !
    repeat
    0
;
: argparse::add_posargs[ _posargs -- ret ]
    var _mode
    argparse::modes_list @ foreach
        _mode ! pop
        _mode @ tolower _mode !
        argparse::modes_list @ _mode @ array_findval not if
            _mode @ _mode @
            "ArgParse: Option '%s' declared as part of non-existent mode '%s'!"
            fmtstring abort 
        then
        _mode @ _posargs @ argparse::parse_posargs pop
    repeat
    0
;
: argparse::show_usage[  -- ret ]
    var _cmd var _mode var _flags var _flag var _posargs
    var _posarg var _line
    trig name ";" split pop strip _cmd !
    "Usage:" me @ swap notify 
    argparse::modes_list @ foreach
        _mode ! pop
        { }list argparse::flags_map @ _mode @ [] foreach
            _flag ! pop
            { "[#" _flag @ "]" }list array_interpret swap []<-
        repeat _flags !
        { }list argparse::posargs_map @ _mode @ [] foreach
            _posarg ! pop
            { _posarg @ 0 [] toupper _posarg @ 1 [] }list array_interpret
            swap []<-
        repeat _posargs !
        argparse::remainder_map @ _mode @ [] toupper
        _posargs @ "" array_join _flags @ if " " else "" then
        _flags @ " " array_join _mode @ _mode @ if "#" else "" then
        _cmd @ "%s %s%s %s%s%s%s" fmtstring _line !
        _line @ me @ swap notify 
    repeat
    0
;
: argparse::parse[ _line -- ret ]
    var _parts var _mode var _flag var _opts var _mode_given
    var _opt var _lc_opt var _found var _posarg
    { }dict _opts !
    0 _mode_given !
    begin
        _line @ "#" stringpfx
    while
        { { _line @ 1 strcut }list 1 [] " " split }list _parts !
        _parts @ 0 [] _opt !
        _opt @ tolower _lc_opt !
        0 _found !
        argparse::modes_list @ foreach
            _mode ! pop
            _mode @ _lc_opt @ stringcmp not if
                _mode @ argparse::current_mode !
                _found ++
                break
            then
        repeat
        _found @ if
            _mode_given ++
            _parts @ 1 [] _line !
            continue
        then
        argparse::flags_map @ argparse::current_mode @ [] foreach
            _flag ! pop
            _flag @ _lc_opt @ stringcmp not if
                _opt @ dup _opts @ _flag @ ->[] _opts ! pop
                _found ++
                break
            then
        repeat
        _found @ if
            _parts @ 1 [] _line !
            continue
        then
        argparse::modes_list @ foreach
            _mode ! pop
            _mode @ _lc_opt @ stringpfx if
                _mode @ argparse::current_mode !
                _found ++
            then
        repeat
        argparse::flags_map @ argparse::current_mode @ [] foreach
            _flag ! pop
            _flag @ _lc_opt @ stringpfx if
                _opt @ dup _opts @ _flag @ ->[] _opts ! pop
                _found ++
            then
        repeat
        _found @ 1 = if
            _parts @ 1 [] _line !
            continue
        else
            _found @ 1 > if
                _opt @ "Option #%s is ambiguous." fmtstring me @ swap notify 
            else
                _opt @ "Option #%s not recognized." fmtstring
                me @ swap notify 
            then
        then
        argparse::show_usage pop
        { }list exit
    repeat
    _mode_given @ 1 > if
        "Cannot mix modes." me @ swap notify 
        argparse::show_usage pop
        { }list exit
    then
    argparse::posargs_map @ argparse::current_mode @ [] foreach
        _posarg ! pop
        { _line @ _posarg @ 1 [] split }list _parts !
        _parts @ 0 [] dup _opts @ _posarg @ 0 [] ->[] _opts ! pop
        _parts @ 1 [] _line !
    repeat
    _line @ dup
    _opts @ argparse::remainder_map @ argparse::current_mode @ [] ->[] _opts ! pop
    argparse::current_mode @ dup _opts @ "mode" ->[] _opts ! pop
    _opts @
;
: _verify[ _override _msg -- ret ]
    _override @ if 1 exit then
    { "Are you sure you want to " _msg @ "?" }list
    array_interpret me @ swap notify 
    { read 1 strcut }list 0 [] "y" stringcmp not if 1 exit then
    "Cancelled." me @ swap notify 
    0
;
: _handle_mode_list[ _obj _prop -- ret ]
    var _lines var _i var _line
    _obj @ _prop @ array_get_proplist _lines !
    _lines @ foreach
        _line ! _i !
        _line @ _i @ ++ "%3i: %s" fmtstring me @ swap notify 
    repeat
    "Done." me @ swap notify 
    0
;
: _handle_mode_append[ _obj _prop _val _force -- ret ]
    var _lines
    _val @ not if
        argparse::show_usage pop
        0 exit
    then
    _force @ "append a line to the list" _verify if
        _obj @ _prop @ array_get_proplist _lines !
        _lines @ _val @ swap []<- _lines !
        _obj @ _prop @ _lines @ array_put_proplist 
        "Line appended." me @ swap notify 
        _obj @ _prop @ _handle_mode_list pop
    then
    0
;
: _handle_mode_delete[ _obj _prop _pos _force -- ret ]
    var _lines
    _pos @ atoi _pos !
    _pos @ not if
        argparse::show_usage pop
        0 exit
    then
    _force @ "delete a line from the list" _verify if
        _obj @ _prop @ array_get_proplist _lines !
        _lines @ _pos @ -- array_delitem _lines !
        _obj @ _prop @ _lines @ array_put_proplist 
        "Line deleted." me @ swap notify 
        _obj @ _prop @ _handle_mode_list pop
    then
    0
;
: _handle_mode_insert[ _obj _prop _pos _val _force -- ret ]
    var _lines
    _pos @ atoi _pos !
    _pos @ not dup not if pop _val @ not then if
        argparse::show_usage pop
        0 exit
    then
    _force @ "insert a line into the list" _verify if
        _obj @ _prop @ array_get_proplist _lines !
        _val @ _lines @ _pos @ -- array_insertitem _lines !
        _obj @ _prop @ _lines @ array_put_proplist 
        "Line inserted." me @ swap notify 
        _obj @ _prop @ _handle_mode_list pop
    then
    0
;
: _handle_mode_replace[ _obj _prop _pos _val _force -- ret ]
    var _lines
    _pos @ atoi _pos !
    _pos @ not dup not if pop _val @ not then if
        argparse::show_usage pop
        0 exit
    then
    _force @ "replace a line in the list" _verify if
        _obj @ _prop @ array_get_proplist _lines !
        _lines @ _pos @ -- array_delitem _lines !
        _val @ _lines @ _pos @ -- array_insertitem _lines !
        _obj @ _prop @ _lines @ array_put_proplist 
        "Line inserted." me @ swap notify 
        _obj @ _prop @ _handle_mode_list pop
    then
    0
;
: _main[ _arg -- ret ]
    var _opts var _obj
    argparse::init pop
    "list" argparse::set_mode pop
    "list" { }list "obj=prop" argparse::add_mode pop
    "append" { "force" }list "obj=prop:val" argparse::add_mode pop
    "delete" { "force" }list "obj=prop:pos" argparse::add_mode pop
    "insert" { "force" }list "obj=prop:pos:val"
    argparse::add_mode pop
    "replace" { "force" }list "obj=prop:pos:val"
    argparse::add_mode pop
    "verbose" argparse::add_flag pop
    _arg @ argparse::parse _opts !
    _opts @ not if 0 exit then
    _opts @ "obj" [] not
    dup not if pop _opts @ "prop" [] not then if
        argparse::show_usage pop
        0 exit
    then
    _opts @ "obj" [] match
    dup #-1 dbcmp if me @ "I don't see that here!" notify then
    dup #-2 dbcmp if me @ "I don't know which one you mean!" notify then
    dup #-3 dbcmp if pop me @ getlink then
    dup ok? if
        me @ over controls not if
            pop #-1 me @ "Permission denied." notify
        then
    then _obj !
    _obj @ 0 < if 0 exit then
    _opts @ "verbose" [] if
        { "Mode = " _opts @ "mode" [] }list array_interpret
        me @ swap notify 
    then
    0 begin pop (switch)
        _opts @ "mode" []
        dup "list" strcmp not if
            _obj @ _opts @ "prop" [] _handle_mode_list pop break
        then
        dup "append" strcmp not if
            _obj @ _opts @ "prop" [] _opts @ "val" [] _opts @ "force" []
            _handle_mode_append pop break
        then
        dup "delete" strcmp not if
            _obj @ _opts @ "prop" [] _opts @ "pos" [] _opts @ "force" []
            _handle_mode_delete pop break
        then
        dup "insert" strcmp not if
            _obj @ _opts @ "prop" [] _opts @ "pos" [] _opts @ "val" []
            _opts @ "force" [] _handle_mode_insert pop break
        then
        dup "replace" strcmp not if
            _obj @ _opts @ "prop" [] _opts @ "pos" [] _opts @ "val" []
            _opts @ "force" [] _handle_mode_replace pop break
        then
        break
    repeat pop
    0
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    "" argparse::current_mode !
    { }list argparse::modes_list !
    { }dict argparse::flags_map !
    { }dict argparse::posargs_map !
    { "" "remainder" }dict argparse::remainder_map !
    _main
;
