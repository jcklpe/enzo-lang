# enzo-lang
I have no real good understanding of computer science, but I'm still interested in the aesthetics and design of programming syntax. This isn't an implementation of a programming language. This is just sort of fantasy sketch of what I think a nice language syntax. 



I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment. 



## Syntax Reference

### Comments

```javascript
// single line comment
```

```
//- Comment Title (styled different in editor and can be used for auto documentation purposes)
```

``` 
/' block comment, the use of single quote has better keyboard ergonomics than the star symbol typically used '/
```



### Variable Type and Assignment

##### strings

```
string string-example: {`string`};
```

##### number

```
number number-example: {number};
```

##### array

```
array array-example: {`string`, 666, referenced-variable-example, function-example, object-example};
```

##### objects

```
object object-example: {object-key: {object-value}};
```

```
object object-example2: {
	object-key: {object-value},
	object-key2: {object-value2},
	object-key3: {object-value3}
};
```

```
object object-example3: {
	object-key-object: {
		object-key-second-layer: {object-value-second-layer}
		}, 
	object-key-object2: {
		object-key2-second-layer: {object-value2-second-layer},
		object-key3-second-layer: {
			object-key3-third-layer: {object-value3-third-layer},
			object-key4-fourth-layer: {object-key4-third-layer}
		}
	}
};
```

##### functions

*functions are conceptually just another variable type*

```
function function-name[parameter1, parameter2]: {
	number number-example: {666};
	return[parameter1 + parameter2 + number-example2];
};
```

*side note: I like how R has a left and right assignment using -> and <- which I think works well visually and has  flexibility that the name: value idea doesn't have. but not sure if I want to move to that instead since I think the : looks nice and clean.* 

### Variable Invocation/Use

*a variable is assigned a value which is contained within {a single set of brackets} and it is invoked using {{two sets of brackets}}*

```
string string-example: {`string`};

string string-example2: {`{{string-example}}`};

if ({{string-example}}=false) {
 return[{{string-example}}]
}
```

*note that `return[return-value]` is a built in function, sorta like print, and the return value being returned is treated as an argument for the return function's parameter.* 

##### function invocation

*functions while being treated largely as variables aren't given {{}}. Though maybe this is an inconsistency. I think it looks bad to put {{}} around function invocations. But it is inconsistent. 😕 Not sure what to do here.*

```
function-example[argument1, argument2];
```

#### Control Flow Statements

 *`:` is used for setting values, while `=` is used for comparing values. Having the two be different reduces the confusion over assignment versus comparison. All comparisons are strict and there's no `==` versus `===` nonsense.*

##### If

```
if(variable = true): {
	return[ 6 + 9 + 8];
}
```

##### Else If

``` 
else if( variable = `bark`): {
  return[`the dog said bark`];
};
```

##### Else

```
else{
	return[null];
};
```

##### Inline if statement

```
if(ready): return[ 12 + 2 ], else return[ 5 + 8 ];
```

##### ternary statement

```
var variable-name: return[7] if(condition = true) else return[20]; 
```

##### Switch

switch is treated like a function that takes an argument to it's parameter which is then passed to the conditional statements that make up the difference cases

```
switch[parameter]: {

    case(number = 1): {
    	return[`the number equals 1`];
    	};
    	
    case(number = 666): {
    	return[`the number equals 666`];
    	};
    	
    case(default): {
    	return[`the number doesn't match anything so it returns this default`];
    	};
};
```

multiple parameters in a switch statement

```
switch[parameter1, parameter2]: {

    case(parameter1 = 1): {
    	return[`the number equals 1`];
    	};
    	
    case(parameter2 = 666): {
    	return[`the number equals 666`];
    	};
    	
    case(parameter2 = 777 and parameter1 = 18): {
    	return[`the numbers are blah blah whatever you get the idea`]
        };
    	
    case(default): {
    	return[`the number doesn't match anything so it returns this default`];
    	};
};
```



##### While

```
while(variable-jim = sick): {
	return[`jim is sick`];
};
```



The following are very early drafts. I actually need to learn a bit more on what the differences are between for while, for in, while, etc really means in various programming languages. 

##### For While

```
for(initial-condition = 0): {
	while(initial-condition < 100){
		initial-condition = intitial-condition + 1;
		return[`initial-condition is now <<intial-condition>>`];
	};
};
```

##### For in

```
for[parameter]: {
	in[collection-or-array-name]: {
		return[`this iteration has returned <<parameter>> of array-name`];
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
- also not totally sure about the for, while, for while, for in, for of etc possibilities. Need to learn more about that. 
- Could be possible to replace "if" with "for"? Conceptually "for while" is basically "if while"