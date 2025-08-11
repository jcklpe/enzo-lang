## 1. **What Is a State/Type Transition?**

It means taking an instance of one variant of a blueprint group and converting it into another variant, possibly carrying over or modifying data.
 Think:

- A **Goblin** becomes an **Orc** after some event
- A **DraftInvoice** becomes a **FinalizedInvoice**
- An **Egg** becomes a **Larva**, then a **Butterfly**

------

## 2. **How Might This Look in Enzo?**

Assume you have blueprint variants:

```
enzo


CopyEdit
Monster variants:
    Goblin: <[ health: Number, mischief: Number ]>,
    or Orc: <[ health: Number, rage: Number ]>,
    or Troll: <[ health: Number, bellow: Text ]>;
```

Let’s say you want a **Goblin** to become an **Orc** under certain conditions (say, after a magical transformation or as a result of battle).

### **A. Explicit Transition Function**

You could define a function to “upgrade” the type:

```
evolve-to-orc: (
    param $goblin: Monster.Goblin;
    // take goblin's health, maybe increase it, give starting rage
    Monster.Orc[
        $health: $goblin.health + 20,
        $rage: 10
    ] :> $orc;
    return($orc);
);
```

And use it in a pipeline:

```
$enemy then
    if $this is a Goblin and $this.health is less than 10,
        evolve-to-orc($this)
    end
    :> $enemy;
```

Now, if the enemy was a Goblin with low health, it “mutates” to an Orc—*type-changing in the pipeline*.

### **B. Generic Type-Switching**

You could also have a generic pattern for “switching” to any variant:

```
become: (
    param $new-variant: ;
    param $data: [ ];
    $new-variant[$data...]
);

// Usage:
$creature then become(Monster.Troll, [health: 200, bellow: "RAAARGH"]);
```

This is a bit like “type casting” but with full control over new fields.

------

## 3. **Pipeline State Transitions in Practice**

Here are some broader *scenarios*:

- **Evolution/Level Up:**
   A character reaches enough XP to become a higher class.

  ```
  $player
      then if $this.xp is greater than 1000,
          become(Hero.Warrior, [health: $this.health + 50, power: 20])
      end
      :> $player;
  ```

- **Workflow States:**
   Document moves from “draft” to “review” to “approved.”

  ```
  $doc
      then if $this.status is "draft" and $this.ready,
          become(Document.Review, [reviewer: "Kim"])
      end;
  ```

- **Data Migration:**
   Data structure “version upgrades” as it passes through processing steps.

------

## 4. **Why Is This Useful?**

- **Clarity:** No mysterious mutation; you see when/why/how an object changes “type.”
- **Safety:** Only allowed transitions, with type-checked field updates.
- **Composability:** These transitions can be part of larger, readable pipelines alongside logic and side effects.

------

## 5. **Comparison to Other Paradigms**

- In most OOP, changing an object’s type “in place” is discouraged or impossible.
- In functional languages with sum types (like Rust, Elm, F#), this is idiomatic—but Enzo makes it more readable and accessible for non-experts.