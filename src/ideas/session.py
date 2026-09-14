"""A file containing a single class meant to keep track of various
configuration choice during a single run/session."""

# This is a global state object for the project, which is normally
# considered to be a bad practice as it might seem to make it
# more difficult to see the influence of a given change.
# In practice, we have found this to be an easier way to keep
# the interactive console in sync with changes introduced by
# various transformers.

import os
import sys

from ideas.ideas_hook import IdeasHook


class State:
    """Keeps track of various configuration choices during a single run/session."""

    def __init__(self):
        self.console_name = "*Ideas Console*"  # chosen to not be a valid filename
        self.show_original = False  # Print the source code prior to a transformation?
        self.active_console = False
        self.original = ""  # code prior to transformation
        self.verbose = False  # diagnostic
        self.show_changes = False  # Do we print the transformed source code?
        self.hooks = []
        self.custom_codecs_source_transform = None
        # The following is the source argument passed to __main__.py
        self.source_argument = None  # py [...] -m ideas [...] source_argument
        self.run_as_main_argument = False
        #
        self.patches = {}
        self.console_source_inits = []
        self.max_nb_lines = 8

    def get_hook_by_name(self, name):
        """Finds a previously imported hook based on its name.

        If it is one of the included examples, the name can be written
        as 'module_name' to be equivalent to 'ideas.included.module_name'."""
        for hook in self.hooks:
            if hook.name == name:
                return hook
        # Perhaps we're trying to find a hook from the examples folder
        if "." not in name:
            name = "ideas.included." + name
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
        or by the an IdeasHook instance. Use name_or_hook="*" as a
        shortcut for removing all hooks.

        Since many of the import hooks are found in the ideas.included directory
        one can use "module_name" as an abbreviation of "ideas.included.module_name".
        """
        if name_or_hook == "*":
            for hook in self.hooks:
                sys.meta_path.remove(hook.meta_path_finder)
                self.hooks.remove(hook)
            return

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

        Since many of the import hooks are found in the ideas.included directory
        one can use "module_name" as an abbreviation of "ideas.included.module_name".
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
            elif hook.name == "ideas.included." + name_or_hook:
                potential_hook = hook
        else:
            if potential_hook is not None:
                potential_hook.enabled = False
                return
        print(f"Could not find hook {name_or_hook}. Here are the known hooks:")
        self.list_hooks()

    def enable_hook(self, name_or_hook):
        """Enables a given import hook, either by its name or by the IdeasHook
        instance. Use name_or_hook="*" as a shortcut for enabling all hooks.

        Since many of the import hooks are found in the ideas.included directory
        one can use "module_name" as an abbreviation of "ideas.included.module_name".
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
            elif hook.name == "ideas.included." + name_or_hook:
                potential_hook = hook
        else:
            if potential_hook is not None:
                potential_hook.enabled = True
                return
        print(f"Could not find hook {name_or_hook}. Here are the known hooks:")
        self.list_hooks()

    def print_transformed(self, source, header="New"):
        """Depending on the configuration, can print the transformed
        output if it differs from the original source.
        """
        if not self.show_changes:
            return
        if source == self.original:
            return

        self.print_source(source, header=header)

    def print_source(self, source, header="Original/New"):
        """Prints a maximum of N or N+1 lines of the source code
        where N is ``current_state.max_nb_lines``.

        If there is a single line, it is prefixed by ``header: `.
        Otherwise, it is surrounded by dividers.

        ``header`` is usually either ``"Original"`` or ``"New"``
        """
        lines = source.split("\n")
        if len(lines) == 1:
            print(f"{header}: {source}")
            return

        max_nb_lines = current_state.max_nb_lines
        nb_lines = len(lines)
        if nb_lines == max_nb_lines + 1:
            # We don't want to see an information line stating
            # " ... 1 line not shown"
            max_nb_lines += 1

        shortened_source_indicator = ""
        if nb_lines > max_nb_lines:
            shortened_source_indicator = (
                f" ... {nb_lines - max_nb_lines} lines not shown"
            )
        lines = lines[:max_nb_lines]
        if len(lines) > 10:
            lines = lines[:10]
        while not lines[-1]:
            lines.pop()
        source = "\n".join(lines[:10]) + shortened_source_indicator
        print(f"\n#========== {header} ====")
        for line in lines:
            print(line)
        if shortened_source_indicator:
            print(shortened_source_indicator)
        print(f"#=== End of {header} ====\n")

    def source_transforms(
        self,
        source,
        filename=None,
        module=None,
        callback_params=None,
        console_dict=None,
        **kwargs,
    ):
        """Applies a source transformation from the installed import hooks.

        Returns a new source.
        """
        if kwargs:
            print(
                "FatalError: unkown argument in session.State.source_transform:", kwargs
            )
            print("This argument cannot be handled correctly.")
            print("Shutting down ...")
            os._exit(1)
        for hook in self.hooks:
            if hook.enabled and hook.transform_source is not None:
                source = hook.transform_source(
                    source,
                    filename=filename,
                    module=module,
                    callback_params=callback_params,
                    console_dict=console_dict,
                )

        return source

    def add_patch(self, module_name, func):
        """Adds patch to be applied to a module.

        ``module_name``: the full name of the module to be patched

        ``func``: a callable which takes as a single argument a module object
        and returns a modified (patched) module object.

        ``add_patch`` can be called multiple times; patches will be applied
        sequentially.

        If ``module_name`` has already been imported, it is deleted from
        ``sys.modules`` so that it can be properly patched."""
        # We need at least one active hook to make transformations
        if not self.hooks:
            from ideas.null_hook import add_hook

            add_hook()

        if module_name not in self.patches:
            self.patches[module_name] = []

        self.patches[module_name].append(func)
        if module_name in sys.modules:
            del sys.modules[module_name]

    def remove_patches(self):
        """Mainly for cleaning up after test"""
        self.patches = {}


current_state = State()
