"""This module contains code specific to iPython/Jupyter notebooks."""

from ideas import current_state


def set_up_ipython_shell(
    ipython_shell,
    ipython_ast_node_transformer=None,
    source_init=None,
    transform_source=None,
):
    if transform_source is not None:
        ipython_source_transformer = make_ipython_source_transformer(transform_source)
        ipython_shell.input_transformers_cleanup.append(ipython_source_transformer)

    if source_init is not None and source_init().strip():
        print("   The following initializing code from ideas is included:\n")
        print(source_init().strip())
        lines = [line for line in source_init().splitlines() if line.strip()]
        for line in lines:
            ipython_shell.ex(line)

    if ipython_ast_node_transformer is not None:
        wrapped_ipython_ast_node_transformer = make_ipython_ast_node_transformer(
            ipython_ast_node_transformer
        )
        ipython_shell.ast_transformers.append(wrapped_ipython_ast_node_transformer())


def make_ipython_source_transformer(transform_source):
    """Takes a source transform and makes returns an IPython compatible
    source transformer.
    """

    # This is done as during the cleanup phase
    # (``ipython_shell.input_transformers_cleanup``), as opposed to the
    # post phase (``ipython_shell.input_transformers_post``) so that
    # transformations that work on code blocks (such as ``repeat``)
    # can work properly.
    def ipython_source_transformer(lines):  # noqa
        # In IPython, the source transformation operates on a list of lines
        original_source = "".join(lines)
        source = transform_source(original_source)
        if current_state.show_changes and source != original_source:
            current_state.print_transformed(source, header="New: ")
        lines = source.splitlines(keepends=True)
        return lines

    return ipython_source_transformer


def make_ipython_ast_node_transformer(ipython_ast_node_transformer):
    """Takes an AST transformer designed to work with IPython,
    and wraps it to add a warning in case the user would like to
    see how the code is actually transformed, since this is not
    possible when using IPython.
    """

    def wrapped_ipython_ast_node_transformer():
        if current_state.show_changes:
            print(
                "Cannot show the changed source for AST transform in IPython/Jupyter."
            )
            current_state.show_changes = False
        return ipython_ast_node_transformer

    return wrapped_ipython_ast_node_transformer
