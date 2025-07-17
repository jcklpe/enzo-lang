#### either (exclusive or)
`either` allows you to test for multiple conditions, and only fires if one is true and the rest are false.
```javascript!
$status: "red alert";

If $status is either "red alert" or "orange alert",
    "stuff is looking bad!";
end;
```

$age: 19; if $age between 13 and 19, "teenager" end;

$x: 9; if $x within 1 to 10, "in range" end;

$score: 97; if $score within 3 of 100, "almost perfect"; end;

#### has
`has` is a comparison word that checks if a list has specific keyname.
```javascript!
$list-example2: [$name: "John", $age: 50];

If $list-example2 has $name,
    "What's your name?";
end;
```
------
## **Number-specific Comparison Operators**

- **less than**
   `$n: 7; if $n less than 10, "single digit"; end;`
- **greater than**
   `$temp: 101; if $temp greater than 100, "boiling!"; end;`
- **at most**
   `$tries: 3; if $tries at most 5, "not too many"; end;`
- **at least**
   `$score: 80; if $score at least 70, "passed"; end;`
- **between**
   `$age: 19; if $age between 13 and 19, "teenager"; end;`
- **within**
   `$x: 9; if $x within 1 to 10, "in range"; end;`
- **is even**
   `$num: 4; if $num is even, "even!"; end;`
- **is odd**
   `$num: 7; if $num is odd, "odd!"; end;`
- **divides**
   `$n: 12; if $n divides 3, "divisible"; end;`
- **multiple of**
   `$x: 24; if $x multiple of 6, "yes"; end;`
- **factor of**
   `$a: 5; if $a factor of 20, "is factor"; end;`
- **prime**
   `$n: 7; if $n prime, "prime!"; end;`
- **positive**
   `$bal: 1; if $bal positive, "in the black"; end;`
- **negative**
   `$diff: -4; if $diff negative, "loss"; end;`
- **zero**
   `$remain: 0; if $remain zero, "empty"; end;`
- **nonzero**
   `$qty: 12; if $qty nonzero, "have some"; end;`
- **approximately**
   `$temp: 100.2; if $temp approximately 100, "close enough"; end;`
- **within delta**
   `$score: 97; if $score within 3 of 100, "almost perfect"; end;`
- **increasing**
   `$nums: [1,2,3]; if $nums increasing, "yes"; end;`
- **decreasing**
   `$nums: [3,2,1]; if $nums decreasing, "descending"; end;`
- **monotonic**
   `$nums: [2,2,3,4]; if $nums monotonic, "always up or same"; end;`
- **finite**
   `$val: 5; if $val finite, "real number"; end;`
- **infinite**
   `$val: Infinity; if $val infinite, "unbounded"; end;`
- **integer**
   `$n: 2; if $n integer, "whole number"; end;`
- **decimal**
   `$n: 1.5; if $n decimal, "fractional"; end;`
- **whole**
   `$n: 0; if $n whole, "whole number"; end;`
- **natural**
   `$n: 1; if $n natural, "positive integer"; end;`

------

## **Text/String-specific Comparison Operators**

- **matches**
   `$s: "foo123"; if $s matches "[a-z]+[0-9]+", "format ok"; end;`
- **starts with**
   `$str: "hello"; if $str starts with "he", "yes"; end;`
- **ends with**
   `$str: "hello"; if $str ends with "lo", "ends right"; end;`
- **includes**
   `$t: "encyclopedia"; if $t includes "clop", "has substring"; end;`
- **length is**
   `$word: "hi"; if $word length is 2, "two chars"; end;`
- **shorter than**
   `$word: "cat"; if $word shorter than 5, "short word"; end;`
- **longer than**
   `$word: "encyclopedia"; if $word longer than 10, "long word"; end;`
- **case equals**
   `$txt: "Hello"; if $txt case equals "Hello", "same"; end;`
- **case-insensitive equals**
   `$txt: "Hello"; if $txt case-insensitive equals "hello", "match"; end;`
- **alphabetically before**
   `$a: "ant"; $b: "bat"; if $a alphabetically before $b, "a comes first"; end;`
- **alphabetically after**
   `$a: "zebra"; $b: "yak"; if $a alphabetically after $b, "zebra wins"; end;`
- **contains**
   `$t: "catnip"; if $t contains "nip", "found"; end;`
- **contains word**
   `$s: "the quick fox"; if $s contains word "fox", "animal!"; end;`
- **is blank**
   `$s: ""; if $s is blank, "no input"; end;`
- **is palindrome**
   `$s: "racecar"; if $s is palindrome, "nice"; end;`
- **has prefix**
   `$txt: "reboot"; if $txt has prefix "re", "has prefix"; end;`
- **has suffix**
   `$txt: "testing"; if $txt has suffix "ing", "is gerund"; end;`
- **is url**
   `$link: "https://enzo-lang.org"; if $link is url, "looks like a link"; end;`
- **is email**
   `$addr: "me@example.com"; if $addr is email, "valid email"; end;`
- **is numeric**
   `$x: "1234"; if $x is numeric, "number as string"; end;`

------

## **List/Collection-specific Comparison Operators**

- **contains**
   `$list: [1,2,3]; if $list contains 2, "found"; end;`
- **has**
   `$map: [$foo: 7]; if $map has $foo, "has foo"; end;`
- **contains all**
   `$a: [1,2,3]; if $a contains all [1,2], "has both"; end;`
- **contains any**
   `$b: [4,5,6]; if $b contains any [5,7], "at least one"; end;`
- **contains none**
   `$nums: [1,2,3]; if $nums contains none [4,5], "disjoint"; end;`
- **length is**
   `$l: [1,2,3,4]; if $l length is 4, "four items"; end;`
- **empty**
   `$xs: []; if $xs empty, "nothing here"; end;`
- **not empty**
   `$xs: [9]; if $xs not empty, "has stuff"; end;`
- **unique**
   `$uniq: [1,2,3]; if $uniq unique, "no duplicates"; end;`
- **sorted**
   `$arr: [1,2,3]; if $arr sorted, "in order"; end;`
- **disjoint from**
   `$a: [1,2]; $b: [3,4]; if $a disjoint from $b, "no overlap"; end;`
- **overlaps**
   `$a: [1,2,3]; $b: [2,4,6]; if $a overlaps $b, "common value"; end;`
- **subset of**
   `$a: [1,2]; $b: [1,2,3]; if $a subset of $b, "subset"; end;`
- **superset of**
   `$a: [1,2,3]; $b: [1,2]; if $a superset of $b, "superset"; end;`
- **same items as**
   `$x: [3,2,1]; $y: [1,2,3]; if $x same items as $y, "same, any order"; end;`
- **deep equals**
   `$p: [$x:1, $y:2]; $q: [$x:1, $y:2]; if $p deep equals $q, "matches!"; end;`
- **shallow equals**
   `$p: [$x:1]; $q: [$x:1]; if $p shallow equals $q, "same top level"; end;`
- **count of**
   `$lst: [1,2,3,4]; if $lst count of (item > 2) is 2, "two over two"; end;`

------

## **Hybrid/Structural or Niche Operators**

- **has key**
   `$map: [$foo: 5]; if $map has key $foo, "key present"; end;`
- **has value**
   `$map: [$foo: 5]; if $map has value 5, "value found"; end;`
- **has property**
   `$obj: [$size: 10]; if $obj has property $size, "has property"; end;`
- **is default**
   `$x: 0; if $x is default, "reset"; end;`
- **has shape**
   `$thing: [$foo:1, $bar:2]; if $thing has shape [$foo, $bar], "correct shape"; end;`
- **is subset**
   `$a: [$foo:1]; $b: [$foo:1, $bar:2]; if $a is subset $b, "subset keys"; end;`
- **has type**
   `$arr: [1,2]; if $arr has type number, "all numbers"; end;`
- **contains type**
   `$arr: [1,"a",2]; if $arr contains type text, "has a string"; end;`
- **is cyclic**
   `$lst: [1,2]; $lst[2] <: $lst; if $lst is cyclic, "circular!"; end;`
- **is deep empty**
   `$arr: [[],[]]; if $arr is deep empty, "all empty"; end;`
- **has duplicates**
   `$xs: [1,2,2,3]; if $xs has duplicates, "not unique"; end;`
- **same length as**
   `$a: [1,2,3]; $b: [4,5,6]; if $a same length as $b, "equal size"; end;`
- **matches pattern**
   `$rec: [$id:7, $val:3]; if $rec matches pattern [$id, $val], "conforms"; end;`
- **intersects with**
   `$x: [1,2]; $y: [2,3]; if $x intersects with $y, "intersection!"; end;`
- **shares prefix with**
   `$a: [1,2,3]; $b: [1,2,4]; if $a shares prefix with $b, "common start"; end;`
- **shares suffix with**
   `$a: [3,4,5]; $b: [2,4,5]; if $a shares suffix with $b, "common end"; end;`

------

### **Temporal / State Operators**

- **is before**
   `$a: "2025-07-10"; $b: "2025-07-16"; if $a is before $b, "a is earlier"; end;`
- **is after**
   `$a: "2025-07-20"; $b: "2025-07-16"; if $a is after $b, "a is later"; end;`
- **expires before**
   `$expires: "2025-07-15"; if $expires expires before "2025-07-20", "soon to expire"; end;`
- **valid until**
   `$date: "2025-07-16"; if $date valid until "2025-07-20", "still good"; end;`
- **expired**
   `$exp: "2025-07-10"; if $exp expired, "too late!"; end;`

------

### **Meta/Other**

- **is defined**
   `$x: 5; if $x is defined, "set"; end;`
- **is undefined**
   `$y: ; if $y is undefined, "not set"; end;`
- **is initialized**
   `$z: 0; if $z is initialized, "ready"; end;`
- **has changed**
   `$x: 1; $x:> 2; if $x has changed, "value changed"; end;`
- **is default**
   `$user: ; if $user is default, "using default"; end;`
- **is reference**
   `$ref: @foo; if $ref is reference, "is ref"; end;`
- **is copy**
   `$c: $foo; if $c is copy, "not a ref"; end;`