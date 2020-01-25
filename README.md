# ideas
Easy creation of custom import hooks to try out new ideas for Python.

## About the name

For this project, I was thinking of using `importhook` (singular),
but there is already a project with that name on pypi.
I was tempted to use `importhooks` (plural), but decided that it might
be too confusing.

I settle on `ideas` as I am guessing that the main application would be
for people to try out suggestions from python-ideas.

## Original motivation


As I find myself doing a lot of copy/paste/modify on the various import
hooks experiments, including on some published projects such as AvantPy,
I thought it would make sense to create a versatile projects which I could
use as the basis of other projects.  An obvious benefit is that I will
need to fix bugs in a single project.

### Additional motivation

Often, on python-ideas, a suggestion is made to someone that proposes something
new to try it by modifying Python using an import hook.
I have yet to see a case of someone following up on that idea.
I believe that the main reason is that most people do not know how to
do this.

So, by creating this project, I'm hoping that enough examples will
be created that could be easily adapted for exploring proposals
submitted to python-ideas.


## Tools

This project uses black for formatting, pytest for running tests,
and flake8 for linting.


## To Do

- Add requirements-dev.txt file
- Add setup.py file and upload to pypi
- List cases/recipes to be included
- Add console
- Add docs
- Add support for `__main__`
- Add test to ensure desired paths (e.g. Python standard library) are excluded.


More to come ...
