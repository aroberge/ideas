"""A file containing a single class meant to keep track of various
configuration choice during a single run/session."""


class State:
    def __init__(self):
        self.console_name = "Ideas Console"
        self.show_original = False
        self.show_changes = False
        self.current_file = ""
        self.active_console = False
        self.original = ""

    def print_original(self, source, header="Original"):
        self.original = source
        if self.active_console:
            return
        if not self.show_original:
            return
        print(f"==========={header}============")
        print(source)
        print("-----------------------------")

    def print_transformed(self, source, header="Transformed"):
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
