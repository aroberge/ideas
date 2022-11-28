from ideas.examples import embedded_html
from ideas.import_hook import remove_hook

def test_single_element():
    hook = embedded_html.add_hook()
    result = embedded_html.transform_source("""
def el(*args, **kwargs):
    pass

test_html = :(<div>A Div</div>):
""")
    assert result == """
def el ( * args , ** kwargs ) :
    pass

test_html = (
    el("div",{},
        "A Div",
    ),
)

"""
    print(result)
    remove_hook(hook)

def test_nested():
    hook = embedded_html.add_hook()
    result = embedded_html.transform_source("""
def el(*args, **kwargs):
    pass

test_html = :(
    <div>
        A Div
        with a
        <a href="http://google.com">Link</a>
    </div>
):
""")
    assert result == """
def el ( * args , ** kwargs ) :
    pass

test_html = (
    el("div",{},
        "A Div with a ",
        el("a",{"href": "http://google.com"},
            "Link",
        ),
    ),
)

"""
    print(result)
    remove_hook(hook)

def test_py_attr():
    hook = embedded_html.add_hook()
    result = embedded_html.transform_source("""
def el(*args, **kwargs):
    pass

x = "abcd"

test_html = :(
    <div class={x}>
    </div>
):
""")
    assert result == """
def el ( * args , ** kwargs ) :
    pass

x = "abcd"

test_html = (
    el("div",{"class": x},
    ),
)

"""
    print(result)
    remove_hook(hook)

def test_py_text():
    hook = embedded_html.add_hook()
    result = embedded_html.transform_source("""
def el(*args, **kwargs):
    pass

x = "abcd"

test_html = :(
    <div>
    Some text with {x} in it.
    </div>
):
""")
    assert result == """
def el ( * args , ** kwargs ) :
    pass

x = "abcd"

test_html = (
    el("div",{},
        "Some text with " + str( x ) + " in it. ",
    ),
)

"""
    print(result)
    remove_hook(hook)

