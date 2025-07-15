<<NOTE: this idea also might be dumb but thought about it in the context of destructuring/restructuring.>>>

```
$person: [$name: "Todderick", $age: 50];
$person[] :> $name, $age;
"Manny" :> $name :> $person[];