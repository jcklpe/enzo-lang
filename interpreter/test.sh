#!/usr/bin/env bash
# ────────────────────────────────────────────────────────────────────────────────
# test.sh
# ────────────────────────────────────────────────────────────────────────────────

poetry install
poetry run enzo <<'EOF'
// ── 1) EMPTY BIND ────────────────────────────────────────────────────────────
$x: ;

// 1a) INVOKING AN UNDEFINED VARIABLE
$undefinedVar;      // error: undefined: $undefinedVar

// ── 2) FILLING AN EMPTY BIND AND INVOKING IT ──────────────────────────────────
$x: 10;
$x;                 // prints 10

// ── 3) REDECLARING A NON‐EMPTY VARIABLE (USING “:”) ────────────────────────────
$a: 1;
$a: 2;              // error: $a already defined

// ── 4) REBINDING WITH “<:” AND INVOKING ───────────────────────────────────────
$x <: 100;
$x;                 // prints 100

// ── 5) REDECLARE A REBOUND VARIABLE WITH “:” (SHOULD ERROR) ───────────────────
$x: 99;             // error: $x already defined

// ── 6) REBIND TYPE MISMATCH ERROR ─────────────────────────────────────────────
$x <: "hello";      // error: cannot assign Text to Number

// ── 7) BINDING MATH OPERATIONS ─────────────────────────────────────────────────
$y: 3 + 2;
$x + $y;            // prints 105

// ── 8) ARITHMETIC PRECEDENCE CHECK ─────────────────────────────────────────────
$c: 2 + 3 * 4;
$c;                 // prints 14

$d: (2 + 3) * 4;
$d;                 // prints 20

// ── 9) FULL BIND UPFRONT LOCKING TYPE ──────────────────────────────────────────
$z: 3 + 4;          // z = 7
$z <: 8;            // rebind OK, z now 8
$z <: "oops";       // error: cannot assign Text to Number

// ── 10) TEXT + INTERPOLATION ───────────────────────────────────────────────────
$text-example: ;
$text-example <: "rebinding this text and ";
$text-example2: "this is text example 2";

"just a plain text";   // prints “just a plain text”

"<$text-example; $text-example2;>";   // prints “rebinding this text and this is text example 2”
"100 plus 5 is: <$x + $y>";           // prints “100 plus 5 is: 105”

// ── 11) LIST STUFF & INDEX ERRORS ─────────────────────────────────────────────
$emptyListTest: [];
$emptyListTest;    // prints “[ ]”
$emptyListTest.1;  // error: list index out of range

// ── 12) BIND EMPTY AND THEN FILL WITH LIST ────────────────────────────────────
$empty-list: ;
$empty-list: 50;    //error: $empty-list already defined
$empty-list<: ["now not empty"];
$empty-list;       // prints “[ "now not empty" ]”

// ── 13) DECLARE LIST AND ACCESS ITEMS ────────────────────────────────────────
$colors: ["red", "green", "blue", "yellow"];
$colors.3;         // prints “blue”
$i: 2;
$colors.$i;        // prints “green”

// ── 14) NESTED LISTS WITH INDEXING ────────────────────────────────────────────
$nestedList: [[1, 2], [3, 4]];
$nestedList.2.1;   // prints “3”

// ── 15) NOW THAT $colors & $i ARE DEFINED, INTERPOLATE A STRING THAT USES THEM ─
$text-about-colors-list: "color <$i> is <$colors.$i>";
$text-about-colors-list;   // prints “color 2 is green”

// ── 16) TABLE STUFF ───────────────────────────────────────────────────────────
$table: { $name: "Alice", $age: 30 };
$table;             // prints “{ $name: "Alice", $age: 30 }”
$table.name;        // prints “Alice”
$table.age;         // prints “30”

// ── 17) REBINDING TABLE PROPERTIES ────────────────────────────────────────────
$table.name <: "Bob";
$table.name;        // prints “Bob”
$table;             // prints “{ $name: "Bob", $age: 30 }”

// ── 18) ANOTHER TABLE + PROPERTY REBIND ───────────────────────────────────────
$table2: { $foo: 42, $bar: "hello" };
$table2.bar;        // prints “hello”
$table2.foo <: 100;
$table2;            // prints “{ $foo: 100, $bar: "hello" }”

// ── 19) EMPTY TABLE LITERAL + BAD PROP ACCESS ERROR ──────────────────────────
$emptyTable: {};
$emptyTable;            // prints “{ }”
$emptyTable.someKey;    // error: 'someKey' does not exist on this table

// ── 20) NESTED TABLE + MIXED INDEX/ATTR ───────────────────────────────────────
$nestedTable: {
    $inner: {
        $val: 42,
        $arr: [10, 20]
    }
};
$nestedTable.inner.val;     // prints “42”
$nestedTable.inner.arr.2;   // prints “20”

// ── 21) REBINDING NESTED TABLES ───────────────────────────────────────────────
$nestedTable.inner.val <: 100;
$nestedTable.inner.val;     // prints “100”

// ── 22) MIXED LIST‐INSIDE‐TABLE ● INDEX VS ATTR ──────────────────────────────
$mix: { $lst: ["a", "b", "c"] };
$mix.lst.2;                // prints “b”

// ── 23) COMPLEX MATH INTERPOLATION ● MULTIPLE EXPRESSIONS ───────────────────
$x <: 7;
$y <: 3;
"Sum=<$x + $y;> Prod=<$x * $y;>";   // prints “Sum=10Prod=21”

   // an indented comment line that should be skipped

// ── 24) REBINDING WITH “:>” IMPLICITLY BINDS IF NEEDED ────────────────────────
55 :> $newImplicit;
$newImplicit;               // prints “55”
$newImplicit <: "oops";     // error: cannot assign Text to Number

// ── 25) COMPLEX TABLE + LIST INDEX/PROPERTY ACCESS ─────────────────────────
$complex: {
    $tbl: { $a: [100, 200], $b: "x" },
    $lst: [ { $foo: 1 }, { $foo: 2 } ]
};
$complex.tbl.a.1;    // prints “100”
$complex.lst.2.foo;  // prints “2”

// ── 26) LIST OF TABLES + INDEX OF TABLE ────────────────────────────────────
$lot: [ { $x: 5 }, { $x: 7 } ];
$lot;                 // prints “[ { $x: 5 }, { $x: 7 } ]”
$lot.2.x;             // prints “7”

// ── 27) TABLE OF LISTS + INDEX OF LIST ─────────────────────────────────────
$tol: { $first: [1, 2], $second: [3, 4] };
$tol.first.2;         // prints “2”
$tol.second;          // prints “[ 3, 4 ]”

// ── 28) COMPOUND INTERPOLATION WITH TABLE+LIST ACCESS ────────────────────────
// We avoid backslash‐escaping inside interpolation by concatenating simple strings:
$myTable: { $greeting: "hi", $nums: [2, 4] };
"<$myTable.greeting;>! The nums are:<$myTable.nums.1;>, and <$myTable.nums.2;>";
                         // prints “hi! The nums are: 2,4”

// ── 29) MULTIPLE ASSIGNMENTS ON ONE LINE ────────────────────────────────────
$u: 1; $v: 2; $u + $v;    // prints “3”

// ── 30) PARENTHESIZED EXPRESSIONS AS STAND‐ALONE ─────────────────────────────
(10 + 5);                 // prints “15”

// ── 31) LARGE NUMBERS + NEGATIVE NUMBERS ────────────────────────────────────
$big: 1234567890;
$big;                     // prints “1234567890”
$neg: -5;
$neg;                     // prints “-5”
$neg * 2;                 // prints “-10”
$negzero: -0;
$negzero;           // prints 0 (should not crash)
$weird: --5;        // error: double minus not allowed

// ── 32) MIXED‐CASE VARIABLE NAMES ───────────────────────────────────────────
$Var123: 10;
$Var123;                  // prints “10”
$var-xyz: 20;
$var-xyz;                 // prints “20”
$Var123 + $var-xyz;       // prints “30”

// ── 33) VARIOUS TYPE‐ERRORS FOR BAD INDEX/PROP REBIND ───────────────────────
$notalist: "oops";
$notalist.1;              // error: index applies to lists

$prim: 999;
$prim.someKey <: 5;       // error: can't rebind to non-existent property

$myTbl: { $a: 1 };
$myTbl.1;                 // error: index applies to lists

// ── MALFORMED INPUT / TRAILING COMMA EDGE CASES ──────────────────────

// Valid trailing commas (should succeed)
$goodTable: { $foo: 1, $bar: 2, };
$goodTable;
$goodList: [1, 2, 3, ];
$goodList;

// Double comma in table (should error)
$badTable1: { $foo: 1,, $bar: 2 };        // error: double comma

// Comma before any item in table (should error)
$badTable2: { ,$foo: 1, $bar: 2 };        // error: leading comma

// Just a comma in table (should error)
$badTable3: { , };                        // error: just comma

// Double comma in list (should error)
$badList1: [1,,2];                        // error: double comma

// Comma before any item in list (should error)
$badList2: [,1,2];                        // error: leading comma

// Just a comma in list (should error)
$badList3: [,];                           // error: just comma

// ── EDGE CASES & WEIRD INPUTS ─────────────────────────────────────────────

// 1. Redundant semicolons and whitespace
;;;;;;              // error: extra semicolons
$meaning-of-life: 42;;          // error: extra semicolons
      ;   ;         // error: extra semicolons

// 2. Variable names — all should be allowed by current grammar
$123abc: 5;         // allowed
$_: 9;              // allowed
$-foo: 3;           // allowed
$123abc;            // prints 5
$_;                 // prints 9
$-foo;              // prints 3




// 4. Out-of-bounds and weird list indices
$list: [1,2,3];
$list.0;            // error: index out of range (0 is not allowed, should be 1-based)
$list.4;            // error: index out of range
$list.-1;           // error: negative index not allowed
$list."foo";        // error: index must be a number
$list.1.1;          // error: index applies to lists (cannot index an integer)

// 5. Table property errors
$table9: { $foo: 1 };
$table9.bar;         // error: '$bar' (not found)
$table9.1;           // error: index applies to lists
$table9.foo.bar;     // error: '$bar' (not found after foo)

// 6. Interpolation errors
"text <bad syntax>";    // error: undefined variable or parse error in interp
"hello <$foo + >";      // error: parse error in interpolation
"hello <<$foo>>";       // error: nested <...> not allowed (for now)

// 7. List/table with trailing comma and blank entries
$lt: [1,,2];            // error: double comma
$tl: { $a: 1, , $b: 2 }; // error: leading comma

// 8. Bindings and rebinding with wrong types
$foo: 7;
$foo <: "text";         // error: cannot assign Text to Number
$foo: "oops";           // error: $foo already defined

// 9. List/table mutation — mutation should be supported!
$mutable: [1,2];
$mutable.1 <: 5;        // updates first element to 5
$mutable;               // prints [ 5, 2 ]
$mutable.3 <: 9;        // error: list index out of range

$tbl: { $x: 1 };
$tbl.x <: 99;           // should work if property rebinding is supported
$tbl;                   // prints { $x: 99 }
$tbl.y <: 42;           // error: '$y' not found for rebinding

// 10. Invalid parenthesis/brackets/braces
(1 + 2;                 // error: unmatched parenthesis
[1, 2, 3;               // error: unmatched bracket
{ $a: 1, $b: 2;         // error: unmatched brace

// 11. Multiple assignments on one line (spacing)
$a:1;$b:2; $a+$b;       // prints 3
$a :  1 ; $b: 2;        // spacing should not break anything

// 12. Unicode and weird strings
$str: "π≈3.14";
$str;                   // prints π≈3.14
$esc: "foo\nbar";       // prints foo\nbar (unless you support real newlines; for now print literal)
$esc2: "foo\"bar\"baz";
$esc2;                  // prints foo"bar"baz

// 14. Markup extension (future)
// (No test here yet, but note to self: someday <enzo> or <markup> context switching should round-trip.)


EOF