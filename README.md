# enzo-lang

I'm a UX designer and don't really have a good computer science background, but I find the aesthetics and design of programming syntaxes interesting. Code is the ultimate user interface. This isn't an implementation of a programming language. This is just sort of fantasy sketch of what I think a nice language syntax would look like. Basically as I'm learning programming stuff, I'll make notes on what I don't understand or find confusing, and I make notes on what I think could be different, which provides an outlet and helps me to better understand the real programming language that I'm trying to learn. 

I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment and to help me better understand programming.

Also want to give a shout out to the ["Quorum Language Project"](https://quorumlanguage.com/). 

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

### Variable Type and Assignment
Types are inferred. 

##### text (string) 

```javascript
$text-example: `here is some text`;
```

##### number

```javascript
$number-example: 888;
```

##### list (array) 

```javascript
$list-example: [`here is some text`, 666, $variable-example];
```

##### table (objects/maps) 

```javascript
$table-example: {
	property: `this is a value which is paired to the property`,
	property2: 2,
	property3: [$variable, 3, `three`],
        property4: {
            property: `second layer of a nested table`,
            property2: `tables are basically the same as maps or objects in other languages`}, 
            property3: {
                property: `third layer of a nested table`,
                property2: `you can nest tables as deeply as you want`, 
                property3:`this property value could be invoked using 'table-example.property4.property3'`}
};
```



##### functions

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

### Variable Invocation/Use

Default case:
```javascript
$text-example: `here is some text`;
$text-example;
//returns `here is some text`
```

All variables are call by value
```javascript
$text-example: `here is some text`;
$text-example2: $text-example;
$text-example2;
// returns `here is some text`
```

#### calling a table's property values

Template literals
```javascript
$number-example: 5;
$number-example2: 3;
$text-example: `the result of the two variables added together is ${$number-example + $number-example2}`

$text-example;
//returns the text 'the result of the two variables addded together is 8'
```

#### function invocation

```javascript 
function-example: (
    param first-number: 1;
    param second-number: 1;
    third-number: 1;
    return(first-number + second-number + third-number);
    );

function-example();
//returns 3

function-example(10, 9);
//returns 20

function-example2: (
    first-number: 5;
    param second-number: ;
    param third-number: number: ;
    
    return(first-number * second-number / third-number);
)

// arguments can be assigned to parameters either by order
function-example2(1, 2);
// returns 2.5

// or by named assignment
function-example2(third-number: 2, second-number: 3);
// returns 7.5

function-example2();
// returns error
```

#### passing a function as a parameter

default function as parameter is lazy evaluation 
```javascript
function-example(argument1, function-example2(argumentA, argumentB), argument3);
```


eager evaluation:
```javascript
function-example(argument1, function-example2(argumentA, argumentB), argument3);
```
The `$()` syntax indicates that all functions contained within the brackets will be eager evaluated. This is meant to mirror the syntax of template literals which use `${}`. 

#### invoking a table property function

```javascript

dog: {
    $name: `Ralph`,
    speak: (
        return(`yo, my name is ${$self.name}`);
    );, 
    play-dead: (
        param $assailant: {};
        return(`ah! I was murdered by ${$assailant}!`);
    );, 
};

$dog.name;
//returns `Ralph`

dog.speak;
// returns `yo, my name is Ralph`

dog.play-dead(`Tom`);
//returns `ah! I was murdered by Tom!`

//piping the return value into a function
toLowerCase(dog.name);
//returns `ralph`

toLowerCase(dog.play-dead(`Jerry`));
// returns `ah! i was murdered by jerry!`



```

#### Control Flow Statements

 *`:` is used for assigning values, while `=` is used for comparing values. Having the two be different makes the two more visually distinct. All comparisons are strict.*

##### If

```
if $variable = true: do
	return(6 + 9 + 8);
end;
```

##### If not

```
if not $variable = true: do
	return(6 + 9 + 8);
end;
```

##### Else If

``` 
else if $variable = `bark`: do
  return(`the dog said bark`);
end;
```

##### Else

```
else : do
	return(null);
end;
```

##### Inline if statement

```
if $ready: return( 12 + 2 ), else return( 5 + 8 );

```

There are no ternaries. I hate 'em!




##### While

```
while $variable-jim = `sick`: do
	return(`jim is sick`);
end;
```



##### For 

```
for $parameter:
	in $list-or-table-name: do
		return(`this iteration has returned parameter of list-name`
    end;
end;
```

### increment a variable
```
++(5);
````

## Notes
- I like how R has a left and right assignment using -> and <- which I think works well visually and has  flexibility that the name: value idea doesn't have. but not sure if I want to move to that instead since I think the : looks nice and clean and is also has better keyboard ergonomics, and I don't really know any reason to have that reversible assignment operator.


### To-do and Questions:

- array access
- dot notation versus alternatives
- explore replacing `for`, `while`, `switch` with some kind of reducible `if` structure 
- static versus dynamic types, casting solutions etc
- variables inside template literals looks clunky: \${$variable-name} Maybe need to investigate more deeply why template literals exist and if there is a more general approach. 
- Is "self" really needed? I have heard the argument for explicitness on that and I generally prefer explicitness but seems like that should just be contextual. I don't know enough OOP stuff yet. 
- OOP stuff?
- Should the table use "\$" when it's used to call a method, even though functions are not normally prefixed with "$"? $ on functions feels like overkill but I do like the explicit visual cue for what is a variable in PHP, and I'm trying to treat functions as basically just another thing assigned to a variable. 