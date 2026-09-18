# This will be the finder

import os
import sys

from importlib.abc import MetaPathFinder
from importlib.util import spec_from_file_location
from ideas import ideas_state
from ideas.loader import IdeasLoader
from ideas import utils


def verbose_finder(text):
    """Print some informative text when verbose is set"""
    if ideas_state.verbose_finder:
        print(text)


class IdeasMetaPathFinder(MetaPathFinder):  # pylint: disable=R0902
    """A custom finder to locate modules. The main reason for this code is
    to ensure that our custom loader, which does the code transformations,
    is used.

    This single metapath finder is meant to cover all existing examples
    and has become nearly unreadable. It definitely needs a serious rewrite.
    """

    def __init__(self, ideas_hook=None):
        self.ideas_hook = ideas_hook
        if self.ideas_hook is None:
            raise RuntimeError("IdeasHook instance missing in IdeasMetaPathFinder().")
        self.inform_about_all_possible_paths = True

    def __repr__(self):
        return f"<IdeasMetaPathFinder for {self.ideas_hook.name}>"

    def _set_path(self, path):
        """Removes from the set of all possible paths to search any
        specifically excluded path."""
        # There is nothing of huge significance in this method:
        # 1. It figures out which paths should, in principle, be included in the search
        # 2. It removes from that list those that were explicitly excluded
        #    when creating the import hook
        #
        # It includes a lot of potential diagnostic statements to be printed
        # for debugging purpose.
        # self.inform_about_all_possible_paths ensures that the information is
        # only printed once.

        # Set paths
        if not path:
            if self.inform_about_all_possible_paths:  # Do only once
                verbose_finder(
                    "No search paths were specified.\n"
                    + " Will use the current directory as well as paths included in sys.path"
                )
            path = [os.getcwd()] + sys.path

        # Inform
        if self.inform_about_all_possible_paths:  # Do only once
            verbose_finder("These are the potential search paths")
            for p in path:
                verbose_finder(f"    {utils.shorten_path(p)}")
            if self.ideas_hook.excluded_paths:
                verbose_finder(
                    "\nThe following have been set as 'excluded' for this import hook."
                )
                for p in self.ideas_hook.excluded_paths:
                    verbose_finder(f"    {utils.shorten_path(p)}")
            else:
                verbose_finder("No paths were set as excluded.")

        # Remove excluded paths
        if self.ideas_hook.excluded_paths:
            for entry in self.ideas_hook.excluded_paths:
                if entry in path:
                    path.remove(entry)
                # Inform
            if self.inform_about_all_possible_paths:  # Do only once
                verbose_finder("\nThese are the remaining search paths:")
                for p in path:
                    verbose_finder(f"    {utils.shorten_path(p)}")

        self.inform_about_all_possible_paths = False  # Will not do again
        return path

    def find_spec(self, fullname, path, target=None):  # pylint: disable=W0613
        """finds the appropriate properties (spec) of a module, and sets
        its loader."""
        # Avoid lots of spurious print statements when running verbose tests
        if fullname == "pygments":  # We don't care about modifying "pygments"
            return None

        if not self.ideas_hook.enabled:
            verbose_finder(
                f"Hook {self.ideas_hook.name} disabled in IdeasMetaPathFinder."
            )
            return None

        verbose_finder(f"\n{self.ideas_hook.name}.find_spec():")

        path = self._set_path(path)

        if "." in fullname:
            module_name = fullname.split(".")[-1]
        else:
            module_name = fullname

        found = False
        for entry in path:
            if os.path.isdir(os.path.join(entry, module_name)):
                # this module has child modules
                filename = os.path.join(entry, module_name, "__init__.py")
                submodule_locations = [os.path.join(entry, module_name)]
                if os.path.exists(filename):
                    found = True
            else:
                for extension in self.ideas_hook.extensions:
                    if not extension.startswith("."):  # be forgiving ...
                        extension = "." + extension
                    filename = os.path.join(entry, module_name + extension)
                    submodule_locations = None
                    if os.path.exists(filename):
                        found = True
                        break

            if not found:
                continue

            verbose_finder(f"FOUND '{filename}'")

            return spec_from_file_location(
                fullname,
                filename,
                loader=IdeasLoader(
                    filename,
                    ideas_hook=self.ideas_hook,
                    callback_params=self.ideas_hook.callback_params,
                    create_module=self.ideas_hook.create_module,
                    exec_=self.ideas_hook.exec_,
                    module_class=self.ideas_hook.module_class,
                    source_init=self.ideas_hook.source_init,
                    transform_ast=self.ideas_hook.transform_ast,
                    transform_bytecode=self.ideas_hook.transform_bytecode,
                    parse_source=self.ideas_hook.parse_source,
                ),
                submodule_search_locations=submodule_locations,
            )

        verbose_finder(f"{self.__repr__()} cannot find '{fullname}'")
        return None  # we don't know how to import this
