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
-----
Currently Enzo relies on something I call "demand driven context" for functions. When a function atom is in a "storage context" it is stored, and not invoked. So `$x: (2*2)` does not invoke the function, it just stores the function body to the $x keyname. But if you wrote `(2*2);` at the top level that would invoke. If you wrote `(2*2)` as an argument being passed to a function parameter it would also invoke, return a value, and then pass that value as the argument to the parameter. If you wanted to pass an actual function object as an argument you'd need to use `@function-name` or `@(...anon function body goes here...)`. If you wanted to immediately invoke an anon function and pass it's value to a key name to be stored in a storage context you'd need to use the `!(...function body...)` syntax. So if you wanted you could write: `$x: !(2*2)` and instead of saving a function to $x it would save the evaluated return value of 4.

But this makes me realize: I've basically created an exception to invoke in storage contexts, and an exception to pass in invocation contexts. Why not simplify this down to a single default and then a single explicit invocation or storage sigil?

I've got a couple of ideas of how this could work:

```
@variable-name: 10; // stores the value, Number type, to @variable-name.
!variable-name; // invokes the variable-name and returns value 10

@variable-name2: @variable-name; // Stores a reference to @variable-name to @variable-name2.
!variable-name2; // invokes !variable-name2 which is a reference to @variable-name which stores the value of 10 which it returns.

@variable-name3: !variable-name2; // invokes !variable-name2 which returns a value of 10 which gets assigned to @variable-name3 keyname
@variable-name <: 12; // rebinds the value of 12 to @variable-name

!variable-name2; // returns 12  (enzo currently has a transparent pointer model rather than repointable reference model implemented)
!variable-name; // returns 12

@function-name: (2*2);  // stores the value of `(2*2)`, type Function, to @function-name

@complex-value: !(4 *4); // stores the value of 4, type Number, to @complex-value

@global-val: 5; // stores the value of 5, type Number, to @global-val

@function-name2: (!global-val + 1); // stores the value of `(!global-val + 1)`, type Function, to @function-name2
!function-name2; // invokes !function-name2 and returns a value of 6

@complex-value2: !(!global-val + 1); // stores the value of 6, type Number, to @complex-value2;
!complex-value2; // invokes and returns value of 6

@global-val <: 2; // rebinds the value of 2 to @global-val

!function-name2; // invokes !function-name2 and returns a value of 3

!complex-value2; // invokes and returns value of 6

// Higher order functions
// 1. Store the function definition
@increment: (param @number: ; return(!number + 1));

// 2. Define the higher-order function
@applyTwice: (
  param @function: (); // Expects a function object
  param @value: 1;
  return(!function(!function(!value))); // Explicitly invoke the function
);

// 3. Pass the function by its handle
!applyTwice(@increment, 7); // returns 9

// Example with anon function
!applyTwice(@(param @x: 0; @x + 4), 7); // returns 15 (7 + 4 + 4)

// for loops

// Store the list
@list-for-ref: [10, 20, 30];

// loop by copy
Loop for @item in !list-for-ref, (
  @item <: !item + 1; // Rebind the temp !item value but not the original value in the list
);

!list-for-ref; // returns [10, 20, 30]

// loop by reference
Loop for @item in @list-for-ref, (
  @item <: !item + 1; // Rebind the referenced value
);

!list-for-ref; // returns [11, 21, 31]


// Destructuring by copy versus by reference:
// 1. Store the main list
@person: [
  $name: "Todd",
  $age: 27
];

// 2. Destructure by creating references
@person[] :> @name, @age;

// 3. Mutating the reference affects the original
"Tim" :> @name;
!person.name; // returns "Tim"

!person[] :> @name, @age; // this would create new @name, and @age variables which copy the values from person and when mutated would not effect !person. You'd need to restructure

// Partial application
@add5: @add( , 5);  // basically how it works currently
@add6: !add( , 6);   // this would invoke the function of add. If it didn't have any default variables for the first parameter, then it would error. If it had default variables then it would use them, do the necessary work, and then save that value, type Number, to @add6. This would not be partial application.

// @/! for string literals
@username: "Jacob";
@greeting1: !"Hi, how are you doing <!username>?";
@greeting2: @"Hi, how are you doing <!username>?";

!greeting1;  // "Hi, how are you doing Jacob?"
!greeting2;  // "Hi, how are you doing Jacob?"

@username <: "Todd";
!greeting1;  // "Hi, how are you doing Jacob?"
!greeting2;  // "Hi, how are you doing Todd?"

@"bare literal string example with @ sigil: <!username>"; // this would either error or just be the same as a !"string"


```