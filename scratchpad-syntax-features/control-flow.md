## Control flow logic
Control flow logic lets you tell your code what to do next, based on the current state or value of things. It checks conditions (like "Is this list empty?" or "Is the user logged in?") and decides which blocks of code to run.

### True/false conditions
There is no dedicated "boolean" type in Enzo. All values [are interpreted as either true or false](https://www.perplexity.ai/search/what-is-truthy-and-falsy-in-a-dZk5OogGSRmHQLFjGJB4HA) in control flow statements, according to these rules:
Examples of “true” conditions:
```javascript!
$favNumber: 7;
$username: "Alice";
$items:     [1,2,3];
$config:    [ mode:"dark" ];
$log: ( say("hi"); );
$example: Monster; // Almost all variant groups and variant group values will be coerced to "true" values;
$example2: Monster.Goblin;
```

Examples of “false” conditions:
```javascript!
$zero: 0;
$emptyText: "";
$emptyList: [];
$emptyList: [0,0,0];
$emptyTbl:  [];
$emptyTbl2: [key: ;];
$no-operation: ( );
$no-operation2: ( param: ;);
$unset:     ;
$kinda-hacky: False; // Built in variant group explained below.
$hacky2: Status.False; // Built in variant group explained below.
```
The built in blueprint variant groups `True`, `False`, and `Status` (with builtin members `Status.True`, and Status.False`) are provided out of the box. These are provided for the sake of readability, they're not a proper separate "Boolean type" as found in many other languages. They can be extended by the user, such as adding things like `Status.Loading`, `Status.Dead` or what have you. `False` and `Status.False` are the only variant group or variant values which return false in a truth condition context. Kinda hacky? ...True!

Comparisons and functions do not automatically return a boolean type, but functions may return True or False by convention.

### If
`If` by itself just checks for a true condition value.
```javascript!
$fav-color: "blue";

If $fav-color,
	"I have a favorite color and it is: <$fav-color>.";
end;
```

### Else
Else provides a fallback for if the If condition is not met.
```javascript!
If $status is "red alert",
    "Panic!!!";
Else,
	"Nothing to worry about";
end;
```

### not
Add in `not` to test for false condition values instead of true condition values.
```javascript!
$fav-color: "blue";

If not $fav-color,
	"I have no favorite color yet."; // this will not run
end;

"" :> $fav-color;

If not $fav-color,
	"I have no favorite color yet."; // this will now run
end;

```

Pair `If`, `is`, and `not` and you can now create a comparison context that resolves to a true/false condition value and tests for false conditions.
```javascript!
$status: "red alert";

If $status is not "red alert",
	"Everything is probably fine."; // this won't fire
end;
```
### Comparison words
#### is
`is` is a comparison word, where rather than simply testing the variable for true/false condition values, a comparison is made, which then resolves to a true/false condition value.
```javascript!
$fav-color: "blue";

If $fav-color is "blue",
	"fav color is blue";
end;
```
*Assigning value operator (`:`)and comparing values (`is`) are visually and semantically distinct which avoids the overloading common in most other programming languages. All comparisons are strict.*

`is` can be used to compare in several ways:
##### Value match
Most of our examples have been value matches. It's just "does this variable match this value":
```javascript!
If $x is 42,
    "It's the answer!";
end;
```

##### Type match
```javascript!
If $x is Number,
    "It's a number!";
end;

If $x is Empty,
    "Nothing to see here";
end;

If $x is Monster.Goblin,
    "It's a goblin!";
end;
```
### less than
`less than` is a comparison word that checks if a number is less than another number.
```javascript!
$temperature: 98;

If $temperature is less than 50,
    "getting kind of chilly in here";
end;
```

#### greater than
`greater than` is a comparison word that checks if a number is greater than another number.
```javascript!
$temperature: 98;

If $temperature is greater than 88,
    "getting kind of warm in here";
end;
```

#### at most (<=)
`at most` is a comparison word that checks if a number is less than or equal to another number.
```javascript!
$temperature: 98;

If $temperature is at most 120,
    "I can survive this heat";
end;
```

#### at least (>=)
`at least` is a comparison word that checks if a number is greater than or equal to another number.
```javascript!
$temperature: 98;

If $temperature is at least 20,
    "I can survive this coolness";
end;
```

#### contains
`contains` is a comparison word that checks if a list contains a value.
```javascript!
$list-example: [1, 2, 3];

If $list-example contains 3,
    "this list contains a 3.";
end;

$list-example2: [$name: "John", $age: 50];

If $list-example2 contains "John",
    "Hi John!";
end;
```

### Condition combiners
#### and
`and` allows you to test for multiple conditions. Both must resolve to true for the logic to fire.
```javascript!
$status : "red alert";
$temp: 75;

If $status is "red alert" and $temp is 95,
    "It's getting really hot in the engine room!"; // this logic will not fire
end;

$temp <: 95;
If $status is "red alert" and $temperature is 95,
    "It's getting really hot in the engine room!"; // this logic will now fire
end;
```

#### or
`or` allows you to test for multiple conditions, and only one needs to resolve to true for the logic to fire.
```javascript!
$status: "red alert";

If $status is "red alert" or "orange alert",
    "stuff is looking bad!";
end;
```

### Else if
If you want to chain several if statements in a row, but only have the subsequent ones fire if the prior one fails you can use `Else if`.
```javascript!
If $status is "red alert",
    "DANGER!";
Else if $status is "yellow alert",
  "warning!";
Else,
    "Probably not a big deal";
end;
```

### Multi-branch checks (switch statement)
Multi-branch checks let you test one value against several conditions in a row. The first one that meets the conditions will fire.

```javascript!
$colors: ["blue", "green", "yellow"];

if $colors is ["red", "green", "blue"],
    "It matches the specific color set!"; // won't fire
or contains "yellow",
    "There's a yellow in the mix!";  // this will also fire
end;
```

### Inline if statement
```javascript!
If $ready, "ready to go!";, Else "not ready yet!";

```
There are no ternaries. I personally find them very difficult to read, but I think this inline syntax is pretty compact all things considered.

### For
```javascript!
For $param in $list-name,
	"this iteration has returned <$param> of <$list-name>";
end;
```

### While
```javascript!
While $number is less than 10,
	$number <: $number + 1
end;
```
