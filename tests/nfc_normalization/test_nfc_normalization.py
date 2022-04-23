from ideas.examples import nfc_normalization
from ideas.import_hook import remove_hook


def test_nfc_normalization():
    hook = nfc_normalization.add_hook()
    from . import n_set  # noqa
    remove_hook(hook)