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