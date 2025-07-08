### Blueprints (custom types)

##### Options Blueprint (enum)

```javascript!
Size: <[small, medium, large]>;

$shirt-size: Size.medium;
```

#### List Blueprint (class/interface/struct)
```javascript!
Person: <[
    name: Text,
    age: Number,
    t-shirt-size: Size,
    greet: (
        return("Hi, my name is <$self.name> and I'm <$self.age> years old.");
    );
]>;

$alice: Person[
    $name: "Alice",
    $age: 30,
    $t-shirt-size: Size.large
];

say($alice.greet);
// Expected output: "Hi, my name is Alice and I'm 30 years old."
```

---

### **Mixed Enum/Struct Example**

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