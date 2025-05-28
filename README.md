# enzo-lang

Code is the ultimate user interface. It is the final user interface on which all other user interfaces are built. So I think it’s interesting to explore this space as a UX designer. I have no intention of actually implementing it but playing with syntax like this helps me better understand programming concepts as I’m learning them.

This is just sort of fantasy sketch of what I think a nice language syntax would look like. As I'm learning programming stuff, I'll make notes on what I don't understand or find confusing, and I sketch out what I think could be different, which both provides an outlet and helps me to better understand the real programming language that I'm trying to learn.

I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment and to help me better understand programming.

Also want to give a shout out to the ["Quorum Language Project"](https://quorumlanguage.com/) for opening my eyes to the intersection between UX practice and syntax design.

## Syntax Reference

### Comments

```javascript!
// single line comment
```

```javascript!
//- Comment Title (styled different in editor and can be used for auto documentation purposes)
```

```javascript!
/' block comment, the use of single quote has better keyboard ergonomics than the star symbol typically used '/
```

### Variable Types and Declaration
Types are static but inferred.

Variables are declared with the `:` operator.
##### Text (string)

```javascript!
$text-example: "here is some text";
```

##### Number

```javascript!
$number-example: 888;
```

##### List (array)

```javascript!
$list-example: ["here is some text", 666, $variable-example];
```

##### Table (objects/maps)

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


##### Functions
``` javascript!
function-example: (

    // Parameters are declared inside the function definition.
    // the param keyword distinguishes parameter from private function scoped variables.
    param $argument1: ;
    //Parameters can be assigned an initial value that it defaults unless otherwise specified when the function is called.
    param $argument2: 12;
    $example-variable: 666;

    return($argument1 + $argument2 + $example-variable);
);
```

###### Nameless functions (lambda)
```javascript!
(6, 5; $a * $b;)
// returns 30
```
A named function is simply a nameless function bound to an identifier. We omit the $ on named functions to keep your API surface clean and readable. But if you think of a function more like a computed piece of data, something you’ll pass around, store in tables, or use inline—you can bind a lambda to a $-variable:
```javascript!
// Treating the lambda as “data” that computes a full name:
$full-name: ($first, $last; $first + " " + $last;);

// Invoking it looks just like calling any function:
say($full-name("Alice", "Smith"));
// Expected output: "Alice Smith"
```
Use $-bound lambdas when the value the function returns is the primary focus, when the function itself feels like data in your mental model.

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

#### Calling a table's property values

Text interpolation
```javascript!
$number-example: 5;
$number-example2: 3;
$text-example: "the result of the two variables added together is {{$number-example + $number-example2}}"

$text-example;
//returns the text 'the result of the two variables added together is 8'
```

#### Function invocation

```javascript!
function-example: (
    param $first-number: 1;
    param $second-number: 1;
    $third-number: 1;
    return($first-number + $second-number + $third-number);
    );

function-example();
//returns 3

function-example(10, 9);
//returns 20

function-example2: (
    $first-number: 5;
    param $second-number: ;
    param $third-number: number: ;

    return($first-number * $second-number / $third-number);
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

#### Passing a function as a parameter

Functions are eager evaluation by default:
```javascript!
$campfireStatus: "unlit";

getCampfireStatus: (
    return($campfireStatus);
);

announceEager: (
    param $statusVal;
    say("Eager campfire: {{$statusVal}}");
);

announceEager(getCampfireStatus());
// Expected output immediately: "Eager campfire: unlit"

$campfireStatus <: "lit";

announceEager(getCampfireStatus());
// Expected output immediately: "Eager campfire: lit"
```

Functions can be set to lazy evaluate using `!`:
```javascript!
$campfireStatus: "unlit";

getCampfireStatus: (
    return($campfireStatus);
);

announceLazy: (
    param $statusFn;

    // Wait 5 minutes
    wait(300000);
    say("Lazy campfire: {{$statusFn()}}");
);

announceLazy(!getCampfireStatus());
// Expected output (after 5 minutes delay): "Lazy campfire: lit"
// (Assuming that before 5 minutes elapse, $campfireStatus is updated.)

$campfireStatus <: "lit";

announceLazy(!getCampfireStatus());
// Expected output (after 5 minutes delay): "Lazy campfire: lit"
```


#### Invoking a table property function

```javascript!

$dog: {
    $name: "Ralph",
    speak: (
        return("yo, my name is {{$self.name}}");
    ),
    play-dead: (
        param $assailant: "";
        return("ah! I was murdered by {{$assailant}}!");
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

example of calling a table function and also passing an additional function as a parameter
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
        return("Hi, my name is {{$self.name}} and I'm {{$self.age}} years old.");
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
  
Examples of “true” in conditions:
```javascript!
$favNumber: 7;
$username: "Alice";
$items:     [1,2,3];
$config:    { mode:"dark" };
$log: ( say("hi"); );
```
Examples of “false” in conditions:
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

##### Else If
```javascript!
else if $variable is "orange alert",
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
		say("this iteration has returned {{$parameter}} of {{$list-name}}");
end;
```

##### While

```javascript!
while $number < 10,
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

Enzo provides a pipeline operator,`then`, to thread a value through a sequence of standalone transformations without nesting or method chaining.

By default it passes the output of the last function to the next function as it's first argument. 


```javascript!
// Step-by-step pipeline
$selected: $users then filter("active") then sortBy("last-name")then select(["id","email"]);

// Exactly equivalent to:
$selected: select(sortBy(filter($users, "active", true),"lastName"),["id","email"]);


// You can even us line breaks to keep things more readable:
$selected: $users 
then filter("active", true) 
then sortBy("lastName")
then select(["id","email"]);

// or use a "left to right" assignment to keep the value going purely from left to right
$users then filter("active", true) then sortBy("lastName")then select(["id","email"]):> $selected;

```

You can also explicitly target any parameter slot with $0, it simply gets replaced by the piped-in value:
```
// move-in($house, $pet)
// teach ($pet,  $command)
// reward($pet,  $treat)

$dog
then move-in($home, $0)       // dog goes in *second* position
then teach($0, "sit")        // dog again in 1st position of teach
then reward($0, "treats")
:> $goodDog;
```

##### Why use `then` pipeline?
- No nesting. Keeps your code flat and readable.
- No method chaining. Functions remain standalone and there's no overloading of dot notation for object property access and piping stuff together. 
- Clear data-flow. You always read top-to-bottom, left-to-right.

### Operator Precedence

- `then` has **lower** precedence than ordinary function calls and arithmetic.
- Parentheses may be used to group sub-expressions when needed.

```javascript!
$result: 4 + 6 then multiply-by($0, 5);   // parsed as (5 + 5) then multiply-by()
// output is 50
```


## To-do and Questions:

- array access
- casting solutions etc
- OOP stuff?


# scratch pad
Random notes about things I'm not really sure about yet. 

----
### Built-in Functions

```javascript!
say()
//builtin print function

return()

unpack() 
// spread operator 

toggle()
// like saying status = !status

```
----




