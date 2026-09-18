# # flake8: noqa
# export_hub/utils.py
# import inspect


# export def pdir(obj=None):  # currently meant for internal use by the Team.
#     """Returns the contents of ``__all__`` if available,
#     if not returns what ``dir`` would."""


#     if obj is not None:
#         if hasattr(obj, "__all__"):
#             return obj.__all__
#         return dir(obj)

#     caller_frame = inspect.currentframe().f_back
#     caller_locals = caller_frame.f_locals if caller_frame else {}
#     if obj is None:
#         if "__all__" in caller_locals:
#             return caller_locals["__all__"]
#         else:
#             return list(caller_locals)  # only the keys

export def useful(): print("I'm useful.")

def internal(): pass

