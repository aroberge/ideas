"""Constants defined by the UPPERCASE_NAME convention"""

XX = 36
XX = 44
XX += 2
globals()["XX"] = "Sneaky"
assert XX == 36, "Uppercase constant did not change value"

a_b = 1
a_b = 4
assert a_b == 4, "Regular variable can change its value."


YY = 1, 2, 4
YY = 3, 3
YY = 1
assert YY == (1, 2, 4), "Constant tuple did not change value"
