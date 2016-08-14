#######################
MUV 2.0 Language Syntax
#######################

.. sectnum::
   :depth: 2

.. contents:: Table of Contents
   :depth: 2
   :backlinks: top


Comments
========
Comments can take one of two styles.  For single-line comments, you can use::

    // Single line comment.

For multi-line comments, you can use::

    /*
    multiple
    line
    comment
    */


Literals
========
Decimal integers are simple::

    123456789

Hexadecimal integers are prefixed with ``0x``::

    0x7ffc

Octal integers are prefixed with ``0o``::

    0o1234567

Binary integers are prefixed with ``0b``::

    0b11010100

You can also prefix decimal numbers with ``0d``, if you want to be pedantic::

    0d123456789

Floating point numbers are given like::

    3.14
    0.1
    3.
    1e9
    6.022e23
    1.6e-35

DataBase References (dbrefs) are given like::

    #12345
    #-1

All numbers, of any base, can have ``_`` placeholder characters, to make the
numbers more human readable, like thousands separators::

    123_456_789
    0xBAD_BEEF
    0b1101_0100
    0o12_345_678
    16_237.21
    #12_345

String literals are given with single or double-quotes::

    "Hello!"
    'Hiya!'

If you use triples of quotes for string delimiters, you can more easily
include single or double character quotes in the string::

    """It's a "test"."""
    '''It's a "test".'''

Singlequotes and doublequotes inside strings can be escaped by a
backslash ``\``::

    "This is a \"test\"."

You can insert a newline inside a string with a ``\r`` or ``\n``, and
an escape char can be added with a ``\e`` or ``\[``::

    '\e[1mBold\[[0m\rNormal'

To make it easier to give regexp patterns with backslashes, you can give raw
strings by preceeding a regular string of any type with a single ``r``.  Raw
strings are not processed for backslash escaped characters::

    r"http://\([a-z0-9._-]+\)"
    r'http://\([a-z0-9._-]+\)'
    r"""http://\([a-z0-9._-]+\)"""
    r'''http://\([a-z0-9._-]+\)'''

List arrays can be declared as comma-separated lists of values, surrounded
by square brackets::

    ["first", "second", "third"]
    [1, 2, 4, 8]

Dictionaries (sometimes called hash tables, or associative arrays in other
languages) are declared like lists, but with key-value pairs, where the key
and value in each pair are separated by ``=>`` delimiters::

    [ "key1" => "val1", "key2" => "val2", "key3" => "val3" ]

To declare an empty dictionary, which is distinct from a list, use::

    [=>]


Constant Declarations
=====================
You can declare constants using the syntax::

    const PI = 3.14159;

By convention, the constant name should be all uppercase.


Global Variables
================
You can declare global variables at the toplevel scope like::

    var myglobal;
    var answer = 42;

The global variables ``me``, ``loc``, ``trigger`` and ``command`` are
pre-defined for all programs.


Function Declarations
=====================
You can declare a function like this::

    func helloworld() {
        return "Hello World!";
    }

With arguments, you can declare it like this::

    func concatenate(var1, var2) {
        return strcat(var1, var2);
    }

If you need a variable number of arguments for a function, you can put a ``*``
after the last variable, to indicate that the last variable will receive all
remaining arguments, in a list::

    func concat(args*) {
        return array_interpret(args);
    }

If you need to declare a ``public`` function, that can be called by name from
other MUF programs, you can declare it like this::

    public func concat(args*) {
        return array_interpret(args);
    }

Functions return the value given to the ``return`` command.  ie: ``return 42;``
will return the integer value ``42`` from the function.  If the end of the
function is reached with no ``return`` executing, then the function will
return the integer ``0``.


Function Calls
==============
You can call functions you have declared, and many builtin MUF primitives in
this way::

    myvar = myfunction(5, "John Doe");
    notify(me, "Hello World!");

If a MUF primitive would return more than one argument on the stack, the MUV
counterpart will return all those values in a list.


Function Variables
==================
You can declare extra variables in function scope like this::

    func myfunction() {
        var myvar;
        var fifth = "5th";
        ...
    }

Variables can be declared in block scopes within functions, and will be in
effect only within those blocks.  You can even declare variables of the same
name within different scopes::

    func myfunction() {
        var x = "C";
        for (var x in ["F", "A", "D"]) {
            if (x eq "A") {
                tell(x);
                var x = "B";
                tell(x);
            }
        }
        tell(x);
    }

will output the following::

    A
    B
    C


Built-Ins Functions
===================
MUV has several built-in commands available to all programs:

===================  ====================================================
     Function                            Description                     
===================  ====================================================
``abort(msg)``       Throws a user exception with the given ``msg``.     
``throw(msg)``       The same as ``abort(msg)``                          
``tell(msg)``        The same as ``notify(me, msg)``                     
``count(arr)``       Returns the count of how many items are in an array.
``cat(...)``         Converts all args to strings and concatenates them. 
``haskey(key,arr)``  Evaluates true if ``key`` is in the array ``arr``.  
===================  ====================================================

MUV also has some built-in constants:

===================  ====================================================
     Constant                             Description                    
===================  ====================================================
``true``              ``1`` (Evaluates as true.)                         
``false``             ``0`` (Evaluates as false.)                        
===================  ====================================================


Namespaces
==========
If you declare global variables and function within a namespace block, then
those variables and functions become part of that namespace::

    namespace math {
        const PI = 3.14159;
    }

Will define the constant ``math::PI``.  To refer to that variable, you will
need to either use the ``math::`` prefix, or specify that you want to use that
namespace like this::

    using namespace math;

Here's more examples::

    namespace math {
        const PI = 3.14159;
        func rad2deg(x) {
            return x*180.0/PI;
        }
    }
    func thirdpi() {
        return math::rad2deg(math::PI/3.0);
    }
    using namespace math;
    func halfpi() {
        return rad2deg(PI/2.0);
    }


Includes
========
You can include the code from other MUV files by using the ``include`` command::

    include "otherfile.muv";

You can include standard MUV files by preceeding the filename with a ``!``.
This tells ``include`` to look for the file in the system-wide MUV includes.
One important standard include file is ``!fb6/prims``::

    include "!fb6/prims";

If you include ``!fb6/prims`` in your file, you will get all the standard FB6
MUF primitives declared for MUV to use.  These primitives will be declared
with exactly the same names as they have in MUF, with the same argument
ordering.  The only exceptions are:

================  ==================  ========================================
    MUF Name           MUV Name                      Change                   
================  ==================  ========================================
``name-ok?``      ``name_ok?()``      Dash in name replaced with underscore.  
``pname-ok?``     ``pname_ok?()``     Dash in name replaced with underscore.  
``ext-name-ok?``  ``ext_name_ok?()``  Dashes in name replaced with underscore.
``fmtstring``     ``fmtstring()``     Argument ordering completely reversed.  
================  ==================  ========================================

Since MUF has kind of a messy namespace, you can *instead* include files
with just the primitives you need, renamed a bit more sensibly.  For example,
if you include the file ``!fb6/obj`` You can get access to the standard
fb6 object related primitives, renamed into the ``obj::`` namespace such
that MUF primitives like ``name`` and ``set`` are renamed to ``obj::name()``
and ``obj::set()``, leading to far less namespace polution.  The standard
namespaced include files are as follows, in alphabetical order.

================  ==============  ============================================
  Include File      NameSpace                  What it declares               
================  ==============  ============================================
``fb6/ansi``      ``ansi::``      ANSI color code string primitives.          
``fb6/argparse``  ``argparse::``  Cmd-line argument parsing.                  
``fb6/array``     ``array::``     Array/list/dictionary primitives.           
``fb6/conn``      ``conn::``      Connection based primitives.                
``fb6/debug``     ``debug::``     Debugging related primitives.               
``fb6/descr``     ``descr::``     Descriptor based connection primitives.     
``fb6/event``     ``event::``     Event handling primitives.                  
``fb6/gui``       ``gui::``       MCP-GUI related primitives and defines.     
``fb6/io``        ``io::``        ``notify`` and ``read`` type primitives.    
``fb6/lock``      ``lock::``      Lock related primitives.                    
``fb6/match``                     ``match_noisy``, ``match_controlled``       
``fb6/math``      ``math::``      Floating point and integer math prims.      
``fb6/mcp``       ``mcp::``       MCP client-server protocol prims.           
``fb6/obj``       ``obj::``       DB object related primitives.               
``fb6/proc``      ``proc::``      MUF process related primitives.             
``fb6/prog``      ``prog::``      Program calling, editing, and compiling.    
``fb6/prop``      ``prop::``      Prims for working with properties.          
``fb6/regex``     ``regex::``     Regular expression primitives.              
``fb6/stdlib``                    ``trig``, ``caller``, ``prog``, ``version``.
``fb6/str``       ``str::``       String manipulation primitives.             
``fb6/sys``       ``sys::``       System related primitives.                  
``fb6/time``      ``time::``      Time based primitives.                      
``fb6/type``      ``type::``      Type checking and conversion primitives.    
================  ==============  ============================================

NOTE: It doesn't make much sense to include *both* ``!fb6/prims`` *and* one
or more of the namespaced files.  If you include from both, it should still
work, but it really misses the point of using namespaces.


Expressions
===========

Basic Math
----------
- Addition: ``2 + 3``
- Subtraction: ``5 - 2``
- Multiplication: ``5 * 2``
- Division: ``10 / 2``
- Modulo: ``7 % 3``
- Grouping: ``2 * (3 + 4)``


Bitwise Math
------------
- Bitwise AND: ``6 & 4``
- Bitwise OR: ``8 | 4``
- Bitwise XOR: ``6 ^ 4``
- Bitwise NOT: ``~10``
- BitShift Left: ``1 << 4``
- BitShift Right: ``128 >> 3``


Assignment
----------
- Simple assignment: ``x = 23``
- Add and assign: ``x += 2`` is the same as ``x = x + 2``
- Subtract and assign: ``x -= 2`` is the same as ``x = x - 2``
- Multiply and assign: ``x *= 2`` is the same as ``x = x * 2``
- Divide and assign: ``x /= 2`` is the same as ``x = x / 2``
- Modulo and assign: ``x %= 2`` is the same as ``x = x % 2``
- Bitwise AND and assign: ``x &= 2`` is the same as ``x = x & 2``
- Bitwise OR and assign: ``x |= 2`` is the same as ``x = x | 2``
- Bitwise XOR and assign: ``x ^= 2`` is the same as ``x = x ^ 2``
- BitShift Left and assign: ``x <<= 2`` is the same as ``x = x << 2``
- BitShift Right and assign: ``x >>= 2`` is the same as ``x = x >> 2``


Numeric Comparisons
-------------------
- ``x == 2`` returns true if ``x`` equals ``2``, otherwise false.
- ``x != 2`` returns true if ``x`` does not equal ``2``, otherwise false.
- ``x < 2`` returns true if ``x`` is less than ``2``, otherwise false.
- ``x > 2`` returns true if ``x`` is greater than ``2``, otherwise false.
- ``x <= 2`` returns true if ``x`` is less than or equal to ``2``, otherwise false.
- ``x >= 2`` returns true if ``x`` is greater than or equal to ``2``, otherwise false.


String Comparisons
------------------
- ``x eq "foo"`` returns true if ``x`` equals the string ``"foo"``, case sensitive.


Array Operations
----------------
- ``x in arr`` returns true if the value ``x`` is in the array ``arr``.
- ``x[2]`` returns the third item of the array in the variable ``x``.
- ``x[2] = 42`` sets the third element of the array in ``x`` to ``42``.


True and False
--------------
In MUV and MUF both, a value is considered True unless it is one of the
following specific False values:

- Integer: ``0``
- DBRef: ``#-1``
- Float: ``0.0``
- Empty String: ``""``
- Empty List: ``[]``
- Empty Dictionary: ``[=>]``
- Invalid Lock
- Stack Mark


Conditional Operator
--------------------
If you need to provide two different results, based on the result of a third
expression, you can use the conditional operator::

    x>0 ? 1 : 2

This will return ``1`` if ``x`` is greater than ``0``, otherwise it will
return ``2``.

**IMPORTANT:** since some identifiers in MUV can end in ``?`` (ie: ``awake?``)
you will need to put a space between an identifier and the ``?`` in a
conditional expression, otherwise you may get odd syntax errors::

    var success = result ?"Yes":"No";


Logical Operations
------------------
- Logical AND: ``x && y`` returns true if both ``x`` or ``y`` are true.
  More specifically, this returns the value of ``x`` if it is false,
  otherwise it returns the value of ``y``.
- Logical OR: ``x || y`` returns true if either ``x`` or ``y`` is true.
  More specifically, this returns the value of ``x`` if it is true,
  otherwise it returns the value of ``y``.
- Logical XOR: ``x ^^ y`` returns true if exactly one of ``x`` or ``y`` is true.
- Logical NOT: ``!x`` returns true if ``x`` is false.

The expression ``x > 3 && !(y < 10)`` will return true if both ``x`` is greater
than ``3`` *and* ``y`` is *not* less than ``10``.

**NOTE:** Logical expressions support shortcutting.  If the left half of a
logical ``||`` (OR) is true, the right half isn't evaluated at all. If
the left half of a logical ``&&`` (AND) is false, the right half isn't
evaluated at all.  Both sides of a logical ``^^`` (XOR) are always
evaluated.  This mostly has implications when you are calling functions
in the right-hand side of a shortcutted expression, as these calls may
not be made at all.

The intrinsic short-cutting in logical ``&&`` (AND) and ``||`` (OR) operators
can also have other uses.  The ``&&`` (AND) operator can be used to chain
successful calls, such as::

    function1(x) && function2(x) && function3(x)

Each function in the chain is only called if every previous function in the
chain returned a true value.  The final value returned will either be the
first false value returned, or the true value returned by the last call.

More usefully, if you have a series of functions that return a false value
on success, and a non-false value on failure, you can chain these calls with
``||`` (OR) operators, and get an overall failure code (or string) for the
chain::

    function1(x) || function2(x) || function3(x)

Each function in this chain is only called if every previous function in
the chain returned a false (success!) value.  The final value returned will
either be the first true (error code or string) value returned, or the false
(success!) value returned by the last call.

The ``||`` (OR) operator is also useful in returning default values::

    function1(x) || 42

This will return the result from ``function1()``, unless it is a value that
evaluates as false, in which case ``42`` will be returned.

**WARNING:** You can combine ``&&`` (AND) and ``||`` (OR) to provide alternate
values for both success and failure, but this is almost never a good idea.
This notation only works correctly if you use the logical operators in that
specific order.  Additionally, if the true branch of the expression tries to
return a false value, then the false branch gets erroneously evaluated as
well, and its result is returned instead.

It will always be cleaner, clearer, more efficient, more concise, and less bug
prone to use the Conditional Operator.  Do this::

    result ? "Yes" : "No";

Don't do this::

    result && "Yes" || "No";


Chaining Expressions
--------------------
All these expressions can be combined and chained in surprisingly complex
ways::

    var y = [[4, 5, 6], 3];
    var z = 1;
    var x = y[0][1] = 43 * (z += 1 << 3);


Arrays
======
Declaring a list array is easy::

    var listvar = ["First", "Second", "Third", "Forth!"];

To declare an empty list, just use::

    var foo = [];

You can fetch an element from a list using a subscript::

    var a = listvar[2];

Which will set the newly declared variable ``a`` to ``"Third"``:

Setting a list element uses a similar syntax::

    listvar[3] = "foo";

That will change the 4th element (as list indexes are 0-based) of the list in
listvar to ``"foo"``, resulting in listvar containing the list::

    ["First", "Second", "Third", "foo"]

You can append items to an existing list with the ``[]`` construct::

    listvar[] = "bar";

Resulting in listvar containing the list::

    ["First", "Second", "Third", "foo", "bar"]

Deletion of list elements uses ``del()`` like this::

    del(listvar[2]);

Which deletes the 3rd element of the list stored in ``listvar``, resulting in
``listvar`` containing::

    ["First", "Second", "foo", "bar"]

If you need to work with nested lists, ie: lists stored in elements of lists,
you can just add subscripts to the expression.  For example, if you start
with this array::

    var nest = [
        [8, 7, 6, 5],
        [4, 3, 2],
        ["Foo", "Bar", "Baz"]
    ];

Then to get the second element of the list embedded in the third element
of the array in the variable ``nest``, you will do the following::

    nest[2][1];

To set the third element of the list embedded in the first element of
``nest``, to the value 23, you can do this::

    nest[0][2] = 23;

At this point, the variable ``nest`` will contain the following::

    [ [8, 7, 23, 5],  [4, 3, 2],  ["Foo", "Bar", "Baz"] ]

To append ``"Qux"`` to the list in the 3rd element of the list in ``nest``::

    listvar[2][] = "Qux";

The variable ``nest`` now contains the following::

    [ [8, 7, 23, 5],  [4, 3, 2],  ["Foo", "Bar", "Baz", "Qux"] ]

To delete the 2nd element of the list in the 3rd element in ``nest``::

    del(nest[2][1]);

The variable ``nest`` now contains::

    [ [8, 7, 23, 5],  [4, 3, 2],  ["Foo", "Baz", "Qux"] ]


Dictionaries
============
Dictionaries are a special type of array, where the keys are not necessarily
numeric, and they don't have to be contiguous.  You can use many of the same
functions and primitives with dictionaries that you use with list arrays.
MUV Dictionaries are functionally like hash tables in other languages.

Defining a dictionary is similar to defining a list array, except you also
specify the keys::

    var mydict = [
        "one" => 1,
        "two" => 2,
        "three" => 3,
        "four" => 4
    ];

To define an empty dictionary, which is distinct from a list, you can use::

    var empty = [=>];

Reading, setting and deleting dictionary elements are very similar to doing
the same with a list array::

    var myvar = mydict["three"];
    mydict["six"] = 6;
    del(mydict["one"]);

Similarly to list arrays, you can also nest dictionaries with other lists and
dictionaries.  The syntax to manipulate nested dictionaries is exactly the
same as for lists::

    var nest = [
        "foo" => [5, 6, 7],
        "bar" => [
            "fee" => 1,
            "fie" => 2,
            "foe" => 3
        ],
        "baz" => 17
    ];
    nest["baz"] = 42;
    nest["bar"][] = "fum";
    del(nest["foo"][1])


Conditional Statements
======================

If Statements
-------------
You can use the ``if`` statement to execute code only if an expression is true::

    if (x > 3)
        tell("Greater!");

This will execute ``tell("Greater!")`` only if the test ``x > 3`` evaluates
as true.

You can make multiple statements part of the conditional by surrounding them
in braces like this::

    if (x > 3) {
        tell("x > 3!");
        tell(cat("x = ", x));
    }

If you also need to have it execute code if the expression was false, you can
use an ``else`` clause, like this::

    if (x < 0) {
        tell("Negative!");
    } else {
        tell("Positive!");
    }

Idiomatically, this is simply "If X is true, do Y, otherwise, do Z."


Post-Conditionals
-----------------
You can make a single statement execute only if an expression is true by
using a trailing ``if`` clause::

    tell("Odd!") if (x%2);

This will only execute ``tell("Odd!")`` if the result of ``x % 2`` evaluates
as true, (non-zero).  Idiomatically, this is "Do X if Y is true."

You can also make a single statement execute only if an expression is false by
using a trailing ``unless`` clause::

    tell("Even!") unless(x%2);

This will only execute ``tell("Even!")`` if the result of ``x % 2`` evaluates
as False (``0``).  Idiomatically, this is "Do X unless Y is true."


Switch Statements
-----------------
If you need to compare a value against a lot of options, you can use the
``switch`` - ``case`` statement::

    switch (val) {
        case(1) tell("One!");
        case(2) tell("Two!");
        case(3) tell("Three!");
    }

The optional ``default`` clause allows you to execute code if no ``case``
matches::

    switch (val) {
        case(1) tell("One!");
        case(2) tell("Two!");
        case(3) tell("Three!");
        default tell("Something else!");
    }

With the ``using`` clause, you can specify a primitive or function that
takes two arguments to use for comparisons.  When the comparison function
or primitive returns true, then a match is found.  When you specify
``using strcmp`` it special-cases the comparison to actually be ``strcmp not``.
The same applies for ``stringcmp``, which is translated to ``stringcmp not``::

    switch (val using strcmp) {
        case("one") {
            tell("First!");
        }
        case("two") {
            tell("Second!");
        }
        case("three") {
            tell("Third!");
        }
        default {
            tell("Something else!")
        }
    }

You can also specify built-in comparison operators like ``eq``, ``in``, or
``=``.  Only the first ``case`` with a successful match will be executed::

    switch (val using eq) {
        case("one") tell("First!");
        case("two") tell("Second!");
        case("three") tell("Third!");
    }

Unlike in C, ``switch`` statements do not fall-through from one case clause to
the next. Also, you can actually use expressions in the case, not just
constants::

    switch(name(obj) using eq) {
        case(strcat(name(me), "'s Brush")) {
            tell("It's one of your brushes!");
            brushcount++;
        }
        case(strcat(name(me), "'s Fiddle")) {
            tell("It's one of your fiddles!");
            fiddlecount++;
        }
    }

If you use the ``break`` statement inside a case clause, you can exit the case
clause early, and execution resumes after the end of the switch.  If you use a
``continue`` statement inside a case clause, the entire switch statement is
re-evaluated.  This can be useful for, perhaps, running a looping state
machine::

    const FIRST = 1;
    const SECOND = 2;
    const THIRD = 3;
    const FOURTH = 4;
    var state = FIRST;
    switch(state) {
        case(FIRST) {
            state = SECOND;
            do_something();
            continue;
        }
        case(SECOND) {
            state = THIRD;
            do_something_else();
            continue;
        }
        case(THIRD) {
            if (do_something_more()) {
                state = FOURTH;
                continue;
            }
            break;
        }
        case(FOURTH) {
            state = FIRST;
            do_something_special()
            continue;
        }
    }


Loop Statements
===============
There are several types of loops available.

While Loops
-----------
While loops will repeat as long as the condition evaluates true.
The condition is checked before each loop::

    var i = 10;
    while (i > 0) {
        tell(intostr(i--));
    }

Idiomatically, ``while(X) Y;`` means  "While X is true, keep repeating Y."


Until Loops
-----------
Until loops will repeat as long as the condition evaluates false.
The condition is checked before each loop::

    var i = 10;
    until (i == 0) {
        tell(intostr(i--));
    }

Idiomatically, ``until(X) Y;`` means  "Until X is true, keep repeating Y."


Do-While Loops
--------------
Do-While loops will repeat as long as the condition evaluates true.
The condition is checked after each loop.  The loop will execute at
least once::

    var i = 10;
    do {
        tell(intostr(i--));
    } while(i > 0);

Idiomatically, ``do X while(Y);`` means "Do X, then while Y is true keep
repeating X."


Do-Until Loops
--------------
Do-Until loops will repeat as long as the condition evaluates false.
The condition is checked after each loop.  The loop will execute at
least once::

    var i = 10;
    do {
        tell(intostr(i--));
    } until(i == 0);

Idiomatically, ``do X until(Y);`` means "Do X, then until Y is true keep
repeating X."


For Loops
---------
For loops come in a few varieties. The first version counts up
from one number to another, inclusive::

    // Count from 1 up to 10, inclusive
    for (var i in 1 => 10) {
        tell(intostr(i));
    }

Idiomatically, ``for (V in X => Y) Z;`` means, "Count from X to Y, inclusive.
For each value, store it in the variable V, then execute Z."

With a ``by`` clause, you can count down, or by a different increment::

    // Count from 10 down to 1, inclusive
    for (var i in 10 => 1 by -1) {
        tell(intostr(i));
    }

Idiomatically, ``for (V in X => Y by N) Z;`` means, "Count from X to Y,
inclusive, adding N each time.  For each value, store it in the variable V,
then execute Z."

You can also iterate arrays/lists/dictionaries like this::

    var letters = ["a", "b", "c", "d", "e"];
    for (var letter in letters)
        tell(letter);

Idiomatically, ``for (V in X) Y;`` means, "For each item in the array X,
store the value in the variable V, then execute the code Y."

To iterate over both indexes/keys and values::

    for (var idx => var letter in ["a", "b", "c", "d", "e"])
        tell(cat(idx, letter));

Idiomatically, ``for (K => V in X) Y;`` means, "For each item in the array X,
store the array item's index (key) in the variable K, and the item's value in
the variable V, then execute the code Y."


Comprehensions
==============
Using a variation on loops and conditionals, you can quickly create lists and
dictionaries that are mutations of already existing arrays.  The original
array is untouched.

For example, if you have a list of strings in the variable ``words``, you can
create a list of uppercased versions of those words like this::

    var words = ["fee", "fie", "foe", "fum"];
    var uppers = [for (var word in words) toupper(word)];

Similarly, you can generate a dictionary.  If we have an existing dictionary,
that we want to make a new dictionary from, with uppercased keys, and values
that are incremented, we can do the following::

    var prims = [
        "notify" => 2,
        "pop" => 1,
        "swap" => 1,
        "setpropstr" => 3
    ];
    var keywords = [for (var k => var v in prims) toupper(k) => v+1];

You can use any variation of for loop for making comprehensions::

    var odd_thirds = [for (x in 1 => 100 by 3) if (x % 2) x];

You can also filter a list or dictionary by adding an ``if`` or ``unless``
clause.  This will only include entries which passed the conditional test::

    var x;
    var odds = [for (x in 0 => 100) if (x % 2) x];
    var sevens = [for (var y in 0 => 100) unless (y % 7) y];


Tuple Assignment
================
If an expression or function call returns an array of known size, you can
assign each array item to an individual variable using tuple assignment::

    extern multiple split(s, delim);
    <var a, var b> = split("Hello, World!", " ");

    <a, b> = split("foo=bar", "=");

You can also use tuple assignment inside a loop or comprehension::

    for (<a, b> in list_generator()) {
        tell(cat(b, a));
    }

    var foo = [for (<a, b> in list_generator()) if (a != b) a + b];

**IMPORTANT:** You must put space between the ``>`` and ``=`` of the
tuple assignment, or the language parser will get confused, thinking
if sees a ``>=`` token.


Exception Handling
==================
You can trap errors with the ``try`` - ``catch`` construct::

    try {
        setname(obj, "Foobar");
    } catch (e) {
        tell(e["error"]);
    }

The variable given to the ``catch`` command will, when an error is received,
have a dictionary stored in it with the following values:

``error``
    The error string that was emitted by the MUF instruction that threw an
    error.

``instr``
    The name of the MUF instruction that threw the error.

``line``
    The MUF line that threw the error.

``program``
    The program that the error was thrown in.  This might not be the same as
    the current program, if the error occurred inside a call.

If you don't care about the exception details, you can just not specify the
variable::

    try {
        setname(obj, "Foobar");
    } catch () {
        tell("Could not set the name.");
    }

If you just want to trap any errors without doing anything, you can just do::

    try {
        setname(obj, "Foobar");
    } catch();

If you need to throw your own custom exception, you can do it like::

    throw("MyError")


MUF Interaction
===============
Sometimes you need to interact with other MUF programs, by reading or
storing data on the MUF stack.  You can do that with the ``top`` and
``push(...)`` constructs. Also, you can specify raw MUF code with the
``muf("...")`` command.

The special variable ``top`` refers to the top of the stack.  You can "pop"
the top item off of the stack and store it in a variable like::

    var foo = top;

You can "push" a value onto the top of the stack with the ``push(...)``
command::

    push("Hi!");

You can also push multiple values at once::

    push("One", 2, #3, "Fore!");

The ``push(...)`` command will return the value of the last item pushed.:

    var v = push(13, 42);

Will leave ``13`` and ``42`` on the stack, and the value of ``v`` will be
set to ``42``.

You can specify raw MUF code by passing it as a string to the ``muf(...)``
command::

    muf('{ "Hello, " args @ }list array_interpret out !');

which will compile directly into MUF as::

    { "Hello, " args @ }list array_interpret out !

IMPORTANT: If you use the ``muf(...)`` command inside a function or in a const
definition, make sure that the MUF code it gives will leave exactly one item
on the stack!

If you need it, you can also use raw MUF code in the using clause of a
``switch``::

    switch (val using muf('"*" strcat smatch')) {
        case("1") tell("Starts with 1");
        case("2") tell("Starts with 2");
        case("3") tell("Starts with 3");
    }


Extern Declarations
===================
If new primitives are added to MUF that MUV doesn't know about, or if you need
to call external libraries, you can use an ``extern`` declaration to let MUV
know about how to call it::

    extern void tell(msg);

will tell MUV that a function or primitive named ``tell`` exists that takes one
argument, and returns nothing on the stack.  A call to this will return the
value ``0``, if it is used in an expression::

    extern single foobar(baz, qux);

will tell MUV that a function or primitive named ``foobar`` exists, that takes
two arguments, and returns a single value on the stack.  When you call this
function, it will return that single stack item to the caller::

    extern multiple fleegul();

will tell MUV that a function or primitive named ``fleegul`` exists, that takes
no arguments, and returns two or more values on the stack.  When you call this
function, it will return a list containing all the returned stack items.

If you need to create an extern for a primitive or function that is problematic
to describe with a normal extern, you can give raw custom MUF code at the end
of the extern to coerce it to a normal form::

    extern single concat(args*) = "array_interpret";

    extern single fmtstr(fmt, args*) = "
        2 try
            array_explode 1 + rotate fmtstring
            depth 0 swap - rotate depth 1 - popn
        catch abort
        endcatch
    ";

The arguments for the extern will be the topmost stack items, with the first
argument being deepest on the stack.  In the case of varargs, like above, the
topmost stack item will be a list containing all the remaining args.  If the
extern is ``void``, then nothing is expected to be left on the stack.  If the
extern is ``single``, then one item is expected to be left on the stack.  If
the extern is ``multiple``, then all items left on the stack will be bundled
into a list to be returned to the caller.

The raw MUF code given is used *instead* of a call to the name of the declared
extern.  A normal extern::

    extern single foo();

will insert ``foo`` into the output code where a call to ``foo()`` is made.
An extern with raw MUF like::

    extern single foo() = "bar";

will insert ``bar`` into the output code where a call to ``foo()`` is made.


Directives
==========
There are a number of compiler directives that are (mostly) passed through to
the MUF output code.  These include:

================  ======================================================
   Directive         What it Does                                          
================  ====================================================== 
$language "muv"   Allow future MUCK servers to determine this is MUV.   
$warn "msg"       Prints msg as a MUV compiler warning.                 
$error "msg"      Prints msg as a MUV error and stops compilation.      
$echo "msg"       Outputs as the corresponding MUF directive.           
$author "who"     Outputs as the corresponding MUF directive.           
$note "msg"       Outputs as the corresponding MUF directive.           
$version 1.2      Outputs as the corresponding MUF directive.           
$libversion 1.2   Outputs as the corresponding MUF directive.           
$include "$foo"   Outputs as the corresponding MUF directive.           
$pragma "foo"     Outputs as the corresponding MUF directive.           
================  ======================================================

**IMPORTANT:** All MUV programs should start with ``$language "muv"``.
Future versions of the MUCK server will use this to recognize MUV source
code.  The MufSim IDE also uses it to distinguish MUV from MUF source.


Debugging MUV
=============
It's easiest to debug and test MUV code using the MufSim GUI IDE.  There
are binaries for Mac OS X, and for 64-bit Windows.  You can find them at:

    https://github.com/revarbat/mufsim/tree/master/dist

For Linux, (or any other platform, really), or if you want to use the
command-line mufsim MUV/MUF debugger instead of the GUI, you can use
Python and pip to install MufSim::

    pip install mufsim --upgrade

If you prefer to install from the github MufSim sources, download and unpack
the mufsim-x.x.x.tar.gz archive, then install with::

    python3 setup.py build install

Otherwise, when you are debugging a program compiled into MUF from MUV,
using the MUCK's built-in MUF debugger or stack-tracing, there are a few
things you should be aware of:

- If you add a ``-d`` to the muv compiler command-line, debugging code will
  be inserted throughout the MUF output. This mostly takes the form of
  comments that show the MUV source line that generated the current MUF code.
  These comments take the form ``(MUV:L123)`` where 123 is the line number.
- To prevent namespace collision with the built-in primitives of MUF, the
  non-public functions and variables that MUV generates are renamed slightly
  from what was given in the MUV sources.  This generally means preceeding
  the name with a ``_``, and converting any ``::`` namespace separators
  to ``__``.  ie: ``::foo::bar`` will get renamed to ``_foo__bar``.
- To keep consistent with expressions returning values, some extra ``dup``
  and ``pop`` statements may appear throughout the code.  Some of this will
  get optimized out by the MUF compiler, and some won't, but they are very
  fast primitives that shouldn't affect performance much.
- Calls to an ``extern void`` defined primitive or function will be followed
  by a ``0`` to fake that the call returned ``0``.
- Calls to an ``extern multiple`` defined primitive or function will be
  wrapped in ``{`` and ``}list`` to collapse the multiple return values
  into a single list array.
- Because in MUV *all* calls have a return value, for those functions that
  don't end in a ``return`` statement, a ``0`` is put at the end of a generated
  function, just in case.

For example, the following MUV source::

    $language "muv"
    extern void tellme(msg) = "me @ swap notify";
    extern single toupper(s);
    extern multiple stats(who);
    var gvar = 42;
    func foo(bar) {
        tellme(toupper(bar));
        var baz = stats(me);
    }

Will compile to MUF as::

    ( Generated by the MUV compiler. )
    (   https://github.com/revarbat/pymuv )
    (MUV:L4) lvar _gvar
    (MUV:L5) : _foo[ _bar -- ret ]
        (MUV:L6) _bar @ toupper me @ swap notify
        (MUV:L7) { me @ stats }list var! _baz
        0
    (MUV:L8) ;
    (MUV:L5) : __start
        "me" match me ! me @ location loc ! trig trigger !
        (MUV:L4) 42 _gvar !
        _foo
    ;

There are several things to note here:

- The program starts with ``$language "muv"``
- There are comments like ``(MUV:L123)`` throughout the code, to indicate
  what MUV source line originated the MUF code following the comment.
- The user declared global variable ``gvar`` has been renamed to ``_gvar``
- The user declared function ``foo`` has been renamed to ``_foo``.
- The user declared scoped variables ``bar`` and ``baz`` have been renamed
  to ``_bar`` and ``_baz``.
- The system variable ``me``, however, remains unchanged.
- Since ``toupper()`` is declared to return a ``single`` value, that value is
  returned unmolested after the call to ``toupper``.
- The call to the ``extern`` declared function ``tellme``, is replaced by the
  code ``me @ swap notify``.
- Since ``stats()`` is declared to return ``multiple`` values, the entire
  expression is wrapped in ``{`` and ``}list`` to collapse all those values
  into a single list array.
- As the function ``foo()`` ends without a ``return`` statement at the end,
  a ``0`` is pushed onto the stack, so ``foo()`` always returns at least ``0``.
- The ``__start`` function is added to the end of the progam, to perform
  initialization of global variables.  It then calls the user's last
  function.
  
**WARNING:** Global variable initialization only occurs in the ``__start``
function, which isn't run for public library calls.  Global variables in
libraries may not get initialized unless you make an explicit public
function to initialize them.

