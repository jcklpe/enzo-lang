#### List Destructuring/Restructuring
Destructuring lets you quickly break a list or object into separate variables, so you can work with each piece individually. Instead of accessing values with long property paths or indexes, destructuring gives you short, readable names for the things you need, making your code simpler and less error-prone.
It’s especially handy when working with complex data structures or when you want to pull out just the relevant bits from a list.
```javscript!
$person : [
  $name: "Todd",
  $age: 27,
  $favorite-color: "blue"
];

// the list can be destructured by name
$name, $age, $favorite-color -> $shirt-color: $person[];
//or alternatively in the other direction:
$person[] :> $name, $age, $favorite-color -> $shirt-color;

// or it can be destructured by list position:
$example-list: [1, 2, 3];
$x, $y, $z: $example-list[];
// $x = 1, $y = 2, $z = 3

// But lists can have both named and positional elements which means that you can also destructure by both name and then position
$person: [5, $foo: 6, 7];
$foo, $bar, $baz: $person[];
// $foo = 6 (by name), $bar = 5 (first position), $baz = 7 (second remaining position)
// Users are encouraged to align their named destructuring with their positional destructuring for the sake of clarity:
$person: [5, $foo: 6, 7];
$bar, $foo, $baz: $person[];
```

Destructuring, like all variable declaration and rebinding in Enzo, is copy by value.
If you want to "restructure" values back to the original list they were derived from you can do so like this:
```javascript!
$name<: "Jason";
28 :> $age;
$shirt-color <: "green";

$person[]<: [$name];
$person.name; // returns "Jason"

[$age, $shirt-color -> $favorite-color] :> $person[];
```

 If you want to destructure by reference (meaning you want changes to the destructured variables to automatically propagate to the original list being destructured) then you need to use the `@` sigil when destructuring. This makes restructuring unnecessary but means all changes to the destructured variables will effect the original:
```javscript!
$person : [
  $name: "Todd",
  $age: 27,
  $favorite-color: "blue"
];
@person[] :> $name, $age, $favorite-color -> $shirt-color;

"Tim" :> $name;
$person.name; // returns "Tim"

```