# enzo-lang
I have no real good understanding of computer science, but I'm still interested in the aesthetics and design of programming syntax. This isn't an implementation of a programming language. This is just sort of fantasy sketch of what I think a nice language syntax. 



I'm def interested in feedback but also understand that this is basically just a kid drawing pictures of racecars and wishing he was Batman. I'm doing this for my own enjoyment. 



## Syntax Outline

### Comments

```javascript
// single line comment
```

``` 
/. block comment./
```



### Variable Expressions

##### variable constant

```
const var variable-name = [value];
```

##### variable let

```
var variable-name = [value];
```

#### variable types

###### strings

```
const var string-example = [`string`];
```

###### number

```
const var number-example = [666];
```

###### array

```
var array-example = [ `string`, 666, referenced-variable-example, function-example, object-example];
```

###### objects

```
const var object-example = [object-key = object-value];
```

```
var object-example2 = [
	object-key = object-value,
	object-key2 = object-value2,
	object-key3 = object-value3
];
```

```
const var object-example3 = [
	object-key-object = [
		object-key-second-layer = object-value-second-layer
		], 
	object-key-object2 = [
		object-key2-second-layer = object-value2-second-layer,
		object-key3-second-layer = [
			object-key3-third-layer = object-value3-third-layer,
			object-key4-fourth-layer = object-key4-third-layer
		]
	]
];
```

###### function declaration

```
const var function-example = function[parameter1, parameter2]{
	var number-example2 = [666];
	return[parameter1 + parameter2 + number-example2];
}
```

###### function invocation

function-example[argument1, argument2];

#### Control Flow Statements

##### Inline if statement

```
if(ready) return[ 12 + 2 ];
```

##### ternary statement

```
if(varible == true) return[result] else return[result]
```





##### If

```
if(variable == true){
	return[ 6 + 9 + 8];
}
```

##### Else If

``` 
else if( variable == `bark`){
  return[`the dog said bark`];
}
```

##### Else

```
else{
	return[null];
}
```

##### Switch

```
switch[parameter]{

    case(number == 1){
    	return[`the number equals 1`];
    	}
    	
    case(number == 666){
    	return[`the number equals 666`];
    	}
    	
    case(default){
    	return[`the number doesn't match anything so it returns this default`];
    	}
}
```

##### While

```
while(variable-jim==sick){
	return[`jim is sick`];
}
```

##### For While

```
for[initial-condition=0]{
	while(initial-condition<100){
		initial-condition = intitial-condition + 1;
		return[`initial-condition is now <<intial-condition>>`]
	}
}
```

##### For in

```
for[parameter] {
	in[collection-or-array-name]{
		return[`this iteration has returned <<parameter>> of array-name`];
	}
}
```





# Thoughts

- perhaps switch the variable assignment and object key to : instead of = and then = can be used purely as a conditional operator without dealing with == or ===. Would also make the assignment of variable more consistent with the object like syntax
- perhaps change for to if 
- () are used for both parameters and conditions. Should separate those out more. 
- //is for comment titles versus // for actual comments