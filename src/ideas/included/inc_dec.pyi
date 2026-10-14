from _typeshed import Incomplete

import token_utils

def is_pre(
    tok2: Incomplete, tok3: Incomplete, tok4: Incomplete, plus_or_minus: Incomplete
) -> Incomplete: ...
def is_post(
    tok2: Incomplete, tok3: Incomplete, tok4: Incomplete, plus_or_minus: Incomplete
) -> Incomplete: ...
def valid_before_guard(tok1: Incomplete, tok2: Incomplete) -> Incomplete: ...
def valid_after_guard(tok4: Incomplete, tok5: Incomplete) -> Incomplete: ...
def is_pre_increment(
    tok1: Incomplete,
    tok2: Incomplete,
    tok3: Incomplete,
    tok4: Incomplete,
    tok5: Incomplete,
) -> Incomplete: ...
def is_pre_decrement(
    tok1: Incomplete,
    tok2: Incomplete,
    tok3: Incomplete,
    tok4: Incomplete,
    tok5: Incomplete,
) -> Incomplete: ...
def is_post_increment(
    tok1: Incomplete,
    tok2: Incomplete,
    tok3: Incomplete,
    tok4: Incomplete,
    tok5: Incomplete,
) -> Incomplete: ...
def is_post_decrement(
    tok1: Incomplete,
    tok2: Incomplete,
    tok3: Incomplete,
    tok4: Incomplete,
    tok5: Incomplete,
) -> Incomplete: ...
def transform_source(source: Incomplete, **_kwargs: Incomplete) -> Incomplete: ...
def add_hook(**_kwargs: Incomplete) -> Incomplete: ...
