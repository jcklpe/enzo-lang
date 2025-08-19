Currently Enzo relies on something I call "demand driven context" for functions. When a function atom is in a "storage context" it is stored, and not invoked. So `$x: (2*2)` does not invoke the function, it just stores the function body to the $x keyname. But if you wrote `(2*2);` at the top level that would invoke. If you wrote `(2*2)` as an argument being passed to a function parameter it would also invoke, return a value, and then pass that value as the argument to the parameter. If you wanted to pass an actual function object as an argument you'd need to use `@function-name` or `@(...anon function body goes here...)`. If you wanted to immediately invoke an anon function and pass it's value to a key name to be stored in a storage context you'd need to use the `$(...function body...)` syntax. So if you wanted you could write: `$x: $(2*2)` and instead of saving a function to $x it would save the evaluated return value of 4.

But this makes me realize: I've basically created an exception to invoke in storage contexts, and an exception to reference pass in invocation contexts. Why not simplify this down to a single default and then a single explicit invocation or storage sigil?

I've got a couple of ideas of how this could work:

```javascript!
@variable-name: 10; // stores the value, Number type, to @variable-name.
$variable-name; // invokes the variable-name and returns value 10

@variable-name2: @variable-name; // Stores a reference to @variable-name to @variable-name2.
$variable-name2; // invokes $variable-name2 which is a reference to @variable-name which stores the value of 10 which it returns.

@variable-name3: $variable-name2; // invokes $variable-name2 which returns a value of 10 which gets assigned to @variable-name3 keyname
@variable-name <: 12; // rebinds the value of 12 to @variable-name

$variable-name2; // returns 12  (enzo currently has a transparent pointer model rather than repointable reference model implemented)
$variable-name; // returns 12

@function-name: (2*2);  // stores the value of `(2*2)`, type Function, to @function-name

@complex-value: $(4 *4); // stores the value of 4, type Number, to @complex-value

@global-val: 5; // stores the value of 5, type Number, to @global-val

@function-name2: ($global-val + 1); // stores the value of `($global-val + 1)`, type Function, to @function-name2
$function-name2; // invokes $function-name2 and returns a value of 6

@complex-value2: $($global-val + 1); // stores the value of 6, type Number, to @complex-value2;
$complex-value2; // invokes and returns value of 6

@global-val <: 2; // rebinds the value of 2 to @global-val

$function-name2; // invokes $function-name2 and returns a value of 3

$complex-value2; // invokes and returns value of 6

// Higher order functions
// 1. Store the function definition
@increment: (param @number: ; return($number + 1));

// 2. Define the higher-order function
@applyTwice: (
  param @function: (); // Expects a function object
  param @value: 1;
  return($function($function($value))); // Explicitly invoke the function
);

// 3. Pass the function by its handle
$applyTwice(@increment, 7); // returns 9

// Example with anon function
$applyTwice(@(param @x: 0; @x + 4), 7); // returns 15 (7 + 4 + 4)

// for loops

// Store the list
@list-for-ref: [10, 20, 30];

// loop by copy
Loop for @item in $list-for-ref, (
  @item <: $item + 1; // Rebind the temp $item value but not the original value in the list
);

$list-for-ref; // returns [10, 20, 30]

// loop by reference
Loop for @item in @list-for-ref, (
  @item <: $item + 1; // Rebind the referenced value
);

$list-for-ref; // returns [11, 21, 31]


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
$person.name; // returns "Tim"

$person[] :> @name, @age; // this would create new @name, and @age variables which copy the values from person and when mutated would not effect $person. You'd need to restructure

// Partial application
@add5: @add( , 5);  // basically how it works currently
@add6: $add( , 6);   // this would invoke the function of add. If it didn't have any default variables for the first parameter, then it would error. If it had default variables then it would use them, do the necessary work, and then save that value, type Number, to @add6. This would not be partial application.

// @/$ for string literals
@username: "Jacob";
@greeting1: $"Hi, how are you doing <$username>?";
@greeting2: @"Hi, how are you doing <$username>?";

$greeting1;  // "Hi, how are you doing Jacob?"
$greeting2;  // "Hi, how are you doing Jacob?"

@username <: "Todd";
$greeting1;  // "Hi, how are you doing Jacob?"
$greeting2;  // "Hi, how are you doing Todd?"

@"bare literal string example with @ sigil: <$username>"; // this would either error or just be the same as a $"string"


```