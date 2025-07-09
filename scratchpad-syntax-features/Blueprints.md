### Blueprints (custom types)
NOTE: originally the table blueprint and options syntax were meant to mirror the syntax of the list[] and table{} data structure syntax in enzo. But I have consolidated the array-like and map-like behavior into a single data structure of Lists (similar to how Lua does this) and that breaks some of the intended textual stylistic parallelism.
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
        return("Hi, my name is <$self.name> and I'm <$self.age> years old.");
    );
}>;

$alice: Person[
    $name: "Alice",
    $age: 30,
    $t-shirt-size: Size.large
];

say($alice.greet);
// Expected output: "Hi, my name is Alice and I'm 30 years old."
```

---


### Proposed **Mixed Enum/Struct Example**???
(NOTE: I am uncertain about this idea. While it could be syntactically possible to merge options and table blueprints into the same structure, to parallel the merging of Lists and Tables, enums and structs serve fundamentally different purposes in a way that is not true for arrays/maps. The parallel between Lists and enums is that they are both lists of values, and the parallel between Tables and structs is that they are both key-name value pairs, but whereas structs are used as templates for extension, enums are not. I'm pretty weak on my OOP knowledge though so I'm still not clear on how what value any of this stuff brings to Enzo per se)
You can mix indexed and keyed entries if you want:

```enzo
Color: <[
    red,
    green,
    blue,
    hex: Text
]>;

$myColor: Color.hex <: "#00FF00";
$myColor.hex;   // "#00FF00"
$myColor.2;     // "green"
```

---

### **Nested Blueprints**

Blueprints can be nested for more complex structures:

```enzo
Address: <[
    street: Text,
    city: Text
]>;

Person: <[
    name: Text,
    address: Address
]>;

$bob: Person[name: "Bob", address: Address[street: "123 Main", city: "Metropolis"]];
$bob.address.city;   // "Metropolis"
```

---

### **Notes**

- All blueprint types use the same `<[ ... ]>` syntax.
- You can access fields by key (`.name`) or by index (`.1`).
- Methods (functions) can be included as fields.
- Enums are just lists of values, but can also have named fields if desired.

---