#!/usr/bin/env bash
#### ┳┳┓        ┓  ┏┳┓
#### ┃┃┃┏┓┏┓┓┏┏┓┃   ┃ ┏┓┏╋┏
#### ┛ ┗┗┻┛┗┗┻┗┻┗   ┻ ┗ ┛┗┛
# Run through a bunch of examples in one shot.
# You’ll still eyeball the results manually.
poetry install
poetry run enzo <<'EOF'
$x: 10
$y: 3 + 2
$x + $y

$colors: ["red", "green", "blue", "yellow"]
$colors.3
$i: 2
$colors.$i

"10 plus 5 is: <$x + $y>"
"color <$i> is <$colors.$i>"

$table: { $name: "Alice", $age: 30 }
$table
$table.name
$table.age


$table.name <: "Bob"
$table.name
$table

$table2 : { $foo: 42, $bar: "hello" }
$table2.bar
$table2.foo <: 100
$table2

$notalist : "oops"
$notalist.1
$table.badprop
EOF
