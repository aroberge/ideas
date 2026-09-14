# For all the files in these tests, in order
# to help identify that we exported the right variables,
# we name variables that should not be exported starting
# either with the suffix 'not_' or 'Not', or simply starting with
# an underscore.

spam = "spam"
ham = "ham"
not_spam = "not_spam"
not_ham = "not_ham"

# Note the use of a tuple instead of a list.
__all__ = ("spam", "ham")