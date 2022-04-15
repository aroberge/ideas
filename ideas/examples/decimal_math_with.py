"""decimal_math_with.py
------------------------

Defines a fake context environment in which explicit floats are
replaced by decimals.
"""


from ideas import import_hook
import token_utils


def source_init():
    """Adds required import"""
    return "from decimal import Decimal\n"


def transform_source(source, **_kwargs):
    """Does the following transformation::

        with float_as_Decimal:
            a = 1.0
            b = 2.0
        c = 3.0

    to::

        if True: # with float_as_Decimal:
            a = Decimal('1.0')
            b = Decimal('2.0')
        c = 3.0
    """

    new_tokens = []
    decimal_block = False

    indentation = 0
    for line in token_utils.get_lines(source):
        first = token_utils.get_first(line)
        if first is None:
            new_tokens.extend(line)
            continue
        elif first == "with":
            first_index = token_utils.get_first_index(line)
            if len(line) > first_index + 1:
                second = line[first_index + 1]
                if second == "float_as_Decimal":
                    first.string = "if"
                    second.string = "True"
                    indentation = first.start_col
                    decimal_block = True
        elif decimal_block and first.start_col > indentation:
            for token in line:
                if token.is_number() and "." in token.string:
                    token.string = f"Decimal('{token.string}')"
        else:
            indentation = first.start_col

        new_tokens.extend(line)

    return token_utils.untokenize(new_tokens)


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_source=transform_source,
    )
    return hook
