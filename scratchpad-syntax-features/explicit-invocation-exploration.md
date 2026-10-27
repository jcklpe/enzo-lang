# Tabled: a truly consistent explicit-invocation syntax (Tcl-inspired)

*Parked exploration, July 2026. Not a commitment — a place to return to someday. Context: the branch formerly called "lazy syntax" (see `lazy-syntax.md`) was abandoned Aug 2025. This doc records (1) the accurate name for what that branch actually was, (2) the inconsistency found in it later, and (3) a sketch of a possible third approach that might fix both its noise problem and its inconsistency.*

## Naming correction

The abandoned branch was never lazy evaluation in any technical sense (no thunks, no call-by-need). What it actually was: **explicit-invocation syntax** — storage and invocation each marked with a sigil (`@` stores, `$` invokes) at every use site, replacing demand-driven context rules. Call it "the explicit branch" going forward.

## The inconsistency discovered post-mortem

The explicit branch wasn't even fully explicit. At named uses, yes: every keyname carries `@` or `$`, no default, symmetric. But at one position class — an *anonymous* parenthesized expression on the right side of a binding — a default sneaks back in:

```
@func: (2 * 2);      // bare parens on an RHS: stored unevaluated (deferred default)
@value: $(4 * 4);    // $ needed to force evaluation-then-storage
```

So bare RHS function atoms defer, with `$()` as the override — a deferred default with a marked exception, hiding inside a scheme whose whole pitch was "no defaults." (Note the polarity: `$` as the force-eval marker is the same polarity as the Jan 2021 spec's `$[]` eager marker. The old idea resurfaced without anyone deciding it.)

## Why the explicit branch felt bad: the noise problem

Every token pays a tax. Most bindings are plain values and most uses are plain reads, but the explicit branch makes *every* name carry a semantic decision sigil. Uniform explicitness optimizes for a reader who is equally confused everywhere; no such reader exists past week one. (Design principle to keep: Huffman-code the syntax — frequent things unmarked/short, rare things marked. Larry Wall cites this explicitly as a Perl design principle.)

## The Tcl direction: mark evaluation, not reference

Tcl's model, which lands strangely close to Enzo:

- Bare word = the name itself. Unadorned, cheap, most tokens look like this.
- `$x` = substitute the *value* now ("$ = the value of").
- `[cmd args]` = run this now, splice in the result.
- `{...}` = quote/defer — an unevaluated block, handed to commands like `if`/`while`/`proc`, which evaluate it later.

The mapping onto Enzo is uncanny: Enzo's function atoms `(...)` ≈ Tcl's braced blocks (stored code, evaluated later by whatever receives them); Enzo's demand contexts ≈ Tcl's `[...]` (evaluate here, use the result); Enzo's `$` ≈ Tcl's `$` (value-of). Enzo's control flow — `If $x, ( ... )` — is structurally Tcl's `if {cond} {body}`: a command handed quoted blocks. Shell is the low-rent cousin of the same idea: assignment unmarked (`x=5`), reads marked (`$x`).

The key inversion vs. the explicit branch: **Tcl marks the two evaluation events (substitute-now, run-now) and leaves *reference* unadorned.** The explicit branch marked reference AND invocation, taxing everything. Tcl's answer to the noise problem: most tokens are bare; sigils appear exactly where evaluation happens — which is both fully consistent (no context rules) and Huffman-correct (evaluation is the rarer, more consequential event).

## Sketch of a possible Enzo variant (unverified, someday)

- Unadorned keyname = the thing itself (reference). `counter` is the binding.
- `$name` = the value of / invoke. `$` stops meaning "this is a variable" and starts meaning "the value of" — arguably what it already connotes.
- `(...)` stays as the stored-code atom (already Tcl-brace-like).
- Some marker (`!`? `[...]`? nothing-at-statement-level?) = evaluate here and splice, if needed beyond `$`.
- Binding might go unmarked on the LHS (shell-style): `counter: 5;`.

## Open questions to answer before taking this seriously

1. **Collision with bare function invocation.** Enzo already lets named functions be called bare (`function1()`) and referenced bare-ish in definitions. If unadorned keyname = reference, what distinguishes `sort-list` (reference) from a call? Does invocation require `$` or parens always?
2. **Kebab-case ambiguity.** Unadorned names in expression positions revive the `foo-bar` vs subtraction question that the `$` sigil currently helps contain.
3. **What happens to `@`?** If reference is the unadorned default, `@` may become unnecessary — a big simplification — or may survive only for pass-by-reference semantics (its copy-vs-reference job, which is separate from its invoke-vs-defer job; the explicit branch conflated these two jobs in one sigil, which may have been part of its problem).
4. **The visual identity cost.** `$` on every variable is currently Enzo's most recognizable feature. This variant deletes most of them. Is the language still Enzo?
5. **The migration test.** Port 2–3 test modules (vars, functions, pipeline) and *read them cold a week later*. The explicit branch died on inhabitation, not on argument; any successor deserves the same trial.

## Verdict for now

Tabled. The shipped demand-driven design remains the choice, for the frequency-weighted reasons above. But this direction — unlike the explicit branch — has a plausible answer to the noise objection, and it resolves the branch's own hidden inconsistency. Worth ten days, someday.
