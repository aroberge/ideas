# coding: experimental-syntax

from experimental-syntax import fraction_literal
from experimental-syntax import decimal_literal

assert 1 /3F == Fraction(1, 3)
assert 0.33D == Decimal('0.33')
