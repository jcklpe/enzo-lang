# Enzo Language Spec Alignment Roadmap

## 1. Parentheses as Function Atoms (Block Expressions)
- [ ] Remove all "grouping parens" handling: parens always mean a block/function atom.
- [ ] Ensure math expressions like `(($x + $y) * $z);` are written as function atoms and parsed as such.
- [ ] Update grammar, parser, and evaluator to reflect this.
- [ ] Update/add relevant tests to enforce this pattern.

### Testing Language Atom Rules
- [ ] Add a test: bare expression `$x + $y;` (no parens) **should fail with syntax error**
- [ ] Add tests: all five atom types allowed outside parens succeed
    - [ ] Number atom: `100;`
    - [ ] Text atom: `"hi there";`
    - [ ] List atom: `[1, 2, 3];`
    - [ ] Table atom: `{ $x: 1 };`
    - [ ] Function atom: `(return(3));` (should work)
- [ ] Add a test: block expr inside parens works as intended (e.g. `($x: 1; $x + 2);` returns 3)
- [ ] Add a test: string interpolation only accepts paren-wrapped expressions (`"<($x + $y)>"`)
- [ ] Add a test: string interpolation with bare `$x + $y` **fails**
- [ ] Add tests: function reference syntax with `@function-name` works, and `$function-name` always returns the value, never the reference

## 2. Function Reference Syntax (`@funcname`)
- [ ] Add grammar support for `@funcname` (function reference, not invocation).
- [ ] Parse `@funcname` to an AST node (e.g., `("func_ref", "funcname")`).
- [ ] Evaluator: resolve to the actual function atom (not its value).
- [ ] Update/add tests for higher-order functions and function references.

## 3. Keyname Binding of Function Atoms (Lazy Evaluation)
- [ ] Ensure assigning a function atom to a keyname does not immediately evaluate; only evaluate on invocation.
- [ ] Make sure `$x: (5 + 5); $x;` works as "deferred" computation.
- [ ] Update/add tests for reactivity and rebinding.

## 4. Top-Level Invocation/Statement Atoms
- [ ] Make sure bare number, string, list, table, and function_atom atoms at the top level evaluate/return themselves (or evaluate function_atom).
- [ ] Audit parser to ensure only atoms can be top-level statements.
- [ ] Audit parser to error on bare expressions at top level (except inside block).
- [ ] Update/add tests for statement-style evaluation.
- [ ] Update error messages to be clear for the new atom/expr rules.

## 5. Scoping & Parameter Passing for Blocks
- [ ] Test block scoping: variable inside block is not available outside.
- [ ] Test parameter passing: block-expr parameters override outer values.
- [ ] Test that parameter default values are respected.
- [ ] Test function call and reference distinctions, e.g. block-as-data vs invocation.

## 6. Tests and Documentation
- [ ] Update golden tests to use the new parens/function atom approach.
- [ ] Add coverage for all edge cases (invocation, assignment, reference, interpolation).
- [ ] Update README examples to show all math/logic expressions in parens.
- [ ] Add “what is an atom?” explainer in the README for clarity.
- [ ] Clarify function reference rules with `@` and show usage examples.
