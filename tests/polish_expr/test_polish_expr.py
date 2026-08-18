import sys

if sys.version_info >= (3, 8):
    from ideas.examples import polish_expr
from ideas.import_hook import remove_hook

import pytest


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
def test_polish_expr():
    hook = polish_expr.add_hook()
    from . import polish  # noqa
    remove_hook(hook)
    assert polish.x == 11
    assert polish.y == 110
    assert polish.z == 505
