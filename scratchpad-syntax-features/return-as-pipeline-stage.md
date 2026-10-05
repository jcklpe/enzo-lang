### Return as a pipeline stage
Because `return` is written like a function call (`return($x)`), it reads as if it could be the last stage of a `then` pipeline, receiving the piped value through `$this`:

```javascript!
add-then-double: (
    param $n: ;
    $n then ($this + 1) then ($this * 2) then return($this);
);
add-then-double(4); // would return 10
```

Nobody designed this as a feature. It falls out of two separate syntax choices: return looks like a call, and `then`/`$this` can feed any call. Under this reading a pipeline can end a function body without a temporary binding:

```javascript!
// today
$n then ($this + 1) then ($this * 2) :> $out;
return($out);

// with return as a pipeline stage
$n then ($this + 1) then ($this * 2) then return($this);
```

#### Status in the current interpreter (checked 2026-10-04, `classic-algos` branch)
Not supported. Two things block it:
- `return` is lexed as a reserved `RETURN` keyword and parsed only at the start of a statement, not as a callable expression, so `4 then return($this);` fails with `Unexpected token: RETURN`.
- `$this` inside a named function declaration currently errors with `can't use reserved $this keyname in named function declaration`, so pipelines using `$this` can't appear in function bodies at all yet.

Supporting this would mean either making `return` an expression that can take a piped argument, or special-casing `then return(...)` in the pipeline parser, plus allowing `$this` in function bodies when it is scoped to a `then` pipeline.

#### Unexpected patterns that emerge from Enzo's syntax design
This is a seed for a possible broader doc collecting idioms that Enzo's syntax suggests or permits but that were never designed in directly. This is the first entry.
