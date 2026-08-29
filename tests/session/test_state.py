from ideas import current_state, remove_hook
from ideas.ideas_hook import IdeasHook

def test_get_hook_by_name():
    from ideas.examples.function_keyword import add_hook
    
    add_hook()
    hook = current_state.get_hook_by_name("ideas.examples.function_keyword")
    assert isinstance(hook, IdeasHook)
    assert hook.name == "ideas.examples.function_keyword"
    #
    # For examples hooks, we should also be able to retrieve them with a "last name"
    hook = current_state.get_hook_by_name("function_keyword")
    assert isinstance(hook, IdeasHook)
    assert hook.name == "ideas.examples.function_keyword"
    # clean up
    remove_hook(hook)
