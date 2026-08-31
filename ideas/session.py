"""A file containing a single class meant to keep track of various
configuration choice during a single run/session."""

# This is a global state object for the project, which is normally
# considered to be a bad practice as it might seem to make it
# more difficult to see the influence of a given change.
# In practice, we have found this to be an easier way to keep
# the interactive console in sync with changes introduced by
# various transformers.
import sys

from .ideas_hook import IdeasHook


class State:
    """Keeps track of various configuration choices during a single run/session."""

    def __init__(self):
        self.console_name = "*Ideas Console*"  # chosen to not be a valid filename
        self.show_original = False  # Print the source code prior to a transformation?
        self.active_console = False
        self.original = ""  # code prior to transformation
        self.verbose = False  # diagnostic
        self.show_changes = False  # Do we print the transformed source code?
        self.transforming_modules = []
        self.hooks = []
        # The following is the source argument passed to __main__.py
        self.source_argument = None  # py [...] -m ideas [...] source_argument
        self.run_as_main_argument = False

    def get_hook_by_name(self, name):
        """Finds a previously imported hook based on its name.

        If it is one of the included examples, the name can be written
        as 'module_name' to be equivalent to 'ideas.examples.module_name'."""
        for hook in self.hooks:
            if hook.name == name:
                return hook
        # Perhaps we're trying to find a hook from the examples folder
        if "." not in name:
            name = "ideas.examples." + name
        for hook in self.hooks:
            if hook.name == name:
                return hook
        if self.verbose:
            print(f"Did not find a hook named {name}.")

    def _add_hook(self, hook):
        """Adds a created IdeasHook instance to the current list."""
        # TODO: check to see if a hook by that name already exists. If so,
        # append the new one but disable it before, and print an error message.
        assert isinstance(hook, IdeasHook)
        self.hooks.append(hook)
        if self.verbose:
            print(f"Added hook {hook.name}")

    def remove_hook(self, name_or_hook):
        """Removes completely a given import hook, either by its name
        or by the an IdeasHook instance.

        Since many of the import hooks are found in the ideas.examples directory
        one can use "module_name" as an abbreviation of "ideas.examples.module_name".
        """
        if isinstance(name_or_hook, str):
            hook = self.get_hook_by_name(name_or_hook)
            if hook is None:
                print(f"ERROR: {name_or_hook} not found.")
                return
        elif not isinstance(name_or_hook, IdeasHook):
            print(f"ERROR: {name_or_hook} not found.")
            return
        else:
            hook = name_or_hook

        if hook.meta_path_finder not in sys.meta_path:
            print(f"ERROR: {hook} not found in sys.meta_path")
            return
        sys.meta_path.remove(hook.meta_path_finder)
        self.hooks.remove(hook)

    def list_hooks(self):
        """Lists the import hooks that have been activated together
        with their status (currently enabled or not).
        """
        if not self.hooks:
            print("No imported hook.")
            return
        for hook in self.hooks:
            enabled = "enabled" if hook.enabled else "disabled"
            print(f"  {hook.name}: {enabled}")

    def disable_hook(self, name_or_hook):
        """Disables a given import hook, either by its name or by the IdeasHook
        instance. Use name_or_hook="*" as a shortcut for disabling all hooks.

        Since many of the import hooks are found in the ideas.examples directory
        one can use "module_name" as an abbreviation of "ideas.examples.module_name".
        """
        if name_or_hook == "*":
            for hook in self.hooks:
                hook.enabled = False
            return

        potential_hook = None
        for hook in self.hooks:
            if (hook.name == name_or_hook) or hook == name_or_hook:
                hook.enabled = False
                return
            elif hook.name == "ideas.examples." + name_or_hook:
                potential_hook = hook
        else:
            if potential_hook is not None:
                potential_hook.enabled = False
                return
        print(f"Could not find hook {name_or_hook}. Here are the known hooks:")
        self.list_hooks()

    def enable_hook(self, name_or_hook):
        """Enables a given import hook, either by its name or by the IdeasHook
        instance. Use name_or_hook="*" as a shortcut for disabling all hooks.

        Since many of the import hooks are found in the ideas.examples directory
        one can use "module_name" as an abbreviation of "ideas.examples.module_name".
        """
        if name_or_hook == "*":
            for hook in self.hooks:
                hook.enabled = True
            return

        potential_hook = None
        for hook in self.hooks:
            if (hook.name == name_or_hook) or hook == name_or_hook:
                hook.enabled = True
                return
            elif hook.name == "ideas.examples." + name_or_hook:
                potential_hook = hook
        else:
            if potential_hook is not None:
                potential_hook.enabled = True
                return
        print(f"Could not find hook {name_or_hook}. Here are the known hooks:")
        self.list_hooks()

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

    def source_transforms(
        self, source, filename=None, module=None, callback_params=None
    ):
        for hook in self.hooks:
            if hook.enabled and hook.transform_source is not None:
                print(f"Transforming from module {hook.name}")
                source = hook.transform_source(
                    source,
                    filename=filename,
                    module=module,
                    callback_params=callback_params,
                )

        return source


current_state = State()
