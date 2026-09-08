# Rather than writing source/expected in the test file, I use this single
# file and will import the relevant cases from here.
# This will likely make it easier to write/maintain tests.

source_1 = "export class ClassName:"
expected_1 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append(ClassName)
class        ClassName:"""

source_2 = "export def function():"
expected_2 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append(function)
def        function():"""

source_3 = "export variable = 3"
expected_3 = """
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.append()
variable        = 3"""