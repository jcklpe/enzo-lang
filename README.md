# enzo-lang

Code is the ultimate user interface. It is the final user interface on which all other user interfaces are built. So I think it’s interesting to explore this space as a UX designer. I have no intention of actually implementing it but playing with syntax like this helps me better understand programming concepts as I’m learning them.

This is just sort of fantasy sketch of what I think a nice language syntax would look like. As I'm learning programming stuff, I'll make notes on what I don't understand or find confusing, and I sketch out what I think could be different, which both provides an outlet and helps me to better understand the real programming language that I'm trying to learn.

I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment and to help me better understand programming.

Also want to give a shout out to the ["Quorum Language Project"](https://quorumlanguage.com/) for opening my eyes to the intersection between UX practice and syntax design.

## Syntax Reference

### Comments

```javascript
// single line comment
```

```javascript
//- Comment Title (styled different in editor and can be used for auto documentation purposes)
```

```
/' block comment, the use of single quote has better keyboard ergonomics than the star symbol typically used '/
```

### Variable Types and Declaration
Types are static but inferred.

Variables are declared with the `:` operator.
##### Text (string)

```javascript
$text-example: "here is some text";
```

##### Number

```javascript
$number-example: 888;
```

##### List (array)

```javascript
$list-example: ["here is some text", 666, $variable-example];
```

##### Table (objects/maps)

```javascript
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
``` javascript
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

##### Nameless functions (lambda)
```javascript
:(return($variable + $variable2 + $variable3);)

```

### Variable Reassignment

When a variable has already been declared, but it's value is reasigned it can be done like so:

```javascript
$dog-name: "Fido";
$dog-name <: "Fluffy";
"Ralph" :> $dog-name;
```

### Variable Invocation/Use

Default case:
```javascript
$text-example: "here is some text";
$text-example;
//returns "here is some text"
```

All variables are call by value
```javascript
$text-example: "here is some text";
$text-example2: $text-example;
$text-example2;
// returns "here is some text"
```

#### calling a table's property values

Text interpolation
```javascript
$number-example: 5;
$number-example2: 3;
$text-example: "the result of the two variables added together is {{$number-example + $number-example2}}"

$text-example;
//returns the text 'the result of the two variables added together is 8'
```

#### function invocation

```javascript
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
```javascript
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

Functions can be set to eager evaluate using `!`:
```javascript
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

```javascript

$dog: {
    $name: "Ralph",
    speak: (
        return("yo, my name is {{$self.name}}");
    );,
    play-dead: (
        param $assailant: "";
        return("ah! I was murdered by {{$assailant}}!");
    );,
};

$dog.name;
//returns "Ralph"

$dog.speak;
// returns "yo, my name is Ralph"

$dog.play-dead("Tom");
//returns "ah! I was murdered by Tom!"

//piping the return value into a function
toLowerCase($dog.name);
//returns "ralph"

toLowerCase($dog.play-dead("Jerry"));
// returns "ah! i was murdered by jerry!"



```

#### Control Flow Statements

 *`:` is used for assigning values, while `=` is used for comparing values. Having the two be different makes the two more visually distinct. All comparisons are strict.*

##### If

```
if $variable = true,
	say("this is true");
end;
```

##### If not

```
if not $variable = true,
	say("this is not true");
end;
```

##### Else If

```
else if $variable = "bark",
  say("bark bark!");
end;
```

##### Else

```
else, 
	say("No clue, dude");
end;
```

##### Inline if statement

```
if $ready, say("ready to go!"), else say("not read yet!");

```

There are no ternaries. I personally find them very difficult to read, but I think this inline syntax is pretty compact all things considered.


##### For

```
for $parameter in $list-or-table-name, 
		say("this iteration has returned parameter of list-name");
end;
```

##### While

```
while $number < 10,
	$number <: $number + 1
end;
```

### To-do and Questions:

- array access
- casting solutions etc
- OOP stuff?


# scratch pad

turn map/filter into a first class feature of the language similar to if/else/while/for

```
$filtered-list: filter $item in $original-list,
    $item = "dog"
end;


$mapped-list: map $item in $original-list, 
    transform($item)
end;

```


example of calling a table function and also passing an additional function as a parameter
```
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

```
