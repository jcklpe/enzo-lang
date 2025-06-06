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
$empty-list: 50;    //this should error
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
$emptyTable.someKey;    // error: 'someKey'

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
$newImplicit :> 55;
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
$prim.someKey <: 5;       // error: property rebind applies to tables

$myTbl: { $a: 1 };
$myTbl.1;                 // error: index applies to lists
EOF