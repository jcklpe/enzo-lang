### Control Flow Statements
*Assigning value operator (`:`)and comparing values (`is`) are visually and semantically distinct which avoids the overloading common in most other programming languages. All comparisons are strict.*

#### Boolean Context
When any expression appears in a conditional position (`if`, `while`, etc.), it is **coerced** as follows:

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
$zero:      0;
$emptyText: "";
$emptyList: [];
$emptyList: [0,0,0];
$emptyTbl:  [];
$emptyTbl2:  [key: ;];
$no-operation: ( );
$no-operation2: ( param: ;);
$unset:     ;
$kinda-hacky: False; // built in variant group explained below.
$hacky2: Status.False; // Built in variant group explained below. Kind of hacky. It's the only variant group value that will return false in a boolean context.
```

The built in blueprint variant groups `True`, `False`, and `Status` (with builtin members `Status.True`, and Status.False`) are provided out of the box. These are provided for the sake of readability, they're not a proper separate "Boolean type" as found in many other languages. They can be extended by the user, such as adding things like `Status.Loading`, `Status.Dead` or what have you. `False` and `Status.False` are the only variant group or variant values which return false in a boolean context. Kinda hacky? ...True!

##### If
```javascript!
$fav-color: "blue";

if $fav-color is "blue",
	"fav color is blue";
end;
```

##### If not
```javascript!
$status: ;

if not $status,
	"no current status";
end;
```

This just checks for a boolean context value.

##### If is not
```javascript!
$status: "red alert";

if $status is not "red alert",
	"Everything is probably fine.";
end;
```

##### If and
```javascript!
$status : "red alert";
$temperature: 600;

if $status is "red alert" and $temperature is 50,
    "It's getting really hot in the engine room!";
end;
```

##### If or
```javascript!
$status: "red alert";

if $status is "red alert" or "orange alert",
    "stuff is looking bad!";
end;
```

##### If less than
```javascript!
$temperature: 98;

if $temperature is less than 50,
    "getting kind of chilly in here";
end;
```

##### If greater than
```javascript!
$temperature: 98;

if $temperature is greater than 88,
    "getting kind of warm in here";
end;
```

##### If at most (<=)
```javascript!
$temperature: 98;

if $temperature is at most 120,
    "I can survive this heat";
end;
```

##### If at least (>=)
```javascript!
$temperature: 98;

if $temperature is at least 20,
    "I can survive this coolness";
end;
```

##### Else If
```javascript!
else if $variable is "yellow alert",
  "warning!";
end;
```

##### Else
```javascript!
else,
	"Nothing to worry about";
end;
```

##### Inline if statement
```javascript!
if $ready, "ready to go!";, else "not read yet!";

```
There are no ternaries. I personally find them very difficult to read, but I think this inline syntax is pretty compact all things considered.

##### For
```javascript!
for $parameter in $list-or-list-name,
		say("this iteration has returned <$parameter> of <$list-name>");
end;
```

##### While
```javascript!
while $number less than 10,
	$number <: $number + 1
end;
```
