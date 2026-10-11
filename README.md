# ideas: *Making it easier to extend Python's syntax*

![ideas logo](https://raw.githubusercontent.com/aroberge/ideas/master/ideas.png)

The purpose of **ideas** is to allow you to easily implement changes in Python's syntax
and be able to see their result either when importing files using your new syntax or
in a specialized REPL, without having to change the Python code itself.


## Installation

```
python -m pip install ideas
```

Depending on your OS, you might need to write `python3` or `py` instead of `python` in the above.

## Usage

```
ideas -a my_cool_new_syntax [my_program[.py]]
```

Admitedly this is a bit terse ... Let's go into a bit more details.

### Usage in more details

As a specific example of a new syntax, suppose that you want to use
`function` as a keyword in Python, to mean
the same thing as `lambda`, enabling you to write

```python
# my_program.py

square = function x: x**2
print(f"{square(4)} is the square of 4.")

if __name__ == "__main__":
    print("This is run as the main module.")
```

You can easily do this with **ideas**.
The simplest way would be as follows:

```python
# my_cool_new_syntax.py

from ideas import create_hook

def transform(source, **kwargs):  # This will also replace lambda in strings :(
    return source.replace("function", "lambda")

def add_hook():
    create_hook(transform_source=transform, name=__main__)
```
Then to use it in an REPL, or optionally to run the python script
mentioned above, all you would need to do is:


```
ideas -a my_cool_new_syntax [my_program]
```

That's it!

Much more can be found in the [documentation](https://aroberge.github.io/ideas/docs/html/).

## Dependencies

 - [token-utils](https://github.com/aroberge/token-utils)
 - Python 3.8+  (Subject to change; it might work with older versions)

## Tools

This project uses [black](https://black.readthedocs.io/en/stable/) for formatting,
[pytest](https://docs.pytest.org/en/latest/) for running tests,
and [flake8](https://flake8.pycqa.org/en/latest/) for linting with custom
settings compatible with black.

## License

MIT

