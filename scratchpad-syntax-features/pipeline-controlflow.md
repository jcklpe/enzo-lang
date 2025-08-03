a. Conditional Operations in Pipelines
Allow control flow “steps” inside a pipeline.
```javascript!
$goblin
  then take-damage($this, 30)
    then if $this.health is less than 1, (
        set-status($this, "dead")
    )
  :> $goblin;
```