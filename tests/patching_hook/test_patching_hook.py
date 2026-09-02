import sys
from ideas import add_patch, remove_hook, disable_hook, current_state
from ideas.examples import function_keyword, nobreak

def on_socket_import(module):
    setattr(module, "gethostname", lambda: "fake_hostname")
    return module


def test_patch():
    import socket
    assert socket.gethostname() != "fake_hostname", "True host name before patch"

    from ideas import add_patch
    add_patch('socket', on_socket_import)

    # During patching, we disable all hooks, and restore their states afterward.
    # The following hooks are added to confirm that this was done correctly.
    hook_f = function_keyword.add_hook()
    disable_hook("function_keyword")
    hook_n = nobreak.add_hook()

    # Confirm the status before
    assert not hook_f.enabled, "Hook disabled for test"
    assert hook_n.enabled, "Hook enabled for test"

    import socket
    assert socket.gethostname() == "fake_hostname", "Fake host name after patch"
    assert not current_state.patches, "Patches should be removed"

    # Confirm the status after.
    assert not hook_f.enabled, "Hook remained disabled after test"
    assert hook_n.enabled, "Hook remained enabled after test"

    # Clean up
    remove_hook("*")

def test_freeze():
    from ideas.utils import freeze_globally
    import math as original_math

    pi = original_math.pi

    math = freeze_globally("math")

    exception_raised = False
    try:
        math.pi = 4
    except AttributeError:
        exception_raised = True
    assert exception_raised, "Exception was raised when trying to change value"

    original_math.pi = 4  # can change value of this object

    assert math.pi != original_math.pi, "Value was changed in original"
    assert math.sqrt(4) == original_math.sqrt(4)

    # remove and import again: it should be the frozen module
    del math
    import math

    assert math.pi == pi

    # Clean up
    sys.modules.pop("math")
