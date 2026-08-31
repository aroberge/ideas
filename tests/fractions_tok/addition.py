from fractions import Fraction as F
print("1 / 10 + 2 / 10 = ", 1 / 10 + 2 / 10)

assert 1 / 10 + 2 / 10 == 3 / 10, "simple addition"

assert 3**2 / 5 == F(9, 5)
