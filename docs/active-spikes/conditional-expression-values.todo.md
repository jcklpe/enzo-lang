# Conditional Expression Values — To Do
Status: **Deferred.** Documentation and reproduction are complete; no parser or evaluator changes have been made.

[Concept](conditional-expression-values.md) · [Work index](../../TODO.md)
## Evidence as of 2026-10-06
Reproduced on branch `classic-algos`, HEAD `e8dc567e45fca41716fd84e0ef75a85d8038443f`, using the local working tree. Existing unrelated edits were present in `.gitignore`, `README-lazy.md`, and syntax scratch files; they were left untouched. The tested parser and evaluator had no reported working-tree edits.

For this minimal source, change the input ID to exercise each branch:

```enzo
$hometeam-id: 9823;
$home-team: If $hometeam-id either is 10189, ("FC Schalke 04"),
    or is 9823, ("FC Bayern Munich"),
    Otherwise, ("Other");
$home-team;
```

| Input | Expected value | Actual evaluator result | Captured stdout |
|---|---|---|---|
| `10189` | `FC Schalke 04` | `FC Schalke 04` | Empty |
| `9823` | `FC Bayern Munich` | Python `None` | `"FC Bayern Munich"` plus newline |
| `123` | `Other` | Python `None` | `"Other"` plus newline |

The equivalent `If … Else if … Else` expression produced the same three outcomes. Returning Python `None` is the observed host result, not a proposed new Enzo value type.
## Reproduction environment
Use the interpreter’s existing `.venv/bin/python` with `interpreter/` on `sys.path`; a generic system Python lacked `colorama` when a printing path imported `src.cli`. Set `PYTHONDONTWRITEBYTECODE=1`. In the in-memory harness, replace `src.runtime_helpers.clear_debug_log` with a no-op before importing/evaluating, so the CLI formatting import does not truncate `interpreter/debugging/debug.log`. This suppresses diagnostic-file setup only; do not patch parsing, evaluation, or output formatting. Reset `_env`, call `_initialize_builtin_variants()`, run `eval_ast(parse(source))`, and capture stdout independently of the returned value.

The harness caught the missing values only after the correct dependency environment was used; neither filesystem nor missing-package errors are the conditional bug.
## Verified workaround
A named function with explicit `return(...)` in every branch returned the correct value for all three IDs, and `$home-team: home-team-name(9823);` bound `FC Bayern Munich` correctly:

```enzo
home-team-name: (
    param $hometeam-id: ;
    If $hometeam-id either is 10189, (return("FC Schalke 04")),
        or is 9823, (return("FC Bayern Munich")),
        Otherwise, (return("Other"));
);
$home-team: home-team-name(9823);
```
## Investigation starting points
- `interpreter/src/enzo_parser/parser.py`: `_parse_multi_branch_if`, `_parse_multi_branch_if_continuation`, regular conditional parsing, and source-line metadata for generated nested `IfStatement` nodes.
- `interpreter/src/evaluator.py`: `IfStatement` handling, branch `EnzoFunction` construction, and `invoke_function` printing/return behavior.
- `interpreter/tests/test-modules/conditional-assignment.enzo` and `conditional-flow.enzo`, plus their golden files. Existing tests demonstrate the two capabilities separately; do not infer their combination is covered.
## To Do — on explicit resumption
- [ ] Add a regression that checks both the returned/bound value and captured stdout for first, later, and fallback branches in `either` and `Else if` chains.
- [ ] Trace the nested-branch evaluation and confirm the root cause before changing semantics.
- [ ] Implement the smallest correction preserving single-line/multiline function rules and existing statement behavior.
- [ ] Cover scope isolation, rebinding/type consistency, supported pipeline use, exactly-once evaluation, and intentional empty-valued branches.
- [ ] Run relevant conditional, function, and pipeline tests; broaden only if the change crosses those boundaries.
- [ ] Document any settled semantic change and update this spike’s status when the fix is verified.
## Done
- [x] Capture the bug for later engagement in a concept/to-do pair and index it without activating implementation.
- [x] Verify all three input outcomes for both exclusive conditional forms, plus the explicit-return workaround.
