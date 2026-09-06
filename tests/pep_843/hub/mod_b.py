# For all the files in these tests, in order
# to help identify that we exported the right variables,
# we name variables that should not be exported starting
# either with the suffix 'not_' or 'Not', or simply starting with
# an underscore.

def cool():
    pass

def _cool():
    pass

def hot():
    pass

def _hot():
    pass