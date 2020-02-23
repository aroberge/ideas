# Todo

Infrequently updated list ...

- Mention https://www.python.org/dev/peps/pep-0511/
- Mention that files are open using utf-8 by default.
- Add requirements-dev.txt file
- List cases/recipes to be included
- Add support for `__main__`
  - something like `import_as_main(module, name_to_use=__as_main__)` ... but
    make an entry in sys.path so that two copies of this module are found,
    once under its name, and once under `__as__main__`

- use decode_source instead of straight read
  - perhaps use a custom encoding (lambda?) as an example
- use two different keywords for match: match_in and match_equal ?
- use instaviz for the docs
- using emojis as identifiers
- have a look at https://github.com/alexmojaki/nameof ... although I still don't understand the possible benefit.
- preventing automatic string concatenation; see recent discussion on python-ideas
  - tokenize, removing all space tokens and comments
  - rescan tokens, looking for two consecutive string tokens.
- pattern matching with pampy https://news.ycombinator.com/item?id=22220434
- combine codec  (ideas-encoding) and import hook in usercustomize
- multiline lambda; idea:

    command = function (x, y, z):

        some code indented more than command
    extract the code and insert into a def at the top.
    convert into a regular lambda calling that function.


- Have a look at https://tomforb.es/automatically-inline-python-function-calls/
- https://gist.github.com/dutc/0f7498451d98e3114268

- Have a look at https://mail.python.org/archives/list/python-ideas@python.org/message/CTTKN5F5UK2PUILSKEK6HAYEXZPQN5CM/ ... and https://mail.python.org/archives/list/python-ideas@python.org/message/BNEAOKFZ6OBXQMP37CLRMUPDEXAQJOCB/
