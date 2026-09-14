# flake8: noqa
# For all the files in these tests, in order
# to help identify that we exported the right variables,
# we name variables that should not be exported starting
# either with the suffix 'not_' or 'Not', or simply starting with
# an underscore.

from tests.from_export.hub.mod_a export Widget, Gadget

from tests.from_export.hub.mod_b export *

from tests.from_export.hub.mod_c export (a,
    b,
   c,
d
)

# mod_d defines __all__ as a tuple
from tests.from_export.hub.mod_d export *
