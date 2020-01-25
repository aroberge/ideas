"""Constants defined by the Final type hint"""
try:
    from typing import Final
except ImportError:
    class Final:
        pass

const: Final = 1
const = 2
const -= 2
assert const == 1, "Constant declared final did not change value."

a_b = 1
a_b = 4
assert a_b == 4, "Regular variable can change its value."
