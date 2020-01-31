# ideas
Easy creation of custom import hooks to try out new ideas for Python.

![ideas logo](ideas.png)


[Documentation](https://aroberge.github.io/ideas/docs/html/)

## Original motivation

Programming in Python is my main hobby. I like to explore various
ideas, learning along the way.
As I find myself doing a lot of copy/paste/modify on the various import
hooks experiments, including on some published projects such as
[AvantPy](https://aroberge.github.io/avantpy/docs/html/),
I thought it would make sense to create a versatile projects which I could
use as the basis of other projects.  An obvious benefit is that I will
need to fix bugs in a single project.

### Additional motivation

Often, on python-ideas, a suggestion is made to someone that proposes something
new to try it by modifying Python using an import hook.
I have yet to see a case of someone following up on such suggestions.
I believe that the main reason is that most people do not know how to
do this.

So, by creating this project, I'm hoping that enough examples will
be created that could be easily adapted for exploring proposals
submitted to python-ideas. If that is the case, I will likely benefit
too as advanced Python programmers may make suggestions as to how
to improve this project.

## About the name

For this project, I was thinking of using `importhook` (singular) or
`importhooks` (plural). However, there is already a project named
`importhook` on Pypi and I thought that using the plural form would
likely be just too confusing.

I settled on `ideas` as I am guessing that the main application would be
for people to try out suggestions from or for python-ideas.

## Tools

This project uses black for formatting, pytest for running tests,
and flake8 for linting.


## To Do

- Add requirements-dev.txt file
- List cases/recipes to be included
- Add console
- Add support for `__main__`
  - something like `import_as_main(module, name_to_use=__as_main__)` ... but
    make an entry in sys.path so that two copies of this module are found,
    once under its name, and once under `__as__main__`
- Add test to ensure desired paths (e.g. Python standard library) are excluded.
- show excluded path
- show abbreviations used for paths
- always exclude ideas itself
- add line tokenizer
- add space preserving tokenizer
- add utils.Token with many methods including `is_identifier`, `is_keyword`,
  `is_operator(optional_string)`
- have a tokenizing option to remove all string contents and strip comments.
- use decode_source instead of straight read
  - perhaps use a custom encoding (lambda?) as an example
- use two different keywords for match: match_in and match_equal ?
- use instaviz



More to come ...
