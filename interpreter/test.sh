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
$empty-list: ["now not empty"];
$empty-list;       // prints “[ "now not empty" ]”

// ── 13) DECLARE LIST AND ACCESS ITEMS ────────────────────────────────────────
$colors: ["red", "green", "blue", "yellow"];
$colors.3;         // prints “blue”
$i: 2;
$colors.$i;        // prints “green”

// ── 14) NESTED LISTS WITH INDEXING ──────────────────────────────────────
