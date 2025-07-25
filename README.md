# enzo-lang

![image](https://hackmd.io/_uploads/BJTFqAWVex.png)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jcklpe/enzo-lang/blob/master/interpreter/demo.ipynb)

Code is the ultimate user interface. It is the final user interface on which all other user interfaces are built. So I think it’s interesting to explore this space as a UX designer.

Originally this started as a fantasy sketch of what I thought a nice language syntax would look like. As I was learning programming stuff, I'd get frustrated or find a particular way of doing things ugly or confusing, so I'd creatively vent by writing this document and it helped me understand the programming concepts for the real language I was learning. I had no intention of implementing it, but now I am!

I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment and to help me better understand programming, and I make no pretense that this language is going to ever be used in the real world, or is superior to existing languages in any fashion, aesthetic or otherwise. This is more of an art project.

Also want to give a shout out to the ["Quorum Language Project"](https://quorumlanguage.com/) for opening my eyes to the intersection between UX practice and syntax design.

## Comments

```javascript!
// single line comment, will not appear in final output. This allows you to write things in the source code for you to read and help remember what stuff does.
```

```javascript!
/' block comment, the use of single quote has better keyboard ergonomics than the star symbol typically used '/
```

```javascript!
//= Test case title commment. Used for breaking up test cases as part of the automated regression testing and will appear on the frontend to the user.
```

## Atoms

Atoms are the most basic parts of the enzo language. Atoms are separated by a semi-colon `;` punctuation.

Atoms can be bound to a keyname using the `:` operator. Keynames are distinguished with the `$` sigil.

```javascript!
$keyname: atomvalue;
$keyname; // this invokes the atomvalue
```

You use keynames to more easily invoke that atomvalue where you need in code. An atom bound to a keyname is a variable.

There are 5 types of atoms. These types are [static but inferred](https://www.perplexity.ai/search/plain-language-explanation-of-bIpK7TNKTtCK.Ao8RdeIuw).

### Number atom

A number atom is any [real number](https://en.wikipedia.org/wiki/Real_number).

```javascript!
100;
0;
120000;
0.5;
-300;
```

Example of a number atom bound a keyname:

```javascript!
$number-example: 888;
```

### Text (string)

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

Example of text atom bound a keyname:

```javascript!
$text-example: "here is some text";
```

#### Text interpolation

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

### List (array/list/map/object/dict)

A list atom is an ordered sequence of values, either atoms, keynames referencing those atoms, or keyname-atomvalue pairs, enclosed in brackets `[...]`.

```javascript!
[1, 2, 3];
["a", "b", "c"];
[1, "two", [3], $four, [$5-list: "value"]];
[$name: "Alice", $age: 30];
[
    $one: 1,
    $two-and-three: [2, 3],
    $can-nest: [
        $nested: "yes"
    ]
];
```

Example of list atom bound to to a keyname:
```javascript!
$list-example: ["here is some text", 666, $keyname-example];
```

Example of a list making heavy use of keyname-atomvalue pairs:
```javascript!
$list-example: [
	$property: "this is a value which is paired to the property",
	$property2: 2,
	$property3: [$variable, 3, "three"],
        $property4: [
            $property: "second layer of a nested list",
            $property2: "lists are basically the same as maps or objects in other languages"],
            exampleFunction: (
            return("this is what a list function (method) looks like");
            ),
            $property3: [
                $property: "third layer of a nested list",
                $property2: "you can nest lists as deeply as you want",
                $property3:"this property value could be invoked using '$list-example.property4.property3'"]
];
```


You can access a specific item in the list via a numbered index like so:

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

#### Dot-Numeric vs. Property Access

- **List property access** uses a “dot + identifier” (e.g. `$user.name`).
- **List indexing** uses a “dot + integer literal” (e.g. `$user.friends.2`)—the parser sees the digit immediately after the dot and interprets it as list indexing rather than property lookup.

```javascript!
// List with a numeric property versus a list:
$user: [
  name: "Alice",
  logs: ["login","logout","login"]
];

// To get "logout":
$secondLog: $user.logs.2;    // → "logout"

```

### Function (anonymous function/expression block)

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
($x: 5, $y: 5; $x * $y); // commas can also be used to separate keyname binding declarations
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

Function atoms can also be bound to a keyname.

```javascript!
function-example: (

    // Parameters are declared inside the function definition.
    // the param keyword distinguishes parameter from private function scoped variables.
    param $argument1: ;
    //Parameters can be bound to an initial argument value that it defaults unless otherwise specified when the function is invoked. If it is declared with an empty (explained below) then that function throws an error.
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

#### Function Atom Evaluation

In Enzo, parentheses always create a function atom (an anonymous function/code block).

If a function atom appears in a context that requires its value immediately (such as a top-level statement, string interpolation, or as a value in a return statement), it is immediately invoked.
If a function atom is being bound to a variable, stored in a list or list, or passed as an argument to a function that expects a function, it is stored as a function object and only invoked when called.
This is called demand-driven function atom evaluation.

### Empty variables (null, undefined)

A variable can be created that is empty.

```javascript!
   $x: ;
```

It has no type.

## Variable Rebinding

When a variable has already been declared, but it's value is reasigned it can be done like so:

```javascript!
$dog-name: "Fido";
$dog-name <: "Fluffy";
"Ralph" :> $dog-name;
```

### Filling empty values

When an empty variable is initially created, it has no type. The first non-empty value bound to it locks it into that type.

```javascript!
$x: ;
// $x has no value or type

$x <: 5;
// $x now has a value of 5 and a type of number.

$x <: 6 // totally fine to rebind this variable with a new number value.
$x <: "five"
// ❌ error: cannot bind Text to a Number type variable
```

## Variable Invocation
Default case:
```javascript!
$text-example: "here is some text";
$text-example;
//returns "here is some text"
```

All variables are passed by copy/value
```javascript!
$text-example: "here is some text";
$text-example2: $text-example;
$text-example2; // returns "here is some text"

// This is also true of Lists (unlike Javascript)
$list-example: [$property1: 4, $property2: 4];
$example: $list-example.property1;
$list-example.property1 <: 5;
$example;   // returns 4

```

## Function invocation

```javascript!
function-example: (
    param $first-number: 1;
    param $second-number: 1;
    $third-number: 1;
    return(($first-number + $second-number + $third-number));
    );

// You can invoke a function in three equal ways:
function-example(); //returns 3
$function-example; //returns 3
$function-example(); //returns 3

// You can invoke a function and pass it arguments in 2 ways:
function-example(10, 9);//returns 20
$function-example(10, 9);//returns 20


// arguments can be bound to parameters either by order
function-example(1, 2);
// returns 2.5

// or by named binding
function-example2($third-number<: 2, $second-number<: 3);
// returns 7.5

function-example2();
// returns error
```

Functions like all other variables are also passed by copy/value:
```javascript!
$global-var: 5;
function-example: (
    return($global-var);
);
$example: function-example();
$example; // returns 5
$global-var<: 6;
$example; // returns 5;
```

## Invocation versus reference
Enzo distinguishes **invoking** a variable or function (by value/copy) from **referencing** it.

Here is how you invoke variables and functions:
```javascript!
$x; // invokes the variable of x and returns its value

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
// 6 is now bound to $total

// 3) Reference it as data (must use $):
$op: @increment;
// ✓ $op now holds the function object

// 4) Call via your $-bound alias:
$result: $op(10);
// 11 bound to $result

// 5) Higher-order usage:
applyTwice: (
  param $function:();      // expects a function object
  param $value: 1;          // default value of 1 tells it to expect a number
  return($function($function($value)));
);

// Pass the function **reference** with `$` and without `()`:
$twice: applyTwice(@increment, 7);
// 9 bound to $twice
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
    "campfire: <$status-value>";
);

announce(get-campfire-status());
// Expected output: "campfire: unlit"

$campfire-status <: "lit";

announcer(get-campfire-status());
// Expected output: "campfire: lit"
```

#### Invoking a function from a list property

```javascript!
$dog: [
    $name: "Ralph",
    speak: (
        return("yo, my name is <$self.name>");
    ),
    play-dead: (
        param $assailant: "";
        return("ah! I was murdered by <$assailant>!");
    ),
];

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

Example of invoking a list function and also passing an additional function as a parameter

```javascript!
$animal: [
    $dog: [
        $bark: (
            param $status: ;
            param $message: ;
            if $status = "loud",
                return( toUpper($message) );
            else,
                return( toLower($message) );
            end;
        );
    ]
];

getCurrentStatus: (
    return("loud");
);

// Invocation: property access via dot notation and function invocation via prefix (nested) style.
$animal.dog.bark(getCurrentStatus(), "Bark Bark");
// returns BARK BARK

```

### List Destructuring/Restructuring
Destructuring lets you quickly break a list into separate variables, so you can work with each piece individually. Instead of accessing values with long property paths or indexes, destructuring gives you short, readable names for the things you need, making your code simpler and less error-prone.
It’s especially handy when working with complex data structures or when you want to pull out just the relevant bits from a list.
```javscript!
$person: [
  $name: "Todd",
  $age: 27,
  $favorite-color: "blue"
];

// the list can be destructured by name
$name, $age, $favorite-color -> $shirt-color: $person[];
// the -> operator allows for the renaming of the $favorite-color variable to $shirt-color.

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

### Custom Types
Custom types let you define your own data structures in Enzo, providing clarity, consistency, and type safety throughout your code. They help ensure data matches the expected shape or structure, reducing bugs and improving readability.

#### Blueprint (class/interface/struct/product type)
Blueprints are reusable templates in Enzo used to instantiate multiple similar objects or data structures. They clearly define the shape, properties, and default values for these structures, enabling organized, type-safe, and repeatable object creation.

Simple example of creating two goblins with different positions on the board:
```javascript!
Goblin: <[
    health-points: Number,
    position: [Number, Number],
]>;

$goblin-1: Goblin[
    $health-points: 100,
    $position: [10, 10],
]>;

$goblin-2: Goblin[
    $health-points: 100,
    $position: [10, 15],
]>;
```

A blueprint can also be defined with default values:
```javascript!
Goblin: <[
    health-points: 100,
    position: [0, 0],
]>;

$goblin1: Goblin[]; // defaults: health = 100, position = [0, 0]

$goblin2: Goblin[
    $health-points: 105,
    $position: [11, 15],
]>;

$goblin3: Goblin[
    // Users can omit any fields they don't want to change from the defaults.
    $position: [10, 10],
]>;
```

```javascript!
Goblin: <[
    health-points: number,
    position: [number, number],
    attacks: [
        $bite: number,
        $torch: number,
    ],
    status-effect: text,
]>;

take-damage: (
    param $target: ;              // expects a target of the damage
    param $damage: 0;
    $target.health-points - $damage :> $target.health-points;
    return($target);              // returns target so it can be used in further pipelines
);

$goblin-1: Goblin[
    $health-points: 100,
    $position: [10, 10],
    $attacks: [
        $bite: 50,
        $torch: 40,
    ],
    status-effect: "poisoned"
];

$goblin-2: Goblin[
    $health-points: 110,
    $position: [15, 10],
    $attacks: [
        $bite: 55,
        $torch: 35,
    ],
    status-effect: "none"
];

$goblin-1 then take-damage($this, 10) :> $goblin-1; // $goblin-1 takes damage and is returned by the function with it's health points decreased by 10. $goblin-2 still has 110 health. Two things coming from the same blueprint.
```

##### Composing blueprints together
You can combine blueprints to reuse common parts, like sharing properties or abilities.
```javascript!
Animal: <[
    position: [Number, Number, Number]
]>;

Flying-Animal: <[
    $wings: "true",
    fly: (
        param $z-position-movement: Number;
        $self.position.3 + $z-position-movement :> $self.position.3;
        return($self);
    )
]>;

Swimming-Animal: <[
    $lives-near-water: Text,
    swim: (
        param $x-position-movement: Number;
        param $y-position-movement: Number;
        $self.position.1 + $x-position-movement :> $self.position.1;
        $self.position.2 + $y-position-movement :> $self.position.2;
        return($self);
    )
]>;

// Combining two blueprints
Duck: Animal and Flying-Animal and Swimming-Animal;

$donald:  Duck[
    $position: [10, 5, 0]
];

// you can add additional blueprint features on by including them at the end
Pelican: Animal and Flying-Animal and Swimming-Animal and  <[large-mouth: "true"]>;


```

Note: If multiple blueprints are composed together and they have conflicting property names (such as both having a "position" property) this is an error. Notice how the "Animal" blueprint above is used to compose in a property that might otherwise be shared between the Flying-Animal and Swimming-Animal blueprints.


##### Blueprint Variants (enum/sum type)
Sometimes, you want a value to be one of several specific options. For example, a monster could be a Goblin, an Orc, or a Troll. This is where blueprint variants come in—they group options together and ensure you only use one at a time.

###### (A) Simple Choices
If you just want to specify a valid list of options:
```javascript!
Magic-Type variants: Fire,
                    or Ice,
                    or Wind,
                    or Earth,
                    or Neutral;

$wizard-attacks: [
    $attack-spell-1: Magic-Type.Fire,
    $attack-spell-2: Magic-Type.Ice,
    $flying-spell: Magic-Type.Wind,
    $magic-shield: Magic-Type.Earth,
    $sword: Magic-Type.Neutral
];
```

###### (B) Variants with Blueprints (sum-of-products)
You can also define variants where each choice has its own structure:
```javascript!
Goblin: <[
    health: Number,
    position: [Number, Number],
    cackle: (
        return("heeheehee");
    )
]>;

Orc: <[
    health: Number,
    position: [Number, Number],
    shout: (
        return("Manmeat for dinner!");
    )
]>;

Troll: <[
    health: Number,
    position: [Number, Number],
    bellow: (
        return("RARGH!!!");
    )
]>;

//And then these Blueprints can be grouped together as a variant grouping:
Monster variants: Goblin,
                or Orc,
                or Troll;

$enemy: Monster.Orc[ $health: 100, $position: [5,5], $rage: 20 ];

// Blueprints can be included in multiple variant groupings:
Boss-Monster variants: Troll,
                    or Nazgul,
                    or Mind-Flayer;

```

You could also define the Blueprint variant grouping and the Blueprints all in one go too:
```javascript!
Monster variants:
    Goblin: <[
        health: Number,
        position: [Number, Number],
        cackle: (
            return("heeheehee");
        )
    ]>,
    or Orc: <[
        health: Number,
        position: [Number, Number],
        shout: (
            return("Manmeat for dinner!");
        )
    ]>,
    or Troll: <[
        health: Number,
        position: [Number, Number],
        bellow: (
            return("RARGH!!!");
        )
    ]>;

```

You can even compose shared blueprints across a blueprint variant grouping and the variants all in one go:
```
Monster variants:
    Monster: <[
        health: Number,
        position: [Number, Number]
    ]>,
    and Goblin: <[
        cackle: (
            return("heeheehee");
        )
    ]>,
    or Orc: <[
        shout: (
            return("Manmeat for dinner!");
        )
    ]>,
    or Troll: <[
        bellow: (
            return("RARGH!!!");
        )
    ]>;
// Goblin, Orc, and Troll all share the Monster qualities defined in the Monster Blueprint

```

You can use those variant grouping values (as in case A) as values in other blueprints too (such as in case B):
```javascript!
Goblin variants:
    Goblin: <[
        health: Number,
        position: [Number, Number],
        elemental-type: Magic-Type
    ]>,
    and Ice-Goblin: <[
        elemental-type: Magic-Type.Ice
    ]>,
    or Earth-Goblin: <[
        elemental-type: Magic-Type.Earth
    ]>,
    or Normal-Goblin: <[
        elemental-type: Magic-Type.Neutral
    ]>;

```

You can add to an existing variant group like so:
```javascript!
Goblin variants: Fire-Goblin: <[
    elemental-type: Magic-Type.Fire;
]>;
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


// or use a "left to right" binding to keep the value going purely from left to right
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
- No method chaining. Functions remain standalone and there's no overloading of dot notation for list property access and piping stuff together.
- Clear data-flow. You always read top-to-bottom, left-to-right.

# Misc implementation details

1. Enzo is expression oriented rather than statement oriented.
2. Enzo is static (lexical) scoped.
3. Enzo **does not** use parentheses for the dual purpose of groupings and code blocks. All parentheses are anon-functions/expression-blocks/code-blocks, however you want to phrase it (in Enzo we call these function atoms). In this way Enzo is a lot like LISP. There is no meaningful distinction between `(10 + 2)` and `($x + 4)`.

---

## Operator Precedence

(the following might be out of date and is subject to change)

1. list property invocation (`.`)
2. function invocation
3. multiplication and division ( `*`, `/` )
4. addition, subtraction (`+`, `-`)
5. variable declaration and binding ( `:` `<:` `:>`)
6. dataflow operators (`then`, `$this`)
7. comparison operators (`is`, `not`, `is not`, `less than`, `greater than`, `at most`, `at least` )
8. logical operators (`and`, `or`)

## Desugaring catalogue
| Sugar syntax                                    | Core form after parse-rewrite               |
| ------------------------------------------------- | --------------------------------------------- |
| **Pipeline** `$v then foo($0,1)`                | `foo($v,1)`                                 |
| **Inline if** `if cond, a, else b`              | `if cond then a else b end`                 |
| **List destructure** `$x,$y : [1,2]`            | `$tmp : [1,2]; $x : $tmp[0]; $y : $tmp[1];` |

## To-do and Questions:
- casting solutions?

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
