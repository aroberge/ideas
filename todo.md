# Todo

Infrequently updated list ...

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
- use instaviz for the docs

