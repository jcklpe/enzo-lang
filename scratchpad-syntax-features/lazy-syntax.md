Currently have @() for passing anon functions as references, but the one remaining need for that is when passing an anon function reference as an argument to a function param. If function params were a "storage" context then that would eliminate the need for @() all together. Furthermore if we just made all contexts "storage" contexts except for !() then that simplifies the mental model by quite a bit (though it would run counter to the typical way things are done and would basically move Enzo closer to Haskell's lazy eval way of doing things.) It could even make it so that invoking a function required a bang with !function-name() to invoke and function-name() just being the function body.

Let's try to push down this path further just as an intellectual exercise. How would you pass a variable by reference? Well everything is a reference right? So in this case I think you would just pass it like this:
```
$referenced-var: 10;
$referencing-var: $referenced-var;

$referencing-var; // prints 10

$referenced-var <: 11;

$referencing-var; // prints 11
```

But what if you want to save the value of $referenced-var to a variable without referencing it? Like so:
```
$invoked-var:  10;
$copied-value-var: !invoked-var; // variable is invoked using the same sigil as an IIFE function

$copied-value-var; // prints 10

$invoked-var<: 11;
$copied-value-var; // prints 10
```

And then destructuring? Well destructuring would be by reference by default too. Unless you did it like this:
```
$name, $age, $location: !person[];
```

And partial application, well that's referenced by default so you could just do this:
```
add: (param $x: 0, param $y: 0; $x + $y);
add5: add( , 5);

add5(5); // prints 10;
```

more examples:
```// The setup. `User` is a type, not an action. The list is data.
User: <[ name: Text, age: Number, isActive: Status ]>;
users: [
    User[$name: "Alice", $age: 31, $isActive: True],
    User[$name: "Bob", $age: 19, $isActive: True],
    User[$name: "Charlie", $age: 45, $isActive: False]
];
$report_lines: [];

// Rule 4: Control flow is eager. No `!` needed here.
Loop for user in users, (
    // Rule 4: Conditions are evaluated eagerly. No `!` needed.
    // Assuming operators like `and` and `>` are also eager.
    If !user.isActive and !user.age > 30, (
        // String interpolation requires getting the *value* of user.name.
        // The interpolation itself is an action that creates a new string.
        line: "User <!user.name> is eligible.";

        // Appending to a list is a mutation, an action. Force it.
        // We need the *value* of the list and the line to create the new list.
        [<!report_lines>, <!line>] :> report_lines;
    );
);

// To print the final result to the console, we need to evaluate it.
!report_lines;
```