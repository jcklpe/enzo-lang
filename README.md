# enzo-lang
I have no real good understanding of computer science, but I'm still interested in the aesthetics and design of programming syntax. This isn't an implementation of a programming language. This is just sort of fantasy sketch of what I think a nice language syntax. 



I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment. 



## Syntax Reference

### Comments

```javascript
// single line comment
```

```
//-Comment Title (styled different in editor and can be used for auto documentation purposes)
```

``` 
/' block comment, the use of single quote has better keyboard ergonomics than the star symbol typically used '/
```



### Variable Expressions

##### variable assignment

```
const variable-name: {value};
```

*side note: I like how R has a left and right assignment using -> and <- which I think works well visually and has flexibility that the name: value idea doesn't have.*  

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

##### variable invocation

```
string string-example: {`string`};

if ({{string-example}}) {
 return {{string-example}}
}
```



##### function declaration

// functions are basically just another variable type

```
function function-name[parameter1, parameter2]: {
	number number-example: {666};
	return[parameter1 + parameter2 + number-example2];
};
```

##### function invocation

```
function-example[argument1, argument2];
```


#### Control Flow Statements

##### Inline if statement

```
if(ready): return[ 12 + 2 ], else return[ 5 + 8 ];
```

##### ternary statement

```
var variable-name: return[7] if(condition = true) else return[20];
// note `:` is used for setting values, while `=` is used for comparing values. All comparisons are strict. So in this case `variable-name` is being set to the value of `7` if the condition is true and 20 if false. 
```

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

##### Switch

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

##### While

```
while(variable-jim = sick): {
	return[`jim is sick`];
};
```

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

##### Template Strings

```
return[`this is a template string where ${variable} is escaped and dynamic. You can also ${nest the ${template-strings} if you want}`];
```

## Notes

### TODO:

- array access
- dot notation versus alternatives
- better consistency in the control statement uses of different kinds of brackets