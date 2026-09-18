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
    if ideas_state.verbose:
        print(text)


# TODO: Add test for french_repeat
# TODO: Ensure that all existing hooks are tested.
# TODO: Refactor and clean-up the code


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

    def find_spec(self, fullname, path, target=None):  # pylint: disable=W0613
        """finds the appropriate properties (spec) of a module, and sets
        its loader."""
        if not self.ideas_hook.enabled:
            verbose_finder(
                f"Hook {self.ideas_hook.name} disabled in IdeasMetaPathFinder."
            )
            return None

        # avoid lots of spurious print statements when running verbose tests
        if fullname == "pygments":
            return None

        verbose_finder(f"\n{self.ideas_hook.name}: inside find_spec")

        if not path:
            path = [os.getcwd()] + sys.path

        if self.inform_about_all_possible_paths:  # Do only once
            verbose_finder(
                "The following paths *might* be searched as they are in sys.path:"
            )
            for p in path:
                verbose_finder(f"    {utils.shorten_path(p)}")
            if self.ideas_hook.excluded_paths:
                verbose_finder(
                    "The following have been set as 'excluded' for this import hook."
                )
                for p in self.ideas_hook.excluded_paths:
                    verbose_finder(f"    {utils.shorten_path(p)}")
            self.inform_about_all_possible_paths = False

        if "." in fullname:
            module_name = fullname.split(".")[-1]
        else:
            module_name = fullname

        for entry in path:
            skip = False
            for sub_path in self.ideas_hook.excluded_paths:
                if entry.lower().startswith(sub_path.lower()):
                    skip = True
                    verbose_finder(f"Skipping over: {utils.shorten_path(entry)}")
                    break
            if skip:
                continue

            for extension in self.ideas_hook.extensions:
                if not extension.startswith("."):  # be forgiving ...
                    extension = "." + extension
                filename = os.path.join(entry, module_name + extension)

                verbose_finder(f"Searching for {utils.shorten_path(filename)}")
                if os.path.exists(filename):
                    verbose_finder(f"Found: {utils.shorten_path(filename)}\n")
                    break
                verbose_finder(
                    "    IdeasMetaPathFinder did not find "
                    + f"{utils.shorten_path(fullname)}\n",
                )
            else:
                continue

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
            )

        verbose_finder(f"{self.__repr__()} cannot import {fullname}\n")

        return self.basic_find_spec(fullname=fullname, path=path, target=None)
        # return None  # we don't know how to import this

    def basic_find_spec(self, fullname, path, target=None):

        if fullname in utils.std_lib_names:  # Avoid circular imports for some hooks
            return None
        if path is None or path == "":
            path = [os.getcwd()]  # top level import --
        if "." in fullname:
            *parents, name = fullname.split(".")
        else:
            name = fullname
        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + ".py")
                submodule_locations = None

            if not os.path.exists(filename):
                continue

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

        return None  # we don't know how to import this
