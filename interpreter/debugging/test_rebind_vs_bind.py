#!/usr/bin/env python3

import sys
sys.path.append('..')

import subprocess

# Test rebinding vs binding in conditional scope
test_content = '''$test-var: "original";
"Before conditional: <$test-var>";

If True, (
    // This should create a NEW shadowed variable
    $test-var: "shadowed";
    "Inside conditional (binding): <$test-var>";
);
"After conditional (should be original): <$test-var>";

If True, (
    // This should REBIND the original variable
    "rebound" :> $test-var;
    "Inside conditional (rebinding): <$test-var>";
);
"After rebinding: <$test-var>";
'''

test_file = '/tmp/test_rebind_vs_bind.enzo'
with open(test_file, 'w') as f:
    f.write(test_content)

print("=== Testing rebinding vs binding in conditional ===")
result = subprocess.run(['poetry', 'run', 'enzo', test_file],
                       capture_output=True, text=True, cwd='.')

print("STDOUT:")
print(repr(result.stdout))
print("STDERR:")
print(repr(result.stderr))
print("Visual output:")
print(result.stdout)
if result.stderr:
    print("Errors:")
    print(result.stderr)
