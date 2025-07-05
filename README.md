# enzo-lang
![image](https://hackmd.io/_uploads/BJTFqAWVex.png)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jcklpe/enzo-lang/blob/master/interpreter/demo.ipynb)


Code is the ultimate user interface. It is the final user interface on which all other user interfaces are built. So I think it’s interesting to explore this space as a UX designer.

Originally this started as a fantasy sketch of what I thought a nice language syntax would look like. As I was learning programming stuff, I'd get frustrated or find a particular way of doing things ugly or confusing, so I'd creatively vent by writing this document and it helped me understand the programming concepts for the real language I was learning. I had no intention of implementing it, but now I am!

I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment and to help me better understand programming, and I make no pretense that this language is going to ever be used in the real world, or is superior to existing languages in any fashion, aesthetic or otherwise. This is more of an art project.


Also want to give a shout out to the ["Quorum Language Project"](https://quorumlanguage.com/) for opening my eyes to the intersection between UX practice and syntax design.

## Syntax Reference
### Comments

```javascript!
// single line comment, will not appear in final output. This allows you to write things in the source code for you to read and help remember what stuff does.
```

```javascript!
/' block comment, the use of single quote has better keyboard ergonomics than the star symbol typically used '/
```

```javascript!
//= Test case title commment. Used for breaking up test cases as part of the automated regression testing and will appear on the frontend to the user.
```

### Atoms
Atoms are the most basic parts of the enzo language. Atoms are separated by a semi-colon `;` punctuation.

Atoms can be assigned a keyname using the `:` operator. Keynames are distinguished with the `$` sigil.
```javascript!
$keyname: atomvalue;
$keyname; // this invokes the atomvalue
```
You use keynames to more easily invoke that atomvalue where you need in code. An atom bound to a keyname is a variable.

There are 5 types of atoms. These types are [static but inferred](https://www.perplexity.ai/search/plain-language-explanation-of-bIpK7TNKTtCK.Ao8RdeIuw).
#### Number atom
A number atom is any [real number](https://en.wikipedia.org/wiki/Real_number).
```javascript!
100;
0;
120000;
0.5;
-300;
```

Example of a number atom assigned a keyname:
```javascript!
$number-example: 888;
```

#### Text (string)
A text atom is any sequence of characters enclosed in double quotes `"..."`.
This includes letters, numbers, punctuation, spaces, emoji, or [any valid Unicode symbol](https://en.wikipedia.org/wiki/Unicode).
```javascript!
"hello world";
"100";     // note: this is *text*, not a number
"π ≈ 3.14159";
"emoji: 😀";
"name_stuff_123";
"line\nbreak"; // newlines and escape sequences allowed
```

Example of text atom assigned a keyname:
```javascript!
$text-example: "here is some text";
```

##### Text interpolation
```javascript!
$name: "Bob";
$favorite-color: "blue";
$request-shirt: "Hi, my name is <$name>, can I get a <$favorite-color> shirt, please?";
$request-shirt; // invokes "Hi, my name is Bob, can I get a blue shirt, please?"

// You can also run functions in interpolation (functions explained below)
$number-example: 5;
$number-example2: 3;
$text-example: "the result of the two variables added together is <($number-example + $number-example2;)>"

$text-example;
//returns the text "the result of the two variables added together is 8"
```

#### List (array)
A list atom is an ordered sequence of atoms (or keynames referencing those atomvalues), enclosed in brackets `[...]`.
```javascript!
[1, 2, 3];
["a", "b", "c"];
[1, "two", [3], $four, {$5-table: "value"}];
```

Example of list atom assigned to a keyname:
```javascript!
$list-example: ["here is some text", 666, $keyname-example];
```

You can access a specific item in the list as follows:
```javascript!
$colors: ["red", "green", "blue", "yellow"];

$firstColor:  $colors.1;   // "red"
$thirdColor:  $colors.3;   // "blue"

// Using a computed index
$indexToFind: 2;
$middleColor: $colors.$indexToFind;
// resolves to $colors.1 → "green"

// nested list selection
$reversed: reverse($colors);  // ["yellow","blue","green","red"]
$pick:     $reversed.2;       // → "blue"

```
The numeric indexing of lists starts at 1.

#### Table (object/map)
A table atom is a collection of keyname-atomvalue pairs, enclosed in braces `{...}`.
```javascript!
{$name: "Alice", $age: 30};

{
    $one: 1,
    $two-and-three: [2, 3],
    $can-nest: {
        $nested: "yes"
    }
};
```

Example of table atom assigned to a keyname:
```javascript!
$table-example: {
	$property: "this is a value which is paired to the property",
	$property2: 2,
	$property3: [$variable, 3, "three"],
        $property4: {
            $property: "second layer of a nested table",
            $property2: "tables are basically the same as maps or objects in other languages"},
            exampleFunction: (
            return("this is what a table function (method) looks like");
            ),
            $property3: {
                $property: "third layer of a nested table",
                $property2: "you can nest tables as deeply as you want",
                $property3:"this property value could be invoked using '$table-example.property4.property3'"}
};
```
##### Dot-Numeric vs. Table Property Access

- **Table property access** uses a “dot + identifier” (e.g. `$user.name`).
- **List indexing** uses a “dot + integer literal” (e.g. `$user.friends.2`)—the parser sees the digit immediately after the dot and interprets it as list indexing rather than property lookup.

```javascript!
// Table with a numeric property versus a list:
$user: {
  name: "Alice",
  logs: ["login","logout","login"]
};

// To get "logout":
$secondLog: $user.logs.2;    // → "logout"

// If someone wrote $user.42:
//   ▸ It would look for a numeric index on the table $user.
//   ▸ Because $user is not a List, this is a type error at compile time.
```

Always ensure that the expression to the **left of the dot** is known to be a List at compile time, or you’ll get a type mismatch error.

#### Function (anonymous function/expression block)
A function atom is a piece of code that does something and gives an atomvalue back.

Examples:

Basic arithmetic
```javascript!
(2 + 2);    // returns 4
(2 - 3);    // returns -1
(50 * 100); // returns 5000
(20 / 5);   // returns 4
```

Function atoms can also have keynames declared inside of them like so:
```javascript!
($x: 4; $y: 6; $x + $y); // returns 10
($x: 5, $y: 5; $x * $y); // commas can also be used to separate keyname assignment declarations
```

Function atoms can also be multi-line:
```javascript!
(
$x: 100;
$y: 100;
return(($x + $y));
); // returns 200
```


Single line function atoms do not require an explicit return. Multi-line function atoms must always have an explicit return.

Function atoms can also be assigned to a keyname.

```javascript!
function-example: (

    // Parameters are declared inside the function definition.
    // the param keyword distinguishes parameter from private function scoped variables.
    param $argument1: ;
    //Parameters can be assigned an initial value that it defaults unless otherwise specified when the function is called. If it is declared with an empty (explained below) then that function throws an error.
    param $argument2: 12;
    $example-variable: 666;

    return($argument1 + $argument2 + $example-variable);
);
```

A named function is simply a nameless function bound to a keyname. We omit the $ on named functions to keep things more readable. All  of the following are valid:
```javascript!
$function1: (
    param $a: 4;
    $x: 5;
    return(($x + $a));
);
$function1;      // returns 9
function1();     // returns 9
$function1();    // returns 9
$function1(5);   // returns 10

function2: ($y: 2; $y + 3);
$function2;      // returns 9
function2();     // returns 9
$function2();    // returns 9
$function2(5);   // returns 10
```

##### Function Atom Evaluation
In Enzo, parentheses always create a function atom (an anonymous function/code block).

If a function atom appears in a context that requires its value immediately (such as a top-level statement, string interpolation, or as a value in a return statement), it is immediately invoked.
If a function atom is being bound to a variable, stored in a table or list, or passed as an argument to a function that expects a function, it is stored as a function object and only invoked when called.
This is called demand-driven function atom evaluation.


##### Empty variables (null, undefined)

A variable can be created that is empty.

```javascript!
   $x: ;
```

It has no type.

### Variable Reassignment

When a variable has already been declared, but it's value is reasigned it can be done like so:

```javascript!
$dog-name: "Fido";
$dog-name <: "Fluffy";
"Ralph" :> $dog-name;
```

#### Filling empty values

When an empty variable is initially created, it has no type. The first non-empty value assigned to it locks it into that type.

```javascript!
$x: ;
// $x has no value or type

$x <: 5;
// $x now has a value of 5 and a type of number.

$x <: 6 // totally fine to reassign this variable with a new number value.
$x <: "five"
// ❌ error: cannot assign Text to a Number
```

### Variable Invocation/Use

Default case:

```javascript!
$text-example: "here is some text";
$text-example;
//returns "here is some text"
```

All variables are call by value

```javascript!
$text-example: "here is some text";
$text-example2: $text-example;
$text-example2;
// returns "here is some text"
```

#### Function invocation

```javascript!
function-example: (
    param $first-number: 1;
    param $second-number: 1;
    $third-number: 1;
    return(($first-number + $second-number + $third-number));
    );

function-example();
//returns 3

function-example(10, 9);
//returns 20

function-example2: (
    $first-number: 5;
    param $second-number: ;
    param $third-number: number: ;

    return(($first-number * $second-number / $third-number));
)

// arguments can be assigned to parameters either by order
function-example2(1, 2);
// returns 2.5

// or by named assignment
function-example2($third-number<: 2, $second-number<: 3);
// returns 7.5

function-example2();
// returns error
```

##### Function invocation versus reference

Enzo distinguishes **invoking** a function from **referencing** it.
Invoking a function has parentheses, like this:

```javascript!
function-name();
//or
$function-name();
// or even just this as long as you don't need to pass any arguments to the parameters
$function-name;
```

A function name with no sigil or parens is always an error:
```javascript!
function-name; // this is always an error!
```

Referencing a function however has an `@` sigil:

```javascript!
@function-name;   // returns the function object
@function-name(); // this is an error. You can't do this.

```

Example of this in action:

```javascript!
// 1) Define a function
increment: (
  param $number: ;
  return($number + 1);
);

// 2) Call it directly:
$total: increment(5);
// 6 is now assigned to $total

// 3) Reference it as data (must use $):
$op: @increment;
// ✓ $op now holds the function object

// 4) Call via your $-bound alias:
$result: $op(10);
// 11 assigned to $result

// 5) Higher-order usage:
applyTwice: (
  param $function:();      // expects a function object
  param $value: 1;          // default value of 1 tells it to expect a number
  return($function($function($value)));
);

// Pass the function **reference** with `$` and without `()`:
$twice: applyTwice(@increment, 7);
// 9 assigned to $twice
```

#### Passing a function as a parameter

Functions are eager evaluation by default:

```javascript!
$campfire-status: "unlit";

get-campfire-status: (
    return($campfire-status);
);

announce: (
    param $status-value:"";
    say("campfire: <$status-value>");
);

announce(get-campfire-status());
// Expected output: "campfire: unlit"

$campfire-status <: "lit";

announcer(get-campfire-status());
// Expected output: "campfire: lit"
```

#### Invoking a function from a table property

```javascript!
$dog: {
    $name: "Ralph",
    speak: (
        return("yo, my name is <$self.name>");
    ),
    play-dead: (
        param $assailant: "";
        return("ah! I was murdered by <$assailant>!");
    ),
};

$dog.name;
//returns "Ralph"

$dog.speak();
// returns "yo, my name is Ralph"

$dog.play-dead("Tom");
//returns "ah! I was murdered by Tom!"

//piping the return value into a function
toLowerCase($dog.name);
//returns "ralph"

toLowerCase($dog.play-dead("Jerry"));
// returns "ah! i was murdered by jerry!"
```

Example of calling a table function and also passing an additional function as a parameter

```javascript!
$animal: {
    $dog: {
        $bark: (
            param $status: ;
            param $message: ;
            if $status = "loud",
                return( toUpper($message) );
            else,
                return( toLower($message) );
            end;
        );
    }
};

getCurrentStatus: (
    return("loud");
);

// Invocation: property access via dot notation and function call via prefix (nested) style.
$animal.dog.bark(getCurrentStatus(), "Bark Bark");
// returns BARK BARK

```

#### Destructuring

##### Table destructuring

```javscript!
$person : {
  $name: "Todd",
  $age: 27,
  $favorite-color: "blue"
}

$name, $age, $shirt-color <- $favorite-color: $person{};
```

##### List destructuring

```javscript!
$example-list: [ 1, 2, 3];

$x, $y, $z: $example-list[];
// $x = 1, $y = 2, $z = 3

```

### Blueprints (custom types)

##### Options Blueprint (enum)

```javascript!
Size: <[small, medium, large]>;

$shirt-size: Size.medium;
```

#### Table Blueprint (class/interface/struct)

```javascript!
Person: <{
    name: Text,
    age: Number,
    t-shirt-size: Size,
    greet: (
        return("Hi, my name is <$self.name> and I'm <$self.age> years old.");
    );
}>;

$alice: Person{
    $name: "Alice",
    $age: 30,
    $t-shirt-size: Size.large
};

say($alice.greet);
// Expected output: "Hi, my name is Alice and I'm 30 years old."
```

### Control Flow Statements

*Assigning value operator (`:`)and comparing values (`is`) are visually and semantically distinct which avoids the overloading common in most other programming languages. All comparisons are strict.*

#### Boolean Context

When any expression appears in a conditional position (`if`, `while`, etc.), it is **coerced** as follows:

Examples of “true” conditions:

```javascript!
$favNumber: 7;
$username: "Alice";
$items:     [1,2,3];
$config:    { mode:"dark" };
$log: ( say("hi"); );
```

Examples of “false” conditions:

```javascript!
$zero:      0;
$emptyText: "";
$emptyList: [];
$emptyList: [0,0,0];
$emptyTbl:  {};
$emptyTbl2:  {key: ;};
$no-operation: ( );
$no-operation2: ( param: ;);
$unset:     ;
$no:        false; // there is no standalone boolean type, but false is left in as a potential false value for readability purposes
```

##### If

```javascript!
$fav-color: "blue";

if $fav-color is "blue",
	say("fav color is blue");
end;
```

##### If not

```javascript!
$status: ;

if not $status,
	say("no current status");
end;
```

This just checks for a boolean context value.

##### If is not

```javascript!
$status: "red alert";

if $status is not "red alert",
	say("Everything is probably fine.");
end;
```

##### If and

```javascript!
$status : "red alert";
$temperature: 600;

if $status is "red alert" and $temperature is 50,
    say("It's getting really hot in the engine room!")
end;
```

##### If or

```javascript!
$status: "red alert";

if $status is "red alert" or "orange alert",
    say("stuff is looking bad!")
end;
```

##### If less than

```javascript!
$temperature: 98;

if $temperature is less than 50,
    say("getting kind of chilly in here");
end;
```

##### If greater than

```javascript!
$temperature: 98;

if $temperature is greater than 88,
    say("getting kind of warm in here");
end;
```

##### If at most (<=)

```javascript!
$temperature: 98;

if $temperature is at most 120,
    say("I can survive this heat");
end;
```

##### If at least (>=)

```javascript!
$temperature: 98;

if $temperature is at least 20,
    say("I can survive this coolness");
end;
```

##### Else If

```javascript!
else if $variable is "yellow alert",
  say("warning!");
end;
```

##### Else

```javascript!
else,
	say("Nothing to worry about");
end;
```

##### Inline if statement

```javascript!
if $ready, say("ready to go!"), else say("not read yet!");

```

There are no ternaries. I personally find them very difficult to read, but I think this inline syntax is pretty compact all things considered.

##### For

```javascript!
for $parameter in $list-or-table-name,
		say("this iteration has returned <$parameter> of <$list-name>");
end;
```

##### While

```javascript!
while $number less than 10,
	$number <: $number + 1
end;
```

### Loop Controls

Higher order functions are first class citizens in Enzo and have dedicated syntax for their use.

#### Filter

```javascript!
$filtered-list: filter $item = "dog" in $original-list;
```

#### Transformation (map)

```javascript!
$original-list: [1, 2, 3, 4, 5];

$transformed-list: transform $item in $original-list, $item + 1;

say($transformed-list);
// returns [2, 3, 4, 5, 6]
```

### Dataflow Operators

Enzo provides a pair of dataflow operators,`then` and `$this` to thread a value through a sequence of standalone transformations without nesting or method chaining.

Simple example using function atoms:
```javascript!
100 then ($this + 1); // returns 101
10 then ($this + $this); // returns 20
1 then ($this + 1) then ($this * 3) // returns 6
```

More complex example using named functions:
```javascript!
// Step-by-step pipeline
$selected: $users then filter($this, "active") then sortBy($this, "last-name")then select($this, ["id","email"]);

// Exactly equivalent to:
$selected: select(sortBy(filter($users, "active"),"lastName"),["id","email"]);


// You can even us line breaks to keep things more readable:
$selected: $users
then filter($this, "active")
then sortBy($this, "lastName")
then select($this, ["id","email"]);


// or use a "left to right" assignment to keep the value going purely from left to right
$users then filter($this, "active") then sortBy($this, "lastName")then select($this, ["id","email"]):> $selected;

```

While `:>` is usualy used to rebind values, it can be used to also declare and bind all in one move, which can be useful with pipeline operations so that you can keep a nice `function() then function() then function() :> $final-variable`

The use of the `$this` operator allows for flexibility in how the output of one function gets piped to the next

```javascript!
// move-in($house, $pet)
// teach ($pet,  $command)
// reward($pet,  $treat)

$dog
then move-in($home, $this)       // dog goes in *second* position
then teach($this, "sit")        // dog again in 1st position of teach
then reward($this, "rawhide chew")
:> $goodDog;
```

You can also use pipeline operators on Lists:

```javascript!
$colors: ["red", "green", "blue", "yellow"];

$colors
then $this.3;       // index into the result
// → "BLUE"
```
**IMPORTANT NOTE:** `$this` is completely unrelated to the `this` keyword found in other languages like javascript. Do not confuse the two. Enzo uses `$self` for that purpose.

##### Why use `then` pipeline?
- No nesting. Keeps your code flat and readable.
- No method chaining. Functions remain standalone and there's no overloading of dot notation for table property access and piping stuff together.
- Clear data-flow. You always read top-to-bottom, left-to-right.

# Misc implementation details

1. Enzo is expression oriented rather than statement oriented.
2. Enzo is static (lexical) scoped.
3. Enzo **does not** use parentheses for the dual purpose of groupings and code blocks. All parentheses are anon-functions/expression-blocks/code-blocks, however you want to phrase it (in Enzo we call these function atoms). In this way Enzo is a lot like LISP. There is no meaningful distinction between `(10 + 2)` and `($x + 4)`.


---

## Operator Precedence
(the following might be out of date and is subject to change)
1. table property invocation (`.`)
2. function invocation
3. multiplication and division ( `*`, `/` )
4. addition, subtraction (`+`, `-`)
5. variable declaration and assignment ( `:` `<:` `:>`)
6. dataflow operators (`then`, `$this`)
7. comparison operators (`is`, `not`, `is not`, `less than`, `greater than`, `at most`, `at least` )
8. logical operators (`and`, `or`)


## Desugaring catalogue
| Sugar syntax                                    | Core form after parse-rewrite               |
| ------------------------------------------------- | --------------------------------------------- |
| **Pipeline** `$v then foo($0,1)`                | `foo($v,1)`                                 |
| **Inline if** `if cond, a, else b`              | `if cond then a else b end`                 |
| **List destructure** `$x,$y : [1,2]`            | `$tmp : [1,2]; $x : $tmp[0]; $y : $tmp[1];` |
| **Table destructure** `$name,$age <- $person{}` | `$name : $person.name; $age : $person.age;` |

## To-do and Questions:
- casting solutions etc
- OOP stuff?

# scratch pad

Random notes about things I'm not really sure about yet.

---

### Built-in Functions

```javascript!
say();
//builtin print function

return();
// Exit current function with value.

error(message);
// Raise an exception that halts execution

import("path/to/resource/to/import");
// imports packages

export("component-name")
// exports components (for a potential markup language syntax in the future?)

unpack()
// spread operator ???

toggle()
// like saying status = !status

```
