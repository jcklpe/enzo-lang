# enzo-lang

$[image](https://hackmd.io/_uploads/BJTFqAWVex.png)

[$[Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jcklpe/enzo-lang/blob/master/interpreter/demo.ipynb)

Code is the ultimate user interface. It is the final user interface on which all other user interfaces are built. So I think it’s interesting to explore this space as a UX designer.

Originally this started as a fantasy sketch of what I thought a nice language syntax would look like. As I was learning programming stuff, I'd get frustrated or find a particular way of doing things ugly or confusing, so I'd creatively vent by writing this document and it helped me understand the programming concepts for the real language I was learning. I had no intention of implementing it, but now I am$

I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment and to help me better understand programming, and I make no pretense that this language is going to ever be used in the real world, or is superior to existing languages in any fashion, aesthetic or otherwise. This is more of an art project.

Also want to give a shout out to the ["Quorum Language Project"](https://quorumlanguage.com/) for opening my eyes to the intersection between UX practice and syntax design.

## Comments
```javascript!
// single line comment, will not appear in final output. This allows you to write things in the source code for you to read and help remember what stuff does.
/' block comment, the use of single quote has better keyboard ergonomics than the star symbol typically used '/
//= Test case title commment. Used for breaking up test cases as part of the automated regression testing and will appear on the frontend to the user.
```

## Atoms
Atoms are a basic unit of data value. Here are some examples of atoms, separated by semicolon punctuation:
```javascript!
5;
"Here's some text";
[5, 6, 7, 8, @name: "Fred"];
(2 * 2);
```

### Variable reference versus invocation
Atoms can be bound to a keyname using the `:` operator. A keyname + atomvalue is a variable.

When binding the atomvalue to the keyname it is distinguished with the `@` sigil to indicate that this is a keyname reference.
```javascript!
@keyname: atomvalue;
```


When you want to invoke the keyname to express that bound value you can do it like this:
```javascript!
$keyname;
```

### Atom types
There are 4 types of atoms. These types are [static but inferred](https://www.perplexity.ai/search/plain-language-explanation-of-bIpK7TNKTtCK.Ao8RdeIuw).

#### Number atom
A Number atom is any [real number](https://en.wikipedia.org/wiki/Real_number).

```javascript!
100;
0;
120000;
0.5;
-300;
```

Example of a Number atom bound a keyname and invoked:
```javascript!
@number-example: 888;
$number-example; // returns the value of `888`
```

#### Text (string)
A Text atom is any sequence of characters enclosed in double quotes `"..."`.
This includes letters, numbers, punctuation, spaces, emoji, or [any valid Unicode symbol](https://en.wikipedia.org/wiki/Unicode).

```javascript!
"hello world";
"100";     // note: this is *Text*, not a Number
"π ≈ 3.14159";
"emoji: 😀";
"name_stuff_123";
"line\nbreak"; // newlines and escape sequences allowed
```

Example of Text atom bound a keyname and invoked:
```javascript!
@text-example: "here is some text";
$text-example; // returns the value of `"here is some text"`
```

### List (array/List/map/object/dict)
A List atom is an ordered sequence of values, either atoms, keynames referencing atomvalues, or keyname-atomvalue pairs, enclosed in brackets `[...]`.

```javascript!
[1, 2, 3];
["a", "b", "c"];
[1, "two", [3], @four, [@5-list: "value"]];
[@name: "Alice", @age: 30];
[
    one: 1,
    @two-and-three: [2, 3],
    @can-nest: [
        @nested: "yes"
    ]
];
```

Example of List atom bound to to a keyname and invoked:
```javascript!
@list-example: ["here is some text", 666, @keyname-example];
$list-example; // returns the value `["here is some text", 666, @keyname-example]`
```

Example of a List making heavy use of nested keyname-atomvalue pairs:
```javascript!
@list-example: [
    @property: "this is a value which is paired to the property",
    @property2: 2,
    @property3: [@variable, 3, "three"],
        @property4: [
            @property: "second layer of a nested List",
            @property2: "lists are basically the same as maps or objects in other languages"],
            @exampleFunction: (
            return("this is what a List function (method) looks like");
            ),
            @property3: [
                @property: "third layer of a nested List",
                @property2: "you can nest lists as deeply as you want",
                @property3:"this property value could be invoked using '$list-example.property4.property3'"]
];
```

You can access a specific item in the List via a numbered index like so:
```javascript!
@colors: ["red", "green", "blue", "yellow"];

@firstColor:  @colors.1;   // "red"
@thirdColor:  @colors.3;   // "blue"

// Using a simple computed index
@indexToFind: 2;
$colors.$indexToFind;  // resolves to `$colors.2` → "green"

// More complex computed index requires a function atom:
$colors.($indexToFind + 1); // resolves to `$colors.3` → "blue"
```
The numeric indexing of Lists starts at 1.

#### Dot-Numeric vs. Property Access
- **List property access** uses a “dot + identifier” (e.g. `@user.name`).
- **List indexing** uses a “dot + integer literal” (e.g. `@user.friends.2`)—the parser sees the digit immediately after the dot and interprets it as List indexing rather than property lookup.

```javascript!
// accessing a value via property keyname versus index:
@user: [
  @name: "Alice",
  @logs: ["login","logout","login"]
];

// To get "logout":
$user.logs.2;    // → "logout"
```

### Interpolation
Sometimes you need to insert a value into another value. Many languages do this with concatenation, or spread operators but Enzo does this through interpolation.
#### Text interpolation
Text interpolation allows you to insert dynamic values into Text:
```javascript!
@name: "Bob";
@favorite-color: "blue";
@request-shirt: "Hi, my name is <$name>, can I get a <$favorite-color> shirt, please?";
$request-shirt; // invokes "Hi, my name is Bob, can I get a blue shirt, please?"

// You can also run functions in interpolation (functions explained below)
@number-example: 5;
@number-example2: 3;
@text-example: "the result of the two variables added together is <($number-example + $number-example2;)>"

$text-example; //returns the Text "the result of the two variables added together is 8"
```

#### List interpolation (spread/append/prepend)
List interpolation allows you to make new lists from other lists or values.

Example of non-interpolated List composition:
```javascript!
@list1: [1, 2, 3];
@list2: [4, 5, 6];

@list3: [$list1, $list2];
$list3; // returns a nested List of `[[1, 2, 3], [4, 5, 6]]`
```

Example of interpolated List composition:
```javascript!
@list1: [1, 2, 3];
@list2: [4, 5, 6];

@list3: [<$list1>, <$list2>];
$list3; // returns a flat List of `[1, 2, 3, 4, 5, 6]`

// you can prepend or append items to a List using interpolation like so:
//prepend
[0, <$list1>] :> @list1;
$list1; // returns a List of `[0, 1, 2, 3]`

//append
@list1<: [<$list1>, "hot dog explosion"];
$list1; // returns a List of `[0, 1, 2, 3, "hot dog explosion"]`
```

### Function (anonymous function/expression block)
A function atom is a piece of code that does something and gives an atomvalue back.

Examples:

Basic arithmetic
```javascript!
$(2 + 2);    // returns 4
$(2 - 3);    // returns -1
$(50 * 100); // returns 5000
$(20 / 5);   // returns 4
$(5 % 2);    // modulo returns 1 (Euclidean style remainder)
```

Function atoms can also have keynames declared inside of them like so:
```javascript!
$(@x: 4; @y: 6; $x + $y); // returns 10
$(@x: 5, @y: 5; $x * $y); // commas can also be used to separate keyname binding declarations
```

Function atoms can also be multi-line:
```javascript!
$(
@x: 100;
@y: 100;
return($x + $y);
); // returns 200
```
Single line function atoms do not require an explicit return. Multi-line function atoms never have implicit return. If you're running any kind of process you expect to have a return value then you will require an explicit return.

Function atoms can also be bound to a keyname.
```javascript!
@function-example: (

    // Parameters are declared inside the function definition.
    // the param keyword distinguishes parameter from private function scoped variables.
    param @argument1: ;
    //Parameters can be bound to an initial argument value that it defaults unless otherwise specified when the function is invoked. If it is declared with an empty (explained below) then that function throws an error.
    param @argument2: 12;
    @example-variable: 666;

    return($argument1 + $argument2 + $example-variable);
);
```

Functions are much more powerful when you assign them to a keyname, because you can pass in arguments to its parameters:
```javascript!
@function1: (
    param @a: 4;
    @x: 5;
    return($x + $a);
);
$function1;      // returns 9, just uses the default parameters, or throws error if there are no defaults
$function1();     // returns 9, just uses the default parameters, or throws error if there are no defaults
$function1(5);   // returns 10, used `5` as an argument for the parameter

function2: (@y: 2; $y + 3);
$function2;      // returns 5
$function2();    // returns 5
$function2(5);   // returns 8
```

#### Forcing immediate evaluation with `$`
Sometimes you want to force immediate evaluation in contexts where function atoms would normally be stored. Use the `$` sigil to immediately invoke the function atom.

```javascript!
// Without $: stores function atom
@func: (2 * 2);                 // Variable type: Function
$func();                         // Call later → returns 4

// With $: forces immediate evaluation
@value: $(2 * 2);               // Variable type: Number, value: 4
@value <: 5;                    // ✅ Type-consistent rebinding
```
**Key benefits:**
- **Type consistency**: Enables rebinding variables with computed values
- **Clear intent**: Makes immediate evaluation explicit rather than context-dependent
- **Flexibility**: Works with any function atom, from simple arithmetic to complex computations

#### Expression Context Rules
**Enzo allows arithmetic and single expressions to appear in most contexts without requiring function atom parentheses:**

```javascript!
// ✅ Bare expressions work in these contexts:
@result: $x + $y;               // assignment
$x + 1 :> @x;                   // rebinding
5 + 3;                          // top-level statement
"Value: <$x + 1>";              // string interpolation
```

**Function atom parentheses are required for:**
```javascript!
// Multi-statement blocks need function atoms for scoping
(@temp: $x + 1; $temp * 2);     // local variables and complex logic

// Storing expressions as function atoms
@func: (2 * 2);                 // stores function atom
```

This design reduces paren noise while maintaining the power of function atoms for complex logic and explicit scoping.

#### Variable shadowing
Variable shadowing is when one variable temporarily overwrites another variable. So for instance:
```javascript!
@x: 0;  // this variable is in the global scope
(@temp: "function scoped"); // the @temp variable is in the function scope.
@temp: 12; // This doesn't create an error because the temp scope hasn't leaked into the global scope
(
    @x: "a totally new variable that is within the function scope via shadowing";
    @temp: "also shadowed";
    // you can declare the @x and @temp here because they are scoped to the function and "shadow" the global scope. Any changes made to variables that are shadowing will not effect the exterior scope
);
```

### Empty variables (null, undefined)
A variable can be created that is empty.
```javascript!
   @x: ;
```

It has no type.

## Variable Rebinding
When a variable has already been declared, but it's value is reasigned it can be done like so:
```javascript!
@dog-name: "Fido";
@dog-name <: "Fluffy";
"Ralph" :> @dog-name;
```

### Filling empty values
When an empty variable is initially created, it has no type. The first non-empty value bound to it locks it into that type.
```javascript!
@x: ; // `@x` has no value or type

@x <: 5; // `@x` now has a value of 5 and a type of Number.

@x <: 6 // totally fine to rebind this variable with a new Number value.
@x <: "five" // ❌ error: cannot bind Text to a Number type variable
```

## Variable Invocation
Default case:
```javascript!
@text-example: "here is some text";
$text-example;
//returns "here is some text"
```

All variables are passed by copy/value
```javascript!
@text-example: "here is some text";
@text-example2: $text-example;
$text-example2; // returns "here is some text"

// This is also true of Lists (unlike Javascript)
@list-example: [@property1: 4, @property2: 4];
@example: $list-example.property1;  // this binds the value of $list-example.property1 to example at time of bind.
@list-example.property1 <: 5;
$example;   // returns 4
```

## Function invocation
```javascript!
@function-example: (
    param @first-number: 1;
    param @second-number: 1;
    @third-number: 1;
    return($first-number + $second-number + $third-number);
    );

// You can invoke a function with or without parens. Without parens will just use default values for params and if there are none it will result in an error:
$function-example;      //returns 3
$function-example();    //returns 3

// Example with arguments passed to the parameters.
$function-example(10, 9);     //returns 20

@function-example2: (
    @first-number: 5;
    param @second-number: ;
    param @third-number: Number;  // If you don't want to give a default but you still want to lock the type of a parameter you can use an explicit declaration of type like so.

    return($first-number * $second-number / $third-number));
)

// arguments can be bound to parameters either by order:
$function-example2(1, 2);    // returns 2.5

// or by named binding
$function-example2(@third-number<: 2, @second-number<: 3);   // returns 7.5

$function-example2();     // returns error, due to missing arguments
```

Functions like all other variables are also passed by copy/value:
```javascript!
@global-var: 5;
@function-example: (
    return($global-var);
);
@example: $function-example();
$example; // returns 5
@global-var<: 6;
$example; // still returns 5;
```

Example of function invocation passed as an argument for another function's parameter:
```javascript!
@campfire-status: "unlit";

@get-campfire-status: (
    return($campfire-status);
);

@announce: (
    param @status-value:"";
    "campfire: <$status-value>";
);

$announce($get-campfire-status());
// Expected output: "campfire: unlit"

@campfire-status <: "lit";

$announcer($get-campfire-status());    // Expected output: "campfire: lit"
```

Function atoms can be saved to a keyname like any other atomvalue, even keynames in lists, and they can also be invoked pretty much the same way from the List as any other item:
```javascript!
@dog: [
    @name: "Ralph",
    @speak: (
        return("yo, my name is <$self.name>");
    ),
    @play-dead: (
        param @assailant: "";
        return("ah$ I was murdered by <$assailant>$");
    ),
];

$dog.name;                  //returns "Ralph"
$@dog.speak();              // returns "yo, my name is Ralph"

$dog.play-dead("Tom");      //returns "ah$ I was murdered by Tom$"

//piping the return value into a function
$toLowerCase($dog.name);
//returns "ralph"

$toLowerCase($dog.play-dead("Jerry"));
// returns "ah$ i was murdered by jerry$"
```

Example of invoking a List function and also passing an additional function as a parameter:
```javascript!
@animal: [
    @dog: [
        @bark: (
            param @status: ;
            param @message: ;
            If $status is "loud", (
                return( $toUpper($message) );
            );
            Else, (
                return( $toLower($message) );
            );
        );
    ]
];

@getCurrentStatus: (
    return("loud");
);

// Invocation: property access via dot notation and function invocation via prefix (nested) style.
$animal.dog.bark($getCurrentStatus(), "Bark Bark");    // returns BARK BARK
```

## Invocation versus reference
Enzo distinguishes **invoking** a variable or function (by value/copy) from **referencing** it using the `@` sigil. This is a generalized solution to reference versus copy across Enzo.
```javascript!
@variable;        // returns a reference to the variable, not it's value
@function-name;   // returns a reference to the function
```

Unlike most languages where functions are referenced by omitting the parentheses, function name with no sigil or parens is always an error:
```javascript!
function-name; // this is always an error$
```

Example of this in action for simple variables:
```javascript!
@referenced-value: 8;
@referring-variable: @referenced-value;
$referring-variable;  // returns 8
@referenced-value<: 9;
$referring-variable;  // returns 9
@referring-variable<: 10;
$referenced-value;  // returns 10
```

Example of this in action for function reference:
```javascript!
// 1) Define a function
@increment: (
  param @number: ;
  return($number + 1);
);

// 2) Call it directly:
@total: $increment(5);
// 6 is now bound to @total

// 3) Bind a function reference to a keyname:
@op: @increment;
// ✓ @op now holds the function object

// 4) Call via your @-bound alias:
@result: $op(10);
// 11 bound to @result

// 5) Higher-order usage:
@applyTwice: (
  param @function:();      // expects a function object
  param @value: 1;          // default value of 1 tells it to expect a Number
  return($function($function($value)));
);

// Pass the function **reference** with `@`:
@twice: $applyTwice(@increment, 7);
// 9 bound to @twice
```

Nameless function atoms are by default references unless explicitly invoked with the `$` sigil:
```javascript!
@funcs-list: [(param @x:; $x + 1), (param @x:; $x * 2)];
$processCustomers($customers, (
    param @customer: ;
    "Email: <$customer.email>";
));
```

### Using a reference for partial application
Sometimes you want to make a new function that is like an existing function but more constrained. Let's say the function take 2 arguments, but you want to make a new one where the second argument is always the same, and only the first one can be customized. You can do this with a feature called "partial application":
```javascript!
@add: (param @a: , param @b: ; $a + $b);
@add5: @add( , 5);

$add5(10);  // returns 15
```


## List Destructuring/Restructuring
Destructuring lets you quickly break a List into separate variables, so you can work with each piece individually. Instead of accessing values with long property paths or indexes, destructuring gives you short, readable names for the things you need, making your code simpler and less error-prone.
It’s especially handy when working with complex data structures or when you want to pull out just the relevant bits from a List.

```javascript!
@person: [
  @name: "Todd",
  @age: 27,
  @favorite-color: "blue"
];

// the List can be destructured by name
@name, @age, @favorite-color -> @shirt-color: $person[];
// the -> operator allows for the renaming of the @favorite-color variable to @shirt-color.

//or alternatively in the other direction:
$person[] :> @name, @age, @favorite-color -> @shirt-color;

// or it can be destructured by List position:
@example-list: [1, 2, 3];
@x, @y, @z: $example-list[];
// `@x` = 1, `@y` = 2, `@z` = 3

// But lists can have both named and positional elements which means that you can also destructure by both name and then position
@person: [5, @foo: 6, 7];
@foo, @bar, @baz: $person[];
// `@foo` = 6 (by name), @bar = 5 (first position), @baz = 7 (second remaining position)
// Users are encouraged to align their named destructuring with their positional destructuring for the sake of clarity:
@person: [5, @foo: 6, 7];
@bar, @foo, @baz: $person[];
```
Destructuring, like all variable declaration and rebinding in Enzo, is copy by value.
If you want to "restructure" values back to the original List they were derived from you can do so like this:

```javascript!
@name<: "Jason";
28 :> @age;
@shirt-color <: "green";

@person[]<: [$name];
@person.name; // returns "Jason"

[$age, $shirt-color -> $favorite-color] :> @person[];
```

If you want to destructure by reference (meaning you want changes to the destructured variables to automatically propagate to the original List being destructured) then you need to use the `@` sigil when destructuring. This makes restructuring unnecessary but means all changes to the destructured variables will effect the original:
```javscript$
@person : [
  @name: "Todd",
  @age: 27,
  @favorite-color: "blue"
];
@person[] :> @name, @age, @favorite-color -> @shirt-color;

"Tim" :> @name;
@person.name; // returns "Tim"
```

## Custom Types
Custom types let you define your own data structures in Enzo, providing clarity, consistency, and type safety throughout your code. They help ensure data matches the expected shape or structure, reducing bugs and improving readability.

### Blueprint (class/interface/struct/product type)
Blueprints are reusable templates in Enzo used to instantiate multiple similar objects or data structures. They clearly define the shape, properties, and default values for these structures, enabling organized, type-safe, and repeatable object creation.

Simple example of creating two goblins with different positions on the board:
```javascript!
Goblin: <[
    health-points: Number,
    position: [Number, Number],
]>;

@goblin-1: Goblin[
    @health-points: 100,
    @position: [10, 10],
]>;

@goblin-2: Goblin[
    @health-points: 100,
    @position: [10, 15],
]>;
```

A blueprint can also be defined with default values:
```javascript!
Goblin: <[
    health-points: 100,
    position: [0, 0],
]>;

@goblin1: Goblin[]; // defaults: health = 100, position = [0, 0]

@goblin2: Goblin[
    @health-points: 105,
    @position: [11, 15],
]>;

@goblin3: Goblin[
    // Users can omit any fields they don't want to change from the defaults.
    @position: [10, 10],
]>;
Goblin: <[
    health-points: Number,
    position: [Number, Number],
    attacks: [
        @bite: Number,
        @torch: Number,
    ],
    status-effect: Text,
]>;

@take-damage: (
    param @target: ;              // expects a target of the damage
    param @damage: 0;
    $target.health-points - $damage :> @target.health-points;
    return(@target);              // returns target so it can be used in further pipelines
);

@goblin-1: Goblin[
    @health-points: 100,
    @position: [10, 10],
    @attacks: [
        @bite: 50,
        @torch: 40,
    ],
    @status-effect: "poisoned"
];

@goblin-2: Goblin[
    @health-points: 110,
    @position: [15, 10],
    @attacks: [
        @bite: 55,
        @torch: 35,
    ],
    @status-effect: "none"
];

$goblin-1 then take-damage($this, 10) :> @goblin-1; // `@goblin-1` takes damage and is returned by the function with it's health points decreased by 10. @goblin-2 still has 110 health. Two things coming from the same blueprint.
```

#### Composing blueprints together
You can combine blueprints to reuse common parts, like sharing properties or abilities.

```javascript!
Animal: <[
    position: [Number, Number, Number]
]>;

Flying-Animal: <[
    @wings: "true",
    @fly: (
        param @z-position-movement: Number;
        $self.position.3 + $z-position-movement :> @self.position.3;
        return(@self);
    )
]>;

Swimming-Animal: <[
    @lives-near-water: Text,
    @swim: (
        param @x-position-movement: Number;
        param @y-position-movement: Number;
        $self.position.1 + $x-position-movement :> @self.position.1;
        $self.position.2 + $y-position-movement :> @self.position.2;
        return(@self);
    )
]>;

// Combining two blueprints
Duck: Animal and Flying-Animal and Swimming-Animal;

@donald:  Duck[
    @position: [10, 5, 0]
];

// you can add additional blueprint features on by including them at the end
Pelican: Animal and Flying-Animal and Swimming-Animal and  <[large-mouth: "true"]>;
```

Note: If multiple blueprints are composed together and they have conflicting property names (such as both having a "position" property) this is an error. Notice how the "Animal" blueprint above is used to compose in a property that might otherwise be shared between the Flying-Animal and Swimming-Animal blueprints.

### Blueprint Variants (enum/sum type)
Sometimes, you want a value to be one of several specific options. For example, a monster could be a Goblin, an Orc, or a Troll. This is where blueprint variants come in—they group options together and ensure you only use one at a time.

#### (A) Simple Choices
If you just want to specify a valid List of options:

```javascript!
Magic-Type variants: Fire,
                    or Ice,
                    or Wind,
                    or Earth,
                    or Neutral;

@wizard-attacks: [
    @attack-spell-1: Magic-Type.Fire,
    @attack-spell-2: Magic-Type.Ice,
    @flying-spell: Magic-Type.Wind,
    @magic-shield: Magic-Type.Earth,
    @sword: Magic-Type.Neutral
];
```

#### (B) Variants with Blueprints (sum-of-products)
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
        return("Manmeat for dinner$");
    )
]>;

Troll: <[
    health: Number,
    position: [Number, Number],
    bellow: (
        return("RARGH$$$");
    )
]>;

//And then these Blueprints can be grouped together as a variant grouping:
Monster variants: Goblin,
                or Orc,
                or Troll;

@enemy: Monster.Orc[ @health: 100, @position: [5,5], @rage: 20 ];

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
            return("Manmeat for dinner$");
        )
    ]>,
    or Troll: <[
        health: Number,
        position: [Number, Number],
        bellow: (
            return("RARGH$$$");
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
            return("Manmeat for dinner$");
        )
    ]>,
    or Troll: <[
        bellow: (
            return("RARGH$$$");
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
Goblin variants include Fire-Goblin: <[
    elemental-type: Magic-Type.Fire;
]>;
```

## Control flow logic
Control flow logic lets you tell your code how to flow, what direction to go in.
### Conditional flow
Conditional flow logic lets you tell your code what to do next, based on the current state or value of things. It checks conditions (like "Is this List empty?" or "Is the user logged in?") and decides which blocks of code to run.
#### True/false conditions
There is no dedicated "boolean" type in Enzo. All values [are interpreted as either true or false](https://www.perplexity.ai/search/what-is-truthy-and-falsy-in-a-dZk5OogGSRmHQLFjGJB4HA) in control flow statements, according to these rules:
Examples of “true” conditions:

```javascript!
@favNumber: 7;
@username: "Alice";
@items:     [1,2,3];
@config:    [ mode:"dark" ];
@log: ( say("hi"); );
@example: Monster; // Almost all variant groups and variant group values will be coerced to "true" values;
@example2: Monster.Goblin;
```

Examples of “false” conditions:
```javascript!
@zero: 0;
@emptyText: "";
@emptyList: [];
@emptyList: [0,0,0];
@emptyTbl:  [];
@emptyTbl2: [key: ;];
@no-operation: ( );
@no-operation2: ( param: ;);
@unset:     ;
@kinda-hacky: False; // Built in variant group explained below.
@hacky2: Status.False; // Built in variant group explained below.
```

The built in blueprint variant groups `True`, `False`, and `Status` (with builtin members `Status.True`, and `Status.False`) are provided out of the box. These are provided for the sake of readability, they're not a proper separate "Boolean type" as found in many other languages. They can be extended by the user, such as adding things like `Status.Loading`, `Status.Dead`or what have you.`False` and `Status.False` are the only variant group or variant values which return false in a truth condition context. Kinda hacky? ...True$

Comparisons and functions do not automatically return a boolean type, but functions may return True or False by convention.

#### If
`If` by itself just checks for a true condition value.
```javascript!
@fav-color: "blue";

If $fav-color, (
    "I have a favorite color and it is: <@fav-color>.";
);
```

#### Else
Else provides a fallback for if the If condition is not met.
```javascript!
If $status is "red alert", (
    "Panic$$$";
),
Else, (
    "Nothing to worry about";
);
```

#### Else if
If you want to chain several if statements in a row, but only have the subsequent ones fire if the prior one fails you can use `Else if`.
```javascript!
If $status is "red alert",(
    "DANGER$";
);
Else if $status is "yellow alert", (
  "warning$";
);
Else, (
    "Probably not a big deal";
);
```

#### not
Add in `not` to test for false condition values instead of true condition values.

```javascript!
@fav-color: "blue";

If not $fav-color, (
    "I have no favorite color yet."; // this will not run
);

"" :> @fav-color;

If not $fav-color, (
    "I have no favorite color yet."; // this will now run
);
```

Pair `If`, `is`, and `not` and you can now create a comparison context that resolves to a true/false condition value and tests for false conditions.
```javascript!
@status: "red alert";

If $status is not "red alert", (
    "Everything is probably fine."; // this won't fire
);
```

#### Comparison words
Rather than just testing to see if a value resolves to a true/false value, you can also use comparison words to compare values, which then resolve to a true/false value.
##### is
`is` is a comparison word, where rather than simply testing the variable for true/false condition values, a comparison is made, which then resolves to a true/false condition value.

```javascript!
@fav-color: "blue";

If $fav-color is "blue", (
    "fav color is blue";
);
```

*Assigning value operator (`:`)and comparing values (`is`) are visually and semantically distinct which avoids the overloading common in most other programming languages. All comparisons are strict.*

`is` can be used to compare in several ways:

###### Value match
Most of our examples have been value matches. It's just "does this variable match this value":

```javascript!
If $x is 42, (
    "It's the answer$";
);
```

###### Type match
```javascript!
If $x is Number, (
    "It's a number$";
);

If $x is Empty, (
    "Nothing to see here";
);

If $x is Monster.Goblin, (
    "It's a goblin$";
);
```

##### less than
`less than` is a comparison word that checks if a Number is less than another Number.

```javascript!
@temperature: 98;

If $temperature is less than 50, (
    "getting kind of chilly in here";
);
```

##### greater than
`greater than` is a comparison word that checks if a Number is greater than another Number.

```javascript!
@temperature: 98;

If $temperature is greater than 88, (
    "getting kind of warm in here";
);
```

##### at most (<=)
`at most` is a comparison word that checks if a Number is less than or equal to another Number.

```javascript!
@temperature: 98;

If $temperature is at most 120, (
    "I can survive this heat";
);
```

##### at least (>=)
`at least` is a comparison word that checks if a Number is greater than or equal to another Number.

```javascript!
@temperature: 98;

If $temperature is at least 20, (
    "I can survive this coolness";
);
```

##### contains
`contains` is a comparison word that checks if a List contains a value.

```javascript!
@list-example: [1, 2, 3];

If $list-example contains 3, (
    "this List contains a 3.";
);

@list-example2: [@name: "John", @age: 50];

If $list-example2 contains "John", (
    "Hi John$";
);
```

#### Condition combiners
Condition combiners allow you to set several conditions together.
##### and
`and` allows you to test for multiple conditions. Both must resolve to true for the logic to fire.

```javascript!
@status : "red alert";
@temp: 75;

If $status is "red alert" and $temp is 95, (
    "It's getting really hot in the engine room$"; // this logic will not fire
);

@temp <: 95;
If $status is "red alert" and $temperature is 95, (
    "It's getting really hot in the engine room$"; // this logic will now fire
);
```

##### or
`or` allows you to test for multiple conditions, and only one needs to resolve to true for the logic to fire.

```javascript!
@status: "red alert";

If $status is "red alert" or "orange alert", (
    "stuff is looking bad$";
);
```

#### Multi-branch checks (switch statement)
Multi-branch checks let you test one value against several conditions in a row.

```javascript!
@colors: ["blue", "green", "yellow"];

If $colors contains "yellow", (
    "There's a yellow in the mix$";  // This will fire
),
or is ["blue", "green", "yellow"], (
    "It matches the specific color set$"; // This will also fire
);
Otherwise,
    "All other cases failed"; (
);
```

If you want to make it so only the first case that matches fires, then you need to add the `either` keyword:

```javascript!
@colors: ["blue", "green", "yellow"];

If $colors either contains "yellow", (
    "There's a yellow in the mix$";  // This will fire
),
or is ["blue", "green", "yellow"], (
    "It matches the specific color set$"; // This will also fire
);
Otherwise, (
    "All other cases failed";
);
```

Order matters when using `either` so keep that in mind.

#### Inline if statement
```javascript!
If $ready, ("ready to go$"), Else ("not ready yet$");
```
There are no ternaries. I personally find them very difficult to read, but I think this inline syntax is pretty compact all things considered.

### Looping flow
Sometimes you need a set of code to loop. You could do this with recursion but to keep things tidy and readable we have loops.

Example of a simple infinite loop:
```javascript!
Loop, (
"this is the song that doesn't end. Yes, it goes on and on, my friend Some people started singing it not knowing what it was, and they’ll continue singing it forever just because";
);
```

#### Ending a loop (break)
You can end a loop by writing `end-loop;`.
```javascript!
@iteration: 0;
@message: "There have been <$iteration> full iteration/s";
Loop, (
    $iteration + 1 :> @iteration;
    $message;
    end-loop;
); // This will iterate once, print the message and then end.
```

You can use conditional flow stuff to end based on conditions.
```javascript!
@iteration: 0;
@message: "There have been <$iteration> full iteration/s";
Loop, (
    $iteration + 1 :> @iteration;
    $message;
    If $iteration is greater than 10, (
        end-loop;
    );
); // this will print 11 times then end.
```

This allows you to create more complex loops that can end loop in multiple ways.
```javascript!
@iteration: 0;
@found: false;
@item-list: [1, 3, 5, 7, 9, 10, 13, 17];
@target: 10;
@message: "";

Loop, (
    $iteration + 1 :> @iteration;
    @current: $item-list.$iteration;

    If $current is $target, (
        @found <: true;
        @message: "Found <$target> at iteration <$iteration>";
        end-loop;
    );

    If $iteration is greater than 10, (
        @message: "Exceeded iteration count without finding <$target>";
        end-loop;
    );
);
$message;   // Returns "Found 10 at iteration 6"
```

#### Restarting a loop (continue)
Sometimes, you want to immediately jump to the next iteration of a loop, skipping the rest of the statements in the current loop body if a certain condition is met. In Enzo, you can do this with the `restart-loop;` statement.
When the interpreter encounters `restart-loop;`, it stops executing the current loop body and immediately begins the next iteration.

```javascript!
@item-list: [1, 2, 3, 4, 5];
@evens: [];
@index: 1;
Loop, (
    If $index is greater than $item-list.length, (
        end-loop;
    );
    @item: $item-list.$index;
    If ($item % 2) is 1, (   // If @item is odd
        $index + 1 :> @index;
        restart-loop;
    );
    // This code only runs for even Numbers
    [<$evens>, $item] :> @evens;
    $index + 1 :> @index;
);
$evens;  // [2, 4]
```
In this example, whenever @item is odd, `restart-loop;` causes the loop to immediately start the next iteration, so only even Numbers are added to @evens.

#### Conditional loop flow
To have a little more readable and less boilerplate there's also a couple of loop subtypes that put their loop conditions up front. You can still use `end-loop;` to end the loop early, or `restart-loop;` to restart it early.

##### While loops
A loop that continues for as long as a condition holds true.
```javascript!
@iteration: 0;
@message: "There have been <$iteration> full iteration/s";
Loop while $iteration is less than 10, (
    $iteration + 1 :> @iteration;
    $message;
 ); // this will print 10 times
```

##### Until loops
The opposite of a while loop, loops until a condition is not true.
```javascript!
@iteration: 0;
@message: "There have been <$iteration> full iteration/s";
Loop until $iteration is more than 10, (
    $iteration + 1 :> @iteration;
    $message;
); // this will print 10 times
```

#### For loops
Loops through a List:
```javascript!
@item-list: [1, 2, 3, 4, 5];
Loop for $item in $item-list, (
    "this iteration has returned <$item> of <$item-list>";
);
```
Loops are "live iteration" style, meaning that as you loop through the List, any changes to the List will be immediate. You could hypothetically create an infinitely growing loop this way. Not sure if this is better or worse UX than the "snapshot" style, but it seems the most intuitive to me.

Also when you define `$item` over the List you are iterating on, it as a copy (all variables are copy by value in Enzo), so any changes you make to the item will not change the item in the original List. See example here:
```javascript!
@list-for-copy: [10, 20, 30];
Loop for $item in $list-for-copy, (
  @item <: $item + 1; // Mutating the loop variable
  "Item copy is now <$item>"; // prints 11, 21, 31
);
$list-for-copy; // prints [10, 20, 30] - original List is unaffected
```

 But if you want to mutate the item as you iterate you can use the `@` sigil to do like so:
```javascript!
@list-for-ref: [10, 20, 30];
Loop for @item in $list-for-ref, (
  @item <: $item + 1; // Mutating the original variable
  "Item is now <$item>"; // prints 11, 21, 31
);
$list-for-ref; // prints [11, 21, 31] - original List has changed
```

Also important info: When a loop restarts, it starts with a fresh context. Here's an illustration of what that means:
```javascript!
@iteration: 0;
Loop, (
    @x: 0
    $x + 1 :> @x;
    $x; // prints 1
    $iteration + 1 :> @iteration;
    If $iteration is greater than 3, (end-loop);
); // This loop will repeat 3 times, and each time it will print 1. The @x declaration won't be an error because each loop is a fresh context. If you want to have a variable persist between loops it must be declared exterior of the loop.
```

### Data flow
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
@selected: $users then $filter($this, "active") then $sortBy($this, "last-name")then $select($this, ["id","email"]);

// Exactly equivalent to:
@selected: $select($sortBy($filter($users, "active"),"lastName"),["id","email"]);


// You can even us line breaks to keep things more readable:
@selected: $users
then $filter($this, "active")
then $sortBy($this, "lastName")
then $select($this, ["id","email"]);


// or use a "left to right" binding to keep the value going purely from left to right
$users then $filter($this, "active") then $sortBy($this, "lastName")then $select($this, ["id","email"]):> @selected;
```

While `:>` is usually used to rebind values, it can also be used to declare and bind all in one move, which can be useful with pipeline operations so that you can keep a nice `function() then function() then function() :> @final-variable`

The use of the `$this` operator allows for flexibility in how the output of one function gets piped to the next

```javascript!
// move-in(@house, @pet)
// teach (@pet,  @command)
// reward(@pet,  @treat)

$dog
then $move-in($home, $this)       // dog goes in *second* position
then $teach($this, "sit")        // dog again in 1st position of teach
then $reward($this, "rawhide chew")
:> @goodDog;
```

You can also use pipeline operators on Lists:
```javascript!
@colors: ["red", "green", "blue", "yellow"];

$colors
then $toUppercase($this.3);       // index into the result
// → "BLUE"
```

**IMPORTANT NOTE:** `$this` is completely unrelated to the `this` keyword found in other languages like javascript. Do not confuse the two. Enzo uses `@self` for that purpose.

##### Why use `then` pipeline?
- No nesting. Keeps your code flat and readable.
- No method chaining. Functions remain standalone and there's no overloading of dot notation for List property access and piping stuff together.
- Clear data-flow. You always read top-to-bottom, left-to-right.

# Misc implementation details
1. Enzo is expression oriented rather than statement oriented.
2. Enzo is static (lexical) scoped.
3. Enzo **does not** use parentheses for the dual purpose of groupings and code blocks. All parentheses are anon-functions/expression-blocks/code-blocks, however you want to phrase it (in Enzo we call these function atoms). In this way Enzo is a lot like LISP. There is no meaningful distinction between `(10 + 2)` and `(@x + 4)`.

---

## Operator Precedence
(the following might be out of date and is subject to change)

1. List property invocation (`.`)
2. function invocation
3. multiplication and division ( `*`, `/` )
4. addition, subtraction (`+`, `-`)
5. variable declaration and binding ( `:` `<:` `:>`)
6. dataflow operators (`then`, `$this`)
7. comparison operators (`is`, `not`, `is not`, `less than`, `greater than`, `at most`, `at least` )
8. logical operators (`and`, `or`)