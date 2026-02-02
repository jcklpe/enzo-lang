- add syntax highlighting to CLI REPL
- implement classic algos
- blueprint extension with inheritance
    - polymorphism
- builtin functions
- casting solutions?
- implement partial application
- named rebinding for function arguments
- forbid concatenation of text, create error test cases
- Loop from 1 to 10, ($i; ...);
- ability to loop over just keys or just unnamed indexes
- `maybe` pipeline operator or try/catch stuff
- block quotes
- multiline text
- write tests and define behavior for pipelines that have no return value (either multiline functions or named functions with no return). Cases such as a function atom with no return value passing via pipeline to another atom that expects a value. Define boundaries on $this etc
- integration tests between pipeline functions and $this used in a conditional flow logic:
    ```
    5 then (
        If $this less than 10, print("less than five");
        return($this);
    ), then print("value is: <$this>");
    ```
- write pipeline tests for stuff like:
    $result: 5 then ($this + 1) then $this // most of the time pipelines terminate in :> but should support the keyname up front too
- add tests for $this.1 and $this.2 for functions that return a list of values.
- text escape characters
- Blueprints that have type but no default set, and then you create an instance without specifying the value. Should be an error.
- instancing a blueprint with the wrong type for a field.
- arithmetic operations that mix types (like `"5" + 5`). Should error
- divide by zero errors
- floating point math
- destructuring blueprint instances (instances are like lists but we haven't actually shown any destructuring of a blueprint instance)
- is odd/even conditional?
- squaring operators?
- inverse exponent?
- generics?