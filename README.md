# enzo-lang

I have no real good understanding of computer science, but I'm still interested in the aesthetics and design of programming syntax. This isn't an implementation of a programming language. This is just sort of fantasy sketch of what I think a nice language syntax would be like. 



I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment. 



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

##### text (string) 

```javascript
text text-example: {`here is some text`};
```

##### number

```javascript
number number-example: {888};
```

##### list (array) 

```javascript
list list-example: { `here is some text`, 666, this-is-a-variable};
```

##### table (objects/maps) 

```javascript
table table-example: {example-key: {example-value}};
```

```javascript
table table-example2: {
	key: {value},
	key2: {value2},
	key3: {value3}
};
```

```javascript
table table-example3: {
    key: text {`here is some example text`},
    key2: number {44}
	key3: list { 55, 66, variable-example },
	key2: table {
		key: {value},
		key2: table {
			key: {value},
			key2: {value2}
		}
	}
};
```

```javascript
table table-example3: {
	key: {
            key: {value},
            key2: {value2},
            key3: {value3}
	}, 
	key2: {
		key: {value},
		key2: {
			key: {value},
			key2: {value2}
		}
	}
};
```

##### functions

``` javascript
function function-name: {
    
    // Argument variables are declared inside the function definition. Param keyword distinguishes argument variables from normal function scoped variables. argument variables can be assigned an initial value that it defaults unless otherwise specified when the function is called. 
    number param argumemt-var1: {};
    number param argument-var2: {12};
    number example-variable: {666};
    
    return[parameter1 + parameter2 + example-variable];
};
```

*side note: I like how R has a left and right assignment using -> and <- which I think works well visually and has  flexibility that the name: value idea doesn't have. but not sure if I want to move to that instead since I think the : looks nice and clean and is also has better keyboard ergonomics.* 

### Variable Invocation/Use

Default case:
```javascript
text text-example: {`here is some text`};
text-example;
//returns `here is some text`
```

All variables are call by value
```javascript
text text-example: {`here is some text`};
text text-example2: {text-example};
text-example2;
// returns `here is some text`
```

Template literals
```javascript
number number-example: {5};
number number-example2: {3};
text text-example: {`the result of the two variables added together is ${number-example + number-example2}`}
```

#### function invocation
*parantheses are reserved for conditional statements, while square brackets are reserved for function arguments*

```javascript 
function-example[argument1, argument2];
```

#### passing a function as a parameter

default function as parameter is lazy evaluation 
```javascript
function-example[argument1, function-example2[argumentA, argumentB], argument3]
```


eager evaluation:
```javascript
function-example$[argument1, function-example2[argumentA, argumentB], argument3]
```

The `$[]` syntax indicates that all functions contained within the brackets will be eager evaluated. This is meant to mirror the syntax of template literals which use `${}`. 

#### Control Flow Statements

 *`:` is used for setting values, while `=` is used for comparing values. Having the two be different reduces the confusion over assignment versus comparison. All comparisons are strict and there's no `==` versus `===` nonsense.*

##### If

```
if(variable = true) {
	return[ 6 + 9 + 8];
}
```

##### If not

```
if( not variable = true) {
	return[ 6 + 9 + 8];
}
```

##### Else If

``` 
else if( variable = `bark`) {
  return[`the dog said bark`];
};
```

##### Else

```
else {
	return[null];
};
```

##### Inline if statement

```
if(ready) return[ 12 + 2 ], else return[ 5 + 8 ];
```






##### While

```
while(variable-jim = sick) {
	return[`jim is sick`];
};
```



##### For 

```
for[parameter] {
	in[list-or-table-name]: {
		return[`this iteration has returned parameter of array-name`];
	};
};
```


### Template Strings

```
return[`this is a template string where ${variable} is escaped and dynamic. You can also ${nest the ${template-strings} if you want}`];
```

### increment a variable

number ++;

## Notes

### TODO:

- array access
- dot notation versus alternatives
- better consistency in the control statement uses of different kinds of brackets
- explore replacing `for`, `while`, `switch` with some kind of reducible `if` structure 