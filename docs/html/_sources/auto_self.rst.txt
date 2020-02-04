Auto self
==========

**Concise but explicit notation to replace the often verbose**::

    self.this_variable = this_variable
    self.that_variable = that_variable
    self.this_other_variable = this_other_variable
    self.foo = foo
    self.bar = bar

    self.baz = [] if baz is None else baz
    self.spam = bread + ham




At least two possibilities::

    self.= this_variable
    self.= that_variable

or::

    $this_variable
    $that_variable

or even::

    self.= :
        this_variable
        that_variable
        this_other_variable
        foo
        bar

    self.baz = [] if baz is None else baz
    self.spam = bread + ham


Note that one could use cls instead of self.

On Python ideas, I have seen::

    self.= this_variable, that_variable, ...

which I do not find very readable.

https://stackoverflow.com/questions/3652851/what-is-the-best-way-to-do-automatic-attribute-assignment-in-python-and-is-it-a

Dataclass may already cover most of this
https://www.python.org/dev/peps/pep-0557/  ... but, they essentially require type hints.
From that PEP (but formatted with Black)::

    class Application:
        def __init__(
            self,
            name,
            requirements,
            constraints=None,
            path="",
            executable_links=None,
            executables_dir=(),
        ):
            self.name = name
            self.requirements = requirements
            self.constraints = {} if constraints is None else constraints
            self.path = path
            self.executable_links = [] if executable_links is None else executable_links
            self.executables_dir = executables_dir
            self.additional_items = []

would become::

    class Application:
        def __init__(
            self,
            name,
            requirements,
            constraints=None,
            path="",
            executable_links=None,
            executables_dir=(),
        ):
            self.=:
                name
                requirements
                path
                executable_dir

            self.constraints = {} if constraints is None else constraints
            self.executable_links = [] if executable_links is None else executable_links
            self.additional_items = []

compared with::

    @dataclass
    class Application:
        name: str
        requirements: List[Requirement]
        constraints: Dict[str, str] = field(default_factory=dict)
        path: str = ''
        executable_links: List[str] = field(default_factory=list)
        executable_dir: Tuple[str] = ()
        additional_items: List[str] = field(init=False, default_factory=list)
