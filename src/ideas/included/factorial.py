"""Enable expressions such as 3! to be recognized as a factorial"""

from token_utils import tokenize, untokenize, BracketStack, pairwise, split_at_token
from ideas import create_hook


def source_init():
    """Adds required import so that ``Fraction`` is a known object."""
    import_factorial = "from math import factorial\n"
    return import_factorial


def transform_source(source, **_kwargs):
    tokens = tokenize(source)
    stack = BracketStack()
    new_tokens = []

    for token, next_ in pairwise(tokens):
        if (
            next_ == "!"
            and token.is_immediately_before(next_)
            and (token.is_integer() or token.is_identifier())
        ):
            token.string = f"factorial({token.string})"
            next_.string = ""
        elif next_ == "!" and token.is_immediately_before(next_) and token == ")":
            matching_bracket = stack.add(token)
            next_.string = ""
            new_tokens, remainder = split_at_token(new_tokens, matching_bracket)
            matching_bracket.string = "factorial("
            new_tokens.append(matching_bracket)
            new_tokens.extend(remainder)
        else:
            if token.is_bracket():
                stack.add(token)
        new_tokens.append(token)

    return untokenize(new_tokens)


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = create_hook(
        name=__name__,
        source_init=source_init,
        transform_source=transform_source,
    )
    return hook
