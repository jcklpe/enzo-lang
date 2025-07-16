### Loop Controls
Higher order functions are first class citizens in Enzo and have dedicated syntax for their use.

#### Filter

```javascript!
filter $item is "dog" in $original-list :> $filtered-list;
```

#### Transformation (map)

```javascript!
$original-list: [1, 2, 3, 4, 5];

$transformed-list: transform $item in $original-list, $item + 1;

$transformed-list;
// returns [2, 3, 4, 5, 6]
```
