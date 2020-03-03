"""lambda_encoding.py
------------------------

This codec replaces any Python identifier (token) represented by the
single Greek letter 'λ' by the corresponding string 'lambda' which is
the Python keyword.

The source is assumed to be actually encoded in utf-8.
"""


from ideas import encoding
import token_utils


def transform_source(source, **kwargs):
    """Simple transformation: replaces any single token λ by lambda.

    By defining this function, we can also make use of Ideas' console.
    """
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token == "λ":
            token.string = "lambda"
    return token_utils.untokenize(tokens)


encoding.register_encoding(
    encoding_name="lambda_encoding",
    transform_source=transform_source,
    hook_name=__name__,
)
