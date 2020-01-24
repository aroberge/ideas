import types


CONSTANTS = {}


class ModuleWithConstants(types.ModuleType):
    """Special module type that prevents variables identified as constants
       to have their value changed.

       This is used to replace a module __class__ from the default as follows:

           module.__class__ = ModuleWithConstants

       This example only prints a message when an attempt is made to change
       the value of a constant. Alternatively, this could be logged or an
       exception could be raised.

       This example assumes two different ways to declare constants:

           - By giving a True value a parameter named "final";
           - By using ALL_CAPS to identify constants.
    """
    def __setattr__(self, attr, value, final=False):
        if self.__file__ not in CONSTANTS:
            CONSTANTS[self.__file__] = {}

        if attr in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s to %s"
                % (self.__name__, attr, value)
            )
            return

        if (
            final  # from optional type declaration
            or attr == attr.upper()  # Python convention for constant names
        ):
            CONSTANTS[self.__file__][attr] = value

        super().__setattr__(attr, value)
