instead of requiring closures you could create a shorthand like so:
```
$counter: ($count + 1 :> $count; $count);
```

This would create a var and add to it and then save that to the var all in one go?