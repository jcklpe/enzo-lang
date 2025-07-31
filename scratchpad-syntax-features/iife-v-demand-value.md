### **Issue: How do function atoms behave when passed as arguments to other functions in Enzo?**

#### **Key Points:**

- **Function atoms (parentheses blocks) in Enzo** auto-invoke (“demand-driven”) **only when placed in a context where their value is immediately needed**—such as:
  - Top-level expressions
  - Assignment (right-hand side)
  - Return statements
  - String interpolation
  - Pipelines (with `$this`)
- **When a function atom is passed as an argument to another function (e.g., `map($nums, (param $x: ; $x + 1))`):**
  - It is **not** auto-invoked.
  - It is passed *as a function object* (a value representing the function, not its result).
  - It will only be invoked **if and when the receiving function (like `map`) explicitly calls it** (e.g., inside a loop: `$fn($item)`).
- **There is no IIFE (immediately-invoked function expression) behavior** when passing a function atom as a parameter—Enzo does not auto-invoke the function atom just because it is used as a function argument.

#### **Summary Table**

| Context                  | Function Atom Auto-Invokes? | Example Syntax                  |
| ------------------------ | --------------------------- | ------------------------------- |
| Top-level                | ✔️                           | `($x: 2; $x + 1);`              |
| Pipeline (`then`)        | ✔️                           | `5 then ($this + 1);`           |
| Assignment, return, etc. | ✔️                           | `$a: ($x: 2; $x + 1);`          |
| Passed as argument       | ❌                           | `map($nums, (param $x: ; ...))` |



**In short:**

> Passing a function atom as an argument to another function in Enzo **does not trigger auto-invocation or IIFE behavior**. It only gets called if the receiving function explicitly invokes it.

------

Let me know if you want a visual, code walkthrough, or further clarification!