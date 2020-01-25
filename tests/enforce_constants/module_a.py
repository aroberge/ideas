try:
    from typing import Final
except ImportError:
    class Final:
        pass

const: Final = 1
print("about to print const")
print("const = ", const)
const = 2
const -= 2

a_b = 1
a_b = 4
XX = 36
XX = 44
YY = 1, 2, 4
YY = 3, 3

XX += 2

if __name__ == "__main__":
    XX = '"I am the main module"'
