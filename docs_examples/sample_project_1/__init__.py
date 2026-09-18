# We might use this with the public_dir=True option.
# However, since we do not modify __all__ in this file
# we must delete the inserted __dir__ if present

if "__dir__" in globals():
    del __dir__

from .mod_a import *
from .mod_b import *
