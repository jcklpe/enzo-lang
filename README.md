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
    
    // Arguments declared inside the function definition, similar to normal variables. Param keyword distinguishes it from normal function scoped variables
    number param argumemt-var1: {};
    number param argument-var2: {};
    number example-variable: {666};
    
    return[parameter1 + parameter2 + example-variable];
};
```

*side note: I like how R has a left and right assignment using -> and <- which I think works well visually and has  flexibility that the name: value idea doesn't have. but not sure if I want to move to that instead since I think the : looks nice and clean and is also has better keyboard ergonomics.* 

### Variable Invocation/Use


```javascript
text text-example: {`here is some text`};

text text-example2: {text-example};
```

##### function invocation
*parantheses are reserved for conditional statements, while square brackets are reserved for arguments for functions*

```javascript 
function-example[argument1, argument2];
```

#### Control Flow Statements

 *`:` is used for setting values, while `=` is used for comparing values. Having the two be different reduces the confusion over assignment versus comparison. All comparisons are strict and there's no `==` versus `===` nonsense.*

##### If

```
if(variable = true) {
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

##### Switch

switch statement syntax is meant to visually echo the syntax of a function.

```
switch[parameter] {

    case(number = 1) {
    	return[`the number equals 1`];
    	};
    	
    case(number = 666) {
    	return[`the number equals 666`];
    	};
    	
    case(default) {
    	return[`the number doesn't match anything so it returns this default`];
    	};
};
```

multiple parameters in a switch statement

```
switch[parameter1, parameter2] {

    case(parameter1 = 1) {
    	return[`the number equals 1`];
    	};
    	
    case(parameter2 = 666) {
    	return[`the number equals 666`];
    	};
    	
    case(parameter2 = 777 and parameter1 = 18) {
    	return[`the numbers are blah blah whatever you get the idea`]
        };
    	
    case(default) {
    	return[`the number doesn't match anything so it returns this default`];
    	};
};
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

## Notes

### TODO:

- array access
- dot notation versus alternatives
- better consistency in the control statement uses of different kinds of brackets
- explore replacing `for`, `while`, `switch` with some kind of reducible `if` structure 