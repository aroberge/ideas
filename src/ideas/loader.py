# Code for the loader

import ast

from importlib.abc import Loader
from importlib.util import decode_source

from ideas import ideas_state
from ideas import utils


class IdeasLoader(Loader):  # pylint: disable=R0902
    """A custom loader which will transform the source prior to its execution

    While not as bad as the code used in the current metapath finder,
    it also needs to be rewritten to be more readable.
    """

    def __init__(
        self,
        filename,
        ideas_hook=None,
        callback_params=None,
        create_module=None,
        exec_=None,
        module_class=None,
        source_init=None,
        transform_ast=None,
        transform_bytecode=None,
        parse_source=None,
    ):  # pylint: disable=R0913
        self.filename = filename
        self.ideas_hook = ideas_hook
        self.exec_ = exec_
        self.callback_params = callback_params
        self.custom_create_module = create_module
        self.module_class = module_class
        self.source_init = source_init
        self.transform_ast = transform_ast
        self.transform_bytecode = transform_bytecode
        self.parse_source = parse_source

    def create_module(self, spec):
        """Potential replacement for the default create_module method."""
        # Note: I do not have an example of custom module creation yet.
        if self.custom_create_module is not None:
            return self.custom_create_module(spec, callback_params=self.callback_params)
        return None  # use default module creation semantics

    def exec_module(self, module):
        """Import the source code, transform it before executing it so that
        it is known to Python.
        """
        if (
            module.__name__ == ideas_state.source_argument
            and ideas_state.run_as_main_argument
        ):
            module.__name__ = "__main__"

        if self.module_class is not None:
            module.__class__ = self.module_class  # pylint: disable=E0243

        with open(self.filename, mode="rb") as file:
            encoded_source = file.read()
        source = decode_source(encoded_source)
        original_source = source

        source = ideas_state.source_transforms(
            source,
            filename=self.filename,
            module=module,
            callback_params=self.callback_params,
        )

        if ideas_state.show_changes and original_source != source:
            ideas_state.print_source(
                original_source,
                header=f"Original source from {utils.shorten_path(self.filename)}",
            )
            ideas_state.print_source(source, header="Transformed source")

        if self.source_init is not None:
            source = self.source_init() + source

        parse_source = self.parse_source or ast.parse
        try:
            tree = parse_source(source, self.filename, "exec")
        except Exception:
            if ideas_state.verbose:
                print("An exception was raised while attempting to produce an AST.")
            raise

        if self.transform_ast is not None:
            tree = self.transform_ast(tree)

        try:
            code_object = compile(tree, self.filename, "exec")
        except Exception:
            if ideas_state.verbose:
                print("An exception was raised while attempting to produce an AST.")
            raise

        if self.transform_bytecode is not None:
            try:
                code_object = self.transform_bytecode(code_object)
            except Exception:
                if ideas_state.verbose:
                    print(
                        "An exception was raised while trying to modify the bytecode."
                    )
                raise

        if self.exec_ is not None:
            self.exec_(
                code_object,
                filename=self.filename,
                globals_=module.__dict__,
                module=module,
                callback_params=self.callback_params,
            )
        else:
            try:
                exec(code_object, module.__dict__)  # pylint: disable=W0122
            except Exception:
                if ideas_state.verbose:
                    print(
                        "An exception was raised while attempting to execute the code object."
                    )
                raise
