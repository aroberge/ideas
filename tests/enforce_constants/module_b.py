import module_a

module_a.XX = "new value"  # should not change
assert module_a.XX == 36

module_a.const = "'changing final constant from module test_b'"
assert module_a.const == 1

module_a.a = 42  # not a constant
assert module_a.a == 42

A = 0
A = 2

assert A == 0
A += 1  # cheating
assert A == 1
