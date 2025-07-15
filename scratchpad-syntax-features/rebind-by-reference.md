<<<Note: not sure if this idea is totally stupid or not but it occurred to me so I'm taking down the notes on it.>>>

value :> $var — assign value to variable (by value/copy)

value :@> $var — assign value to variable's origin (by reference, if $var is a reference)

 **Should the distinction between copy/reference happen at destructure, or at rebind/mutation?**


------

## **1. Reference vs. Copy: Where Should the Distinction Live?**

### **A. Reference/copy at destructure**

- **Current model:**
  - `$person[] :> $name, $age` → copy of values
  - `@person[] :> $name, $age` → references to *slots* in `$person`
- **Upside:**
  - Predictable, mirrors your function argument model (`$foo` vs `@foo`)
  - User must be explicit up front: “I want copies” or “I want links.”
- **Downside:**
  - Once you destructure, you’re stuck with that relationship.
  - You can’t later “upgrade” a copy to a reference, or vice versa.

### **B. Reference/copy at rebind/mutation**

- **Idea:**
  - Always destructure as copies (safe default), but when rebinding a variable, allow a choice:
    - Rebinding only affects the *copy* (normal case)
    - Rebinding *also* affects the source/original (“up the chain”)
- **How?**
  - Could have a special rebinding operator, e.g.,
    - `:>` for normal (copy),
    - `<@:` for “update original/reference”
- **Upside:**
  - Flexible: destructure safely, but selectively mutate upstream when needed.
- **Downside:**
  - Adds complexity (“spooky action at a distance”)
  - Could be confusing—less clear dataflow; mutation logic is split from declaration.

------

## **2. What’s the \*Real\* Use Case for Reference Rebinding?**

- **Typical need:** You want to extract fields from a record/list, *work with them independently*, but occasionally push changes “back up” into the original structure.
- **But in practice:** Most languages make you choose up front.
  - Python: always copy
  - JS: always copy unless you’re destructuring objects and those objects are themselves mutable references
  - Rust: explicit borrow/reference

**Very few languages allow “upgrade from copy to reference” later—because it breaks reasoning about mutability and scope.**

------

## **3. Possible Syntaxes (For Reference)**

- **Destructure as reference:**

  ```
  @person[] :> $name, $age;
  ```

- **Destructure as copy:**

  ```
  $person[] :> $name, $age;
  ```

- **Rebinding a reference:** (Current design)

  ```
  "Tim" :> $name; // if $name is a reference, updates $person.name
  ```

- **Upgrading copy to reference later:** (More complex, not recommended unless you see a killer use case)

  ```
  $name :> @person.name; // re-link $name as a reference to $person.name
  ```

  or (even more complex)

  ```
  "Tim" <@ $name; // special “upstream rebind” operator
  ```
