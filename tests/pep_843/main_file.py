# For all the files in these tests, in order
# to help identify that we exported the right variables,
# we name variables that should not be exported starting
# either with the suffix 'not_' or 'Not', or simply starting with
# an underscore.

from tests.pep_843.file_a export Widget, Gadget

from tests.pep_843.file_b export *

from tests.pep_843.file_c export (a,
    b,
   c,
d
)

# the file_d defines __all__ as a tuple
from tests.pep_843.file_d export *
