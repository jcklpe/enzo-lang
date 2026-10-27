## **General Rule (Inferred from Your Tests)**

### **Rule:**

> **Every top-level statement or expression must be terminated by a semicolon at the end of its line, unless:**
>
> - The next line is a valid continuation (e.g., a pipeline or block continuation), or
> - The statement is immediately closed by a parenthesis or block delimiter on the same line.

### **Key Points:**

- Single-expression function atoms



  must be terminated by a semicolon if they are on their own line.

  - Example:
    `(6); // valid`
    `(6) // error: missing semicolon`

- **Multi-line blocks:** Each statement must end with a semicolon, except when the next line is a valid continuation (e.g., a pipeline).

- **Return statements:** Must be followed by a semicolon if not immediately closed by a parenthesis on the same line.

- **Commas** are allowed for separating parameters or variable declarations, but not as statement terminators.

- A statement that ends a block must have a semicolon if the closing parenthesis is on the next line.

  - Example:

    return(($x + $y)) // error: missing semicolon

    );

    vs.

    return(($x + $y)));

### **Summary Table**

| Pattern                                   | Semicolon Required? | Valid Example                                 | Invalid Example                              |
| ----------------------------------------- | ------------------- | --------------------------------------------- | -------------------------------------------- |
| Single-expression function atom, own line | Yes                 | `(6);`                                        | `(6)`                                        |
| Multi-statement function atom             | Yes                 | `($x: 1; $y: 2; $x + $y;);`                   | `($x: 1 $y: 2; $x + $y;);`                   |
| Statement before block close, same line   | No                  | `return(($x + $y)));`                         |                                              |
| Statement before block close, next line   | Yes                 | `return(($x + $y));` (then `);` on next line) | `return(($x + $y))` (then `);` on next line) |
| Pipeline/continuation                     | No                  | `($semi + $colon)\nthen ($this + 1);`         |                                              |

------

## **How to Implement in the Parser**

1. **After parsing a statement or expression:**
   - If the next token is a newline and the following line is not a valid continuation, require a semicolon at the end of the current line.
   - If the statement is immediately closed by a parenthesis or block delimiter on the same line, a semicolon is not required.
   - If the next line is a valid continuation (e.g., pipeline), a semicolon is not required.
2. **For multi-line blocks:**
   - Each statement must end with a semicolon unless it is immediately followed by a block close on the same line.
3. **For single-expression function atoms:**
   - If the expression is on its own line, it must be terminated by a semicolon.

------

## **Action Plan to Get Tests Passing**

- Update the parser to enforce that **every statement/expression must be terminated by a semicolon at the end of its line, unless the next line is a valid continuation or the statement is immediately closed by a parenthesis on the same line**.
- For error reporting, show the offending line as in your golden file.

------

**Would you like a code snippet for how to update your parser to enforce this rule? If so, let me know which parser file/function handles statement boundaries and I can provide a targeted patch.**

------

## NOTE (July 2026): actual current behavior, a footgun, and a possible UX fix

**Everything above is stale.** The strict per-line rule described above was never what got implemented. Verified against the current parser + empirical tests:

### What the implementation actually does

- Statements self-delimit by structure. Semicolons (and commas) after a statement are **optional** and greedily consumed (`parse_statements`, parser.py ~786). `$x: 5 $y: 10 $x + $y` parses fine with no separators at all.
- Newline tokens are filtered before parsing — pure formatting, never semantic.
- Semicolons are **load-bearing in exactly one situation**: a value expression followed by `(...)`. Without a semicolon between them, the parens are parsed as a *function invocation* on the preceding expression. The parser has a dedicated check for this (parser.py ~238–250: it scans for a semicolon between the base expression's end and the `LPAR` before committing to the call reading).

So the real rule is: **a semicolon is a terminator you only need when an expression could greedily continue — in practice, when the next token is `(`.**

### The footgun

Because newlines mean nothing, this misparses **silently** when arities happen to line up:

```
$f: (param $a: 0; return($a + 1));
$f
(3 * 3);
```

Intended: invoke `$f` (→ 1), then evaluate `(3 * 3)` (→ 9). Actual: parsed as `$f(9)` → prints `10`, no error, nothing else. (If `$f` took zero params you'd at least get "too many args" — the with-param case is the dangerous one.)

This is the same hazard class as JavaScript ASI's lines-starting-with-`(`-or-`[` problem, and the case Odin's newline-sensitive insertion rules exist to handle. It arises from the intersection of three individually-good choices: non-semantic newlines + optional semicolons + parens-as-invocation. Any two are safe; all three create this one ambiguity. Following documented Enzo style (semicolons everywhere) never triggers it.

### Possible UX-oriented fix (design decision, not a bug fix)

Keep newlines non-semantic for *parsing*, but retain their positions for *diagnostics only*. When the parser commits to the invocation reading AND a newline sits between the value and the `(`, emit a warning:

> `$f` followed by `(...)` on a new line was read as a function call — add `;` after `$f` if you meant two separate statements.

A warning isn't syntax, so the decouple-syntax-from-formatting principle survives intact; and this is the one spot where stricter feedback passes the proportionality test (a deviation here *can* silently harm). Alternative homes for the same check: the CLI linter layer, or the VS Code extension. Left as a note rather than a to-do since the project is feature-frozen.

------

### **Summary Table**

| Pattern                                   | Semicolon Required? | Valid Example                                 | Invalid Example                              |
| ----------------------------------------- | ------------------- | --------------------------------------------- | -------------------------------------------- |
| Single-expression function atom, own line | Yes                 | `(6);`                                        | `(6)`                                        |
| Multi-statement function atom             | Yes                 | `($x: 1; $y: 2; $x + $y;);`                   | `($x: 1 $y: 2; $x + $y;);`                   |
| Statement before block close, same line   | No                  | `return(($x + $y)));`                         |                                              |
| Statement before block close, next line   | Yes                 | `return(($x + $y));` (then `);` on next line) | `return(($x + $y))` (then `);` on next line) |
| Pipeline/continuation                     | No                  | `($semi + $colon)\nthen ($this + 1);`         |                                              |

------

## **How to Implement in the Parser**

1. **After parsing a statement or expression:**
   - If the next token is a newline and the following line is not a valid continuation, require a semicolon at the end of the current line.
   - If the statement is immediately closed by a parenthesis or block delimiter on the same line, a semicolon is not required.
   - If the next line is a valid continuation (e.g., pipeline), a semicolon is not required.
2. **For multi-line blocks:**
   - Each statement must end with a semicolon unless it is immediately followed by a block close on the same line.
3. **For single-expression function atoms:**
   - If the expression is on its own line, it must be terminated by a semicolon.

------

## **Action Plan to Get Tests Passing**

- Update the parser to enforce that **every statement/expression must be terminated by a semicolon at the end of its line, unless the next line is a valid continuation or the statement is immediately closed by a parenthesis on the same line**.
- For error reporting, show the offending line as in your golden file.

------

**Would you like a code snippet for how to update your parser to enforce this rule? If so, let me know which parser file/function handles statement boundaries and I can provide a targeted patch.**