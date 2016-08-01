( Generated from test_example_lsedit_in.muv by the MUV compiler. )
(   https://github.com/revarbat/muv )
$author Revar Desmera <revar@gmail.com>
$note An example replacement for the lsedit program, written in MUV.
$version 1.0
$lib-version 1.0
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
lvar lsedit::help_lines
lvar lsedit::insert_pos
: lsedit__init_help[  -- ret ]
    { }list lsedit::help_lines !
    0
;
public lsedit__init_help
$libdef lsedit__init_help
: lsedit__show_help[  -- ret ]
    var _line
    {
        {
            "-- Commands: -----------------------------------------------------"
            "..LINE              Insert .LINE at current insertion position."
            ".h                  Show this help message."
            ".q                  Quit editor, saving changes."
            ".x                  Quit editor, aborting changes."
            ".l                  List all lines."
            ".l LINE             List given LINE."
            ".l LINE,LINE        List given LINE range, inclusive."
            ".i LINE             Move insertion to before LINE."
            ".d LINE             Delete LINE."
            ".d LINE,LINE        Delete given LINE range, inclusive."
            ".f                  Format all lines to 75 columns."
            ".f LINE,LINE        Format given line range to 75 columns."
            ".f LINE,LINE=COLS   Format given line range to COLS columns."
            ".s /FIND/REPL       Substitute regexp FIND with REPL in all lines."
            ".s LINE/FIND/REPL   Substitute regexp FIND with REPL in LINE."
            ".s L1,L2/FIND/REPL  Substitute FIND with REPL between L1 and L2."
            ".w                  Write/Save changes without exiting editor."
            ".w OBJ=PROP         Write/Save list to OBJ in proplist PROP."
        }list lsedit::help_lines @
        {
            "------------------------------------------------------------------"
        }list
    }list
    { }list swap array_reverse foreach swap pop 0 swap array_insertrange repeat
    foreach
        _line ! pop
        _line @ me @ swap notify 
    repeat
    0
;
public lsedit__show_help
$libdef lsedit__show_help
: lsedit__add_helptext[ _line -- ret ]
    lsedit::help_lines @ _line @ swap []<- lsedit::help_lines !
    0
;
public lsedit__add_helptext
$libdef lsedit__add_helptext
: lsedit::show_list[ _lines _start _end _pos -- ret ]
    var _lnum var _line
    _lines @ foreach
        _line ! _lnum !
        _lnum ++
        _lnum @ _start @ >= dup if pop _lnum @ _end @ <= then if
            _line @ _lnum @ _lnum @ _pos @ = if ">" else " " then
            "%s%3i: %s" fmtstring me @ swap notify 
        then
    repeat
    _pos @ _lines @ array_count > if ">" me @ swap notify  then
    "Done." me @ swap notify 
    0
;
: lsedit::list_split_range[ _lines _start _end -- ret ]
    var _pfx var _mid var _sfx var _idx var _line
    { }list _pfx !
    { }list _mid !
    { }list _sfx !
    _lines @ foreach
        _line ! _idx !
        _idx ++
        _idx @ _start @ < if _pfx @ _line @ swap []<- _pfx ! then
        _idx @ _start @ >= dup if pop _idx @ _end @ <= then if
            _mid @ _line @ swap []<- _mid !
        then
        _idx @ _end @ > if _sfx @ _line @ swap []<- _sfx ! then
    repeat
    { _pfx @ _mid @ _sfx @ }list
;
: lsedit::regexp_list_sub[ _lines _fnd _repl -- ret ]
    var _changed var _idx var _line var _newln
    0 _changed !
    _lines @ foreach
        _line ! _idx !
        _line @ _fnd @ _repl @ reg_all reg_icase bitor regsub _newln !
        _newln @ _line @ strcmp if
            _newln @ dup _lines @ _idx @ ->[] _lines ! pop
            _changed ++
        then
    repeat
    { _changed @ _lines @ }list
;
: lsedit::format_list[ _lines _cols -- ret ]
    var _txt var _out var _pre var _rem
    _lines @ " " array_join _txt !
    _txt @ "  *" " " reg_all regsub _txt !
    { }list _out !
    begin
        _txt @ strlen _cols @ >
    while
        { _txt @ _cols @ strcut }list dup
        dup 0 [] _pre ! dup 1 [] _txt ! pop pop
        { _pre @ " " rsplit }list dup
        dup 0 [] _pre ! dup 1 [] _rem ! pop pop
        _pre @ not if
            _rem @ _pre !
            "" _rem !
        else
            _rem @ strlen _cols @ 2 / > if
                { _pre @ " " _rem @ }list array_interpret _pre !
                "" _rem !
            then
        then
        _out @ _pre @ swap []<- _out !
        _rem @ _txt @ strcat _txt !
    repeat
    _txt @ strip if _out @ _txt @ swap []<- _out ! then
    _out @
;
: lsedit::parse_lines[ _str _line1 _line2 -- ret ]
    _str @ "," instr if
        { _str @ "," split }list _str !
        _str @ 0 [] atoi _line1 !
        _str @ 1 [] atoi _line2 !
    else
        _str @ " " instr if
            { _str @ " " split }list _str !
            _str @ 0 [] atoi _line1 !
            _str @ 1 [] atoi _line2 !
        else
            _str @ strip if _str @ atoi dup _line2 ! _line1 ! then
        then
    then
    { _line1 @ _line2 @ }list
;
: lsedit__editor[ _lines _obj _prop -- ret ]
    var _line1 var _line2 var _inln var _cmd var _cmdargs
    var _fnd var _repl var _pfx var _subbed var _sfx var _changed
    var _oldcount var _saveobj var _savelist var _cols var _pfx2
    var _mid var _sfx2 var _origcnt
    0 _line1 !
    0 _line2 !
    begin
        lsedit::insert_pos @ _lines @ array_count ++ > if
            _lines @ array_count ++ lsedit::insert_pos !
            lsedit::insert_pos @ "Inserting at line %i" fmtstring
            me @ swap notify 
        then
        read _inln !
        _inln @ "." 1 strncmp if
            _inln @ _lines @ lsedit::insert_pos @ -- array_insertitem _lines !
            lsedit::insert_pos ++
            continue
        then
        _inln @ ".." 2 strncmp not if
            { _inln @ 1 strcut }list 1 [] _inln !
            _inln @ _lines @ lsedit::insert_pos @ -- array_insertitem _lines !
            lsedit::insert_pos ++
            continue
        then
        { _inln @ " " split }list dup
        dup 0 [] _cmd ! dup 1 [] _cmdargs ! pop pop
        0 begin pop (switch)
            _cmd @
            dup ".h" strcmp not if lsedit__show_help pop break then
            dup ".q" strcmp not if
                _obj @ _prop @ _lines @ array_put_proplist 
                "Saved." me @ swap notify 
                { _cmd @ _cmdargs @ _lines @ }list exit break
            then
            dup ".x" strcmp not if
                "Aborting." me @ swap notify 
                { _cmd @ _cmdargs @ _lines @ }list exit break
            then
            dup ".l" strcmp not if
                _cmdargs @ 1 999999 lsedit::parse_lines dup
                dup 0 [] _line1 ! dup 1 [] _line2 ! pop pop
                _lines @ _line1 @ _line2 @ lsedit::insert_pos @
                lsedit::show_list pop break
            then
            dup ".i" strcmp not if
                _cmdargs @ 1 1 lsedit::parse_lines dup
                dup 0 [] _line1 ! dup 1 [] _line2 ! pop pop
                _line1 @ _line2 @ = not if
                    "Usage: .i LINENUM" me @ swap notify 
                    break
                then
                _line1 @ lsedit::insert_pos !
                lsedit::insert_pos @ _lines @ array_count ++ > if
                    _lines @ array_count ++ lsedit::insert_pos !
                then
                lsedit::insert_pos @ "Inserting at line %i" fmtstring
                me @ swap notify  break
            then
            dup ".s" strcmp not if
                _cmdargs @ "/" explode_array _cmdargs !
                _cmdargs @ array_count 3 = if
                    _cmdargs @ dup
                    dup 0 [] _line1 ! dup 1 [] _fnd ! dup 2 [] _repl ! pop pop
                    _line1 @ 1 999999 lsedit::parse_lines dup
                    dup 0 [] _line1 ! dup 1 [] _line2 ! pop pop
                    _line1 @ not dup not if pop _line2 @ not then
                    dup not if pop _fnd @ not then if
                        "Usage: .s [LINE[,LINE]]/FIND/REPLACE" me @ swap notify 
                        break
                    then
                    _lines @ _line1 @ _line2 @ lsedit::list_split_range dup
                    dup 0 [] _pfx ! dup 1 [] _subbed ! dup 2 [] _sfx ! pop pop
                    _subbed @ _fnd @ _repl @ lsedit::regexp_list_sub dup
                    dup 0 [] _changed ! dup 1 [] _subbed ! pop pop
                    { _pfx @ _subbed @ _sfx @ }list
                    { }list swap array_reverse foreach swap pop 0 swap array_insertrange repeat
                    _lines !
                    _changed @ "Changed %i lines." fmtstring me @ swap notify 
                    _lines @ _line1 @ _line2 @ lsedit::insert_pos @
                    lsedit::show_list pop
                else
                    "Usage: .s [LINE[,LINE]]/FIND/REPLACE" me @ swap notify 
                then break
            then
            dup ".d" strcmp not if
                _lines @ array_count _oldcount !
                _cmdargs @ 0 0 lsedit::parse_lines dup
                dup 0 [] _line1 ! dup 1 [] _line2 ! pop pop
                _line1 @ not dup not if pop _line2 @ not then if
                    "Usage: .d LINENUM [LINENUM]" me @ swap notify 
                then
                _lines @ _line1 @ -- _line2 @ -- array_delrange _lines !
                _oldcount @ _lines @ array_count - "Deleted %i lines."
                fmtstring me @ swap notify 
                lsedit::insert_pos @ _line1 @ >= if
                    lsedit::insert_pos @ _line2 @ > if
                        lsedit::insert_pos @ _line2 @ _line1 @ - ++ - lsedit::insert_pos !
                    else
                        _line1 @ lsedit::insert_pos !
                    then
                then
                lsedit::insert_pos @ "Inserting at line %i" fmtstring
                me @ swap notify  break
            then
            dup ".w" strcmp not if
                _cmdargs @ "=" explode_array _cmdargs !
                _cmdargs @ not if
                    _obj @ dup if pop _prop @ then if
                        _obj @ _prop @ _lines @ array_put_proplist 
                        "Saved." me @ swap notify 
                    else
                        "Usage: .w OBJECT=LISTPROP" me @ swap notify 
                    then
                else
                    _cmdargs @ array_count 2 = if
                        _cmdargs @ dup dup 0 [] _saveobj ! dup 1 [] _savelist ! pop pop
                        _saveobj @ match
                        dup #-1 dbcmp if me @ "I don't see that here!" notify then
                        dup #-2 dbcmp if me @ "I don't know which one you mean!" notify then
                        dup #-3 dbcmp if pop me @ getlink then
                        dup ok? if
                            me @ over controls not if
                                pop #-1 me @ "Permission denied." notify
                            then
                        then _saveobj !
                        _saveobj @ 0 < if break then
                        _savelist @ not if
                            "Usage: .w [OBJECT=LISTPROP]" me @ swap notify 
                            break
                        then
                        _saveobj @ _savelist @ _lines @ array_put_proplist 
                        "Saved." me @ swap notify 
                    else
                        "Usage: .w [OBJECT=LISTPROP]" me @ swap notify 
                    then
                then break
            then
            dup ".f" strcmp not if
                { _cmdargs @ "=" split }list dup
                dup 0 [] _cmdargs ! dup 1 [] _cols ! pop pop
                _cmdargs @ 1 999999 lsedit::parse_lines dup
                dup 0 [] _line1 ! dup 1 [] _line2 ! pop pop
                _cols @ if _cols @ atoi else 75 then _cols !
                _cols @ not dup not if pop _line1 @ not then
                dup not if pop _line2 @ not then if
                    "Usage: .f [L1,[L2]][=LISTPROP]" me @ swap notify 
                    break
                then
                _lines @ _line1 @ _line2 @ lsedit::list_split_range dup
                dup 0 [] _pfx2 ! dup 1 [] _mid ! dup 2 [] _sfx2 ! pop pop
                _mid @ array_count _origcnt !
                _mid @ _cols @ lsedit::format_list _mid !
                { _pfx2 @ _mid @ _sfx2 @ }list
                { }list swap array_reverse foreach swap pop 0 swap array_insertrange repeat
                _lines !
                _origcnt @ "Formatted %i lines." fmtstring me @ swap notify 
                _lines @ _line1 @ _line2 @ lsedit::insert_pos @
                lsedit::show_list pop break
            then
            (default)
            { _cmd @ _cmdargs @ _lines @ }list exit break
        repeat pop
    repeat
    0
;
public lsedit__editor
$libdef lsedit__editor
: lsedit__basic[ _arg -- ret ]
    var _opts var _obj var _cmd var _args var _lines
    argparse::init pop
    "" argparse::set_mode pop
    "" { }list "obj=list" argparse::add_mode pop
    _arg @ argparse::parse _opts !
    _opts @ not if 0 exit then
    _opts @ "obj" [] not
    dup not if pop _opts @ "list" [] not then if
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
    1 lsedit::insert_pos !
    _obj @ _opts @ "list" [] array_get_proplist _lines !
    _lines @ 1 999999 lsedit::insert_pos @ lsedit::show_list pop
    begin
        _lines @ _obj @ _opts @ "list" [] lsedit__editor dup
        dup 0 [] _cmd ! dup 1 [] _args ! dup 2 [] _lines ! pop pop
        { ".x" ".q" }list _cmd @ array_findval if break then
        _cmd @ "Unrecognized editor command '%s'." fmtstring
        me @ swap notify 
    repeat
    { _cmd @ _args @ _lines @ }list
;
public lsedit__basic
$libdef lsedit__basic
: _main[ _arg -- ret ]
    lsedit__init_help pop
    _arg @ lsedit__basic
;
: __start
    "me" match me ! me @ location loc ! trig trigger !
    "" argparse::current_mode !
    { }list argparse::modes_list !
    { }dict argparse::flags_map !
    { }dict argparse::posargs_map !
    { "" "remainder" }dict argparse::remainder_map !
    { }list lsedit::help_lines !
    _main
;
