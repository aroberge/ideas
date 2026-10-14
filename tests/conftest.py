import pytest
from ideas import ideas_state


@pytest.fixture(autouse=True, scope="function")
def some_function_name():
    ideas_state._clear()
    yield
    ideas_state._clear()
