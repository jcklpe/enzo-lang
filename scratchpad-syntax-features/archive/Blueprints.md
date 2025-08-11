# potential future features for blueprints
### **Constructors**

Functions that execute automatically upon instantiation.

**Example syntax:**

```
Goblin: <[
  health: Number,
  position: [Number, Number],
  constructor: (
    say("Goblin spawned at <$self.position> with health <$self.health>");
  )
]>;

$newGoblin: Goblin[health:50, position:[0,0]];
// automatically says: "Goblin spawned at [0, 0] with health 50"
```

**Benefit:**

- Perform automatic initialization logic on object creation.


### **Static Properties & Methods**

Properties or methods associated with the Blueprint itself, not individual instances.

**Example:**

```
Goblin: <[
  health: Number,
  position: [Number, Number],
  static count: 0, // shared across all Goblin instances
  constructor: (
    Goblin.count + 1 :> Goblin.count;
  ),
  static getCount: (
    return(Goblin.count);
  )
]>;

Goblin.getCount(); // returns number of Goblins created
```

**Benefit:**

- Shared global state or utility methods.