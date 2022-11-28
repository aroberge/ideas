import types
from ideas.examples import embedded_html
from ideas.import_hook import remove_hook

def el(name, attrs, *children):
    return [(name, attrs), *children]

def import_result(result):
    mod = types.ModuleType("test_module")
    mod.el = el
    exec(result, mod.__dict__)
    return mod

def test_single_element():
    result = embedded_html.transform_source("""
test_html = >>|<div>A Div</div>|<<
""")
    print(result)
    new_module = import_result(result)
    assert new_module.test_html == el("div", {}, "A Div")

def test_nested():
    result = embedded_html.transform_source("""
test_html = >>|
    <div>
        A Div
        with a
        <a href="http://google.com">Link</a>
    </div>
|<<
""")
    new_module = import_result(result)
    assert new_module.test_html == el("div", {}, "A Div with a ", el("a", {"href":"http://google.com"}, "Link"))

def test_py_attr():
    result = embedded_html.transform_source("""
x = "abcd"

test_html = >>|
    <div class={x}>
    </div>
|<<
""")
    new_module = import_result(result)
    assert new_module.test_html == el("div", {"class":"abcd"},)

def test_py_text():
    result = embedded_html.transform_source("""
x = "abcd"

test_html = >>|
    <div>
    Some text with {x} in it.
    </div>
|<<
""")
    new_module = import_result(result)
    assert new_module.test_html == el("div", {}, "Some text with abcd in it. ")

def test_deeper_indent():
    result = embedded_html.transform_source("""
x = "abcd"

def some_html():
    def f():
        return >>|
            <div class={x}>
            </div>
        |<<
    return f
test_html = some_html()()
    """)
    new_module = import_result(result)
    assert new_module.test_html == el("div", {"class":"abcd"},)

def test_multiple_tags():
    result = embedded_html.transform_source("""
test_html = >>|
    <div>
        <p/>
        <br/>
    </div>
|<<
    """)
    new_module = import_result(result)
    assert new_module.test_html == el("div", {}, el("p", {}), el("br", {}))