"""As their name indicates, import hooks only work on files that are imported,
and not on the main script. This file contains a single variable
that is set to 'some_script' when executing a script using

    python -m ideas some_script[.py]

Then, prior to execution, some_script.__name__ is set to __main__,
after which the variable main_name here is set back to None.
"""
main_name = None