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

**Would you like a code snippet for how to update your parser to enforce this rule? If so, let me know which parser file/function handles statement boundaries and I can provide a targeted patch.**### **Summary Table**

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