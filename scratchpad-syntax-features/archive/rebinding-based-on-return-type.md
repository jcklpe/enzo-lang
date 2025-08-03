## Enzo: Rebinding Block Bindings Based on Return Type

### Feature Idea

Allow variables bound to block expressions (functions) to be *rebound* to a value of the *type returned by the block*, treating a function returning a value as compatible with a value of that type for rebinding purposes.

---

#### Example

```enzo
$z: (3 + 4);      // $z is a block, returns 7 (type: () → Number)
$z;               // evaluates to 7
$z <: 8;          // valid: rebinding a block returning Number to a Number
$z <: "oops";     // error: can't rebind Number to String
```
### Motivation

- **Flexibility:** Enables code to abstract between computations and their results, making it easy to replace a computed value with a constant or vice versa.
- **Consistency:** Makes function-to-value and value-to-function transitions seamless when the value types match.

------

### Possible Issues

- **Complexity:** Increases the cognitive load and type system complexity, as the language must reason about return types of blocks at bind time.
- **Edge Cases:** Harder to debug mismatches between function shape/signature and value type, especially if functions take parameters.
- **Performance:** May obscure when evaluation happens and what is actually stored (function or value).

------

### Status

Not implemented; currently, Enzo only allows rebinding blocks to other blocks (same signature) and values to other values of the same type.
 Feature idea tabled for future exploration.