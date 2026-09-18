# tortue_demo
try:
    from ideas.included import french_repeat
except ImportError: # ideas is not installed
    import os
    import sys
    os.chdir("..")
    sys.path.insert(0, os.getcwd())

    from ideas.included import french_repeat


french_repeat.add_hook()

import tortue  # noqa
