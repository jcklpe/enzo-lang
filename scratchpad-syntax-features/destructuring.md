#### Destructuring
<<<NOTE: there maybe a conflict here in syntax between positional and named destructuring now that Arrays and Maps have been consolidated into a single unified "List" data structure>>>
```javscript!
$person : [
  $name: "Todd",
  $age: 27,
  $favorite-color: "blue"
]
$name, $age, $favorite-color -> $shirt-color: $person[];
//or alternatively in the other direction:
$person[] :> $name, $age, $favorite-color -> $shirt-color;

$example-list: [1, 2, 3];
$x, $y, $z: $example-list[];
// $x = 1, $y = 2, $z = 3
```
