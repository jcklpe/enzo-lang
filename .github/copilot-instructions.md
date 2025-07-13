---
applyTo: "**"
---
# Project general coding standards

## Important Context
- The interpreter can be found in folder `~/work/enzo-lang/interpreter/`. `enzo-lang/` is the root project folder but all terminal commands for the interpreter must be run from the interpreter folder.
- The interpreter project is a poetry env so you have to use `poetry run python` instead of just `python`
- please put all debugging related scripts in the "debugging" folder so it doesn't clutter the project space. If you need to debug something it might be helpful to check if a script already exists there too.
- All error messaging and all error handling are centralized to the "error_messaging.py" and "error_handling.py" files.
- When running tests remember this legend at the top of the test runner output:
```
✔ correct expected outcome
✖ failing actual outcome
```
