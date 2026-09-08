import pytest
from ideas import remove_hook

@pytest.fixture(autouse=True, scope="function")
def some_function_name():
    remove_hook("*")
    yield
    remove_hook("*")