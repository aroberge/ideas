"""confused_math_bc.py
------------------------

Import hook that performs bytecode changes,
swapping BINARY_ADD and BINARY_MULTIPLY.

Note: If code contains something like a + b, or a * b, where
a and b are integer literals (e.g. 2 + 4), the operations are
done prior to the creation of a code object and thus are
not captured by this transformation.

Requires Python version >= 3.6 as it assumed that bytecode
instructions are "wordcode" i.e. that instructions like
BINARY_ADD and BINARY_MULTIPLY will fall on even-index values
of the bytecode.
"""
import dis
import sys

from types import CodeType

from ideas import import_hook

assert sys.version_info >= (3, 6)

ADD = dis.opmap['BINARY_ADD']
MUL = dis.opmap['BINARY_MULTIPLY']


def swap_add_mul(bytecode):
    """Interchange BINARY_ADD and BINARY_MULTIPLY"""
    new_bc = []
    for i, b in enumerate(bytecode):
        if b == ADD and i % 2 == 0:
            new_bc.append(MUL)
        elif b == MUL and i % 2 == 0:
            new_bc.append(ADD)
        else:
            new_bc.append(b)
    return bytes(new_bc)


def create_new_co(code_object):
    """Recursivelly creates new code objects from old ones, swapping
    BINARY_ADD and BINARY_MULTIPLY.
    """
    new_code = swap_add_mul(code_object.co_code)
    new_const = []
    for c in code_object.co_consts:
        if isinstance(c, CodeType):
            new_const.append(create_new_co(c))
        else:
            new_const.append(c)
    new_code_object = CodeType(
        code_object.co_argcount,
        code_object.co_kwonlyargcount,
        code_object.co_nlocals,
        code_object.co_stacksize,
        code_object.co_flags,
        new_code,
        tuple(new_const),
        code_object.co_names,
        code_object.co_varnames,
        code_object.co_filename,
        code_object.co_name,
        code_object.co_firstlineno,
        code_object.co_lnotab,
        code_object.co_freevars,
        code_object.co_cellvars,
    )
    return new_code_object


def transform_bytecode(code_object):
    """Transforms the code object into a new code object"""
    new_code_object = create_new_co(code_object)
    return new_code_object


def add_hook(verbose_finder=False):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        transform_bytecode=transform_bytecode,
    )
    return hook
