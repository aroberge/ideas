# ideas

## *Ideas: making it easier to extend Python’s syntax.*

![ideas logo](https://raw.githubusercontent.com/aroberge/ideas/master/ideas.png)


## Documentation

[Everything you need will eventually be found here](https://aroberge.github.io/ideas/docs/html/).

## Installation

> [!IMPORTANT] 
> As of August 18 2026, I've started updating this project after a 4 year hiatus.
> The version that can be installed via pypi (using pip) has not been updated yet.

```
python -m pip install ideas
```

Depending on your OS, you might need to write `python3` or `py` instead of `python` in the above.

## Dependencies

 - [token-utils](https://github.com/aroberge/token-utils)
 - Python 3.7+  (Subject to change)


## Usage

Suppose that you want to use `function` as a keyword in Python, to mean
the same thing as `lambda`, enabling you to write

```python
# my_program.py

square = function x: x**2
print(f"{square(4)} is the square of 4.")

if __name__ == "__main__":
    print("This is run as the main module.")
```

You can do this using an import hook.

The simplest (but flawed) way to create such an import hook with `ideas`
would be as follows:

```python
from ideas import import_hook

def transform(source, **kwargs):
    return source.replace("function", "lambda")

import_hook.create_hook(transform_source=transform)
```

Then, you'd need to use it. Since there is already an example import hook
that does this, we'll use it instead.  All you have to do
is instruct Python to add the import hook, and it will be used
from that point on. There are two ways to do so.

The first method would be to create a second file which adds the
required import hook and then imports your program.

```python
# Let's call this 'loader.py'

from ideas.examples import function_keyword
function_keyword.add_hook()

import my_program
```

You could then run this second file the normal way.

```
python loader.py
```

So, `my_program.py`, and any other module that could be
loaded by it would recognize that `function` is a valid alternative to `lambda`.
However, using this method, `loader` would be the `__main__` script, and
the code block defined by `if __name__ == "__main__":` in `my_program`
would be ignored.

The second way is to skip the creation of a loader, and run `my_program` directly
using `ideas`:

```
python -m ideas my_program -t function_keyword
```
This method will ensure that `my_program` is the `__main__` module.

Many more examples can be found in the [documentation](https://aroberge.github.io/ideas/docs/html/),
including a better way to create such an import hook and information about
a console (REPL) that supports code transformations.


## Tools

This project uses [black](https://black.readthedocs.io/en/stable/) for formatting,
[pytest](https://docs.pytest.org/en/latest/) for running tests,
and [flake8](https://flake8.pycqa.org/en/latest/) for linting with custom
settings compatible with black.

## License

MIT

