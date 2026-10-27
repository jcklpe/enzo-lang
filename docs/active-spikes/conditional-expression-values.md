# Conditional Expression Values
Status: **Deferred — bug captured, implementation not started.** Created 2026-10-06.

[Work index](../../TODO.md) · [To-do and reproduction](conditional-expression-values.todo.md)
## Purpose
Make conditional assignment produce the selected branch’s value consistently. The existing `If … either … or … Otherwise` form already expresses first-match selection; no new SQL-style `CASE` or naming syntax is required merely to support this use case.

The desired expression is:

```enzo
$home-team: If $hometeam-id either is 10189, ("FC Schalke 04"),
    or is 9823, ("FC Bayern Munich"),
    Otherwise, ("Other");
```

The selected branch supplies the value, and `$home-team:` binds its name. Currently only the first branch reliably produces that value; later branches print it and yield an empty result. The to-do document owns the exact evidence and reproduction.
## Scope and constraints
- Investigate conditional value propagation for exclusive `either` branches, `Else if`, and the fallback.
- Preserve existing statement behavior, first-match ordering, lexical scope, and explicit-return behavior.
- Preserve the documented distinction between single-line function atoms with implicit results and multiline function atoms requiring explicit returns. Do not solve the bug by enabling implicit returns for every multiline function.
- Specify what should happen when a branch intentionally has no value, and verify side effects occur once.
- Cover binding, rebinding, and a conditional used in a pipeline where those contexts are supported.
- Do not change non-exclusive multi-branch behavior without separately defining and approving its value contract.
- Do not add table/dataframe types, grouping helpers, or new language syntax as part of this bug fix.
## Design questions for resumption
The parser represents later exclusive branches as nested `IfStatement` nodes. The evaluator wraps branch bodies in function atoms and infers whether they are multiline from statement `code_line` metadata. That interaction is a plausible cause of the lost values, not a completed diagnosis. Determine whether source metadata, branch evaluation, or both need correction before choosing an implementation.

A correct fix should make the compact expression predictable without altering unrelated printing or function-return rules. Keep any durable semantic decision in the language reference after implementation; keep investigation history in the paired to-do document.
## Completion boundary
All selected branches return the expected bound value without unintended output; regression coverage checks earlier branch semantics, scope, explicit returns, and supported expression contexts. Revisit this spike only when Aslan resumes it.
