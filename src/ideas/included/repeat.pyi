from _typeshed import Incomplete

from ideas import create_hook, utils
import token_utils

class RepeatSyntaxError(Exception): ...

def transform_source(
    source: Incomplete, callback_params: Incomplete = None, **_kwargs: Incomplete
) -> Incomplete: ...
def add_hook(
    predictable_names: Incomplete = False, **_kwargs: Incomplete
) -> Incomplete: ...
