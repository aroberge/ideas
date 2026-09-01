from ideas import add_patch, remove_hook, remove_patches

def on_socket_import(module):
    setattr(module, "gethostname", lambda: "fake_hostname")
    return module


def test_patch():
    import socket
    assert socket.gethostname() != "fake_hostname", "True host name before patch"

    from ideas import add_patch
    add_patch('socket', on_socket_import)

    import socket
    assert socket.gethostname() == "fake_hostname", "Fake host name after patch"

    # Remove the entry created by patching_hook
    remove_hook("ideas.null_hook")
    remove_patches()