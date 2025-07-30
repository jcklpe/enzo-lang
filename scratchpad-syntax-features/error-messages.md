Gleam has some cool error messages:
```
error: Unknown record field

  ┌─ ./src/app.gleam:8:16
  │
8 │ user.alias
  │     ^^^^^^ Did you mean `name`?

The value being accessed has this type:
    User

It has these fields:
    .name
```