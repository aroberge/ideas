"""A file containing a single class meant to keep track of various
configuration choice during a single run/session."""

# This is a global state object for the project, which is normally
# considered to be a bad practice as it might seem to make it
# more difficult to see the influence of a given change.
# In practice, we have found this to be an easier way to keep
# the interactive console in sync with changes introduced by
# various transformers.


class State:
    """Keeps track of various configuration choices during a single run/session."""

    def __init__(self):
        self.console_name = "*Ideas Console*"  # chosen to not be a valid filename
        self.show_original = False  # Print the source code prior to a transformation?
        self.active_console = False
        self.original = ""  # code prior to transformation
        self.verbose_finder = False  # diagnostic
        self.show_changes = False  # Do we print the transformed source code?
        self.transforming_modules = []
        self.hooks = []
        # The following is the source argument passed to __main__.py
        self.source_argument = None  # py [...] -m ideas [...] source_argument
        self.main_file_name = None  # ... source_argument.filename.py
        self.main_module = None  # ... source_argument -> main_module

    def add_hook(self, hook):
        self.hooks.append(hook)
        print(f"Added hook {hook.name}")

    def disable_hook(self, name):
        for hook in self.hooks:
            if hook.name == name:
                hook.enabled = False
                return
        else:
            print(f"Could not find hook {name}. Here are the known hooks:")
            for hook in self.hooks:
                print("  ", hook.name)

    def enable_hook(self, name):
        for hook in self.hooks:
            if hook.name == name:
                hook.enabled = True
                return
        else:
            print(f"Could not find hook {name}. Here are the known hooks:")
            for hook in self.hooks:
                print("  ", hook.name)

    def print_original(self, source, header="Original"):
        """Depending on configuration, can print the original source
        code of a module that was imported."""
        self.original = source
        if self.active_console:  # We just typed the original; no need to print again
            return
        if not self.show_original:
            return
        print(f"==========={header}============")
        print(source)
        print("-----------------------------")

    def print_transformed(self, source, header="Transformed"):
        """Depending on the configuration, can print the transformed
        output if it differs from the original source.
        """
        if not self.show_changes:
            return
        if source == self.original:
            return

        lines = source.split("\n")
        if len(lines) == 1:
            print(f"new: {lines[0]}")
            return
        if self.active_console:
            for line in lines:
                print(f"new: {line}")
        else:
            print(f"==========={header}============")
            print(source)
            print("-----------------------------")


current_state = State()
