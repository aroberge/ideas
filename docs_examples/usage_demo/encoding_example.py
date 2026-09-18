# coding: experimental-syntax

from experimental-syntax import fraction_literal  # noqa
from experimental-syntax import decimal_literal  # noqa

assert 1 /3F == Fraction(1, 3)  # noqa
assert 0.33D == Decimal('0.33')  # noqa

print("encoding_example.py ran successfully.")
