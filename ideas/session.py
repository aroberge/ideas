"""A file containing a single class meant to keep track of various
configuration choice during a single run/session."""


class State:
    """Keeps track of various configuration parameters"""

    def __init__(self):
        self.console_name = "Ideas Console"
        self.show_original = False
        self.current_file = ""
        self.active_console = False
        self.original = ""
        self.verbose_finder = False
        self.show_changes = False

    def print_original(self, source, header="Original"):
        """Depending on configuration, can print the original source
        code of a module that was imported."""
        self.original = source
        if self.active_console:
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


config = State()
