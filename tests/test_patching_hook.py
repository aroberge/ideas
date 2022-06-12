
def on_socket_import(module):
    setattr(module, "gethostname", lambda: "fake_hostname")
    return module


def test_patch():
    import socket
    assert socket.gethostname() != "fake_hostname", "True host name before patch"

    from ideas import patching_hook
    patching_hook.add_patch('socket', on_socket_import)
    import socket
    assert socket.gethostname() == "fake_hostname", "Fake host name after patch"
