import sys
from ideas import utils


class IdeasHook:
    """A custom import hook main object."""

    def __init__(
        self,
        callback_params=None,
        console_only=False,
        create_module=None,
        does_not_play_well_with_others=False,
        exec_=None,
        extensions=None,
        excluded_paths=utils.DEFAULT,
        name="",
        module_class=None,
        parse_source=None,
        source_init=None,
        transform_ast=None,
        transform_bytecode=None,
        transform_source=None,
    ):
        self.callback_params = callback_params
        self.console_only = console_only
        self.create_module = create_module
        if excluded_paths is utils.DEFAULT:
            self.excluded_paths = [utils.PYTHON, utils.SITE_PACKAGES, utils.IDEAS]
        elif excluded_paths is None:
            self.excluded_paths = []
        else:
            self.excluded_paths = excluded_paths
        self.does_not_play_well_with_others = does_not_play_well_with_others
        self.exec_ = exec_
        self.extensions = extensions if extensions is not None else [".py"]
        if not name:
            raise ValueError(
                "IdeasHook name is required and must be the name of its source module."
            )
        self.name = name
        self.module_class = module_class
        self.parse_source = parse_source
        self.source_init = source_init
        self.transform_ast = transform_ast
        self.transform_bytecode = transform_bytecode
        self.transform_source = transform_source

        # The following attribute are created by the IdeasMetaFinder
        self.meta_path_finder = None  # IdeasMetaFinder instance; is it
        self.filename = None
        self.fullname = None
        self.loader = None  # Is this needed?
        # This will normally be changed via a method from session.ideas_state in session.py
        self.enabled = True

        try:
            self.source_module = sys.modules[name]
        except KeyError:
            print("FATAL ERROR!")
            print(
                "IdeasHook object must be created with the name of its source module."
            )
            raise

    def __repr__(self):
        return f"<Ideas import hook: {self.name}>"

    def __eq__(self, other):
        return isinstance(other, IdeasHook) and self.name == other.name
