# Rather than writing source/expected in the test file, I use this single
# file and will import the relevant cases from here.
# This will likely make it easier to write/maintain tests.

# First some valid single line transformations
source_1 = "export class ClassName:"
expected_1 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append('ClassName')
class        ClassName:"""

source_2 = "export def function():"
expected_2 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append('function')
def        function():"""

source_3 = "export variable = 3"
expected_3 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append('variable')
variable        = 3"""

# 'export' as a valid identifier

source_4 = "export class export:"
expected_4 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append('export')
class        export:"""

source_5 = "export def export():"
expected_5 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append('export')
def        export():"""

source_6 = "export export = 3"
expected_6 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append('export')
export        = 3"""

# Same as 1, 2, and 3 but indented

source_7 = "    export class ClassName:"
expected_7 = """
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('ClassName')
    class        ClassName:"""

source_8 = "    export def function():"
expected_8 = """
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('function')
    def        function():"""

source_9 = "    export variable = 3"
expected_9 = """
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('variable')
    variable        = 3"""

source_10 = """
# In the following, all of the occurrences of 'export' should be left untouched

from math export pi

export = True

export variable # no assignment

def export():
    export variable = 4
    return True

def test():

    export def inner_test():
        pass
        
class One:
    export variable = True
    export def function():
        pass

class Two:

    export class Three():
    
        export def function():
           pass
"""

expected_10 = source_10

source_11 = """
if True:
    export variable1 = 1
"""

expected_11 = """
if True:

    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('variable1')
    variable1        = 1
"""

source_12 = """
if True:
    def test():
        export var = 2
    export def test2():
        export name = 5
else:
    export class Name:
        pass
"""

expected_12 = """
if True:
    def test():
        export var = 2

    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('test2')
    def        test2():
        export name = 5
else:

    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('Name')
    class        Name:
        pass
"""

# Weird indentation
source_13 = """
if True:
    def test(
):           # ends left of "def"
        export name = 3
"""
expected_13 = source_13
