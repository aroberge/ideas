# Developer notes

Coming back to programming after 4 years, I found that I needed to document some things that 
I thought were obvious, so that I don't spend so much time if this happens again.


## Using virtual environments

In this section we document our use of virtual environments and naming
convention; the naming convention is only useful if you wish to make use
of the existing batch file.

1. Create a virtual environment for a given Python version; for example:

        py -3.14 -m venv ./venv-ideas3.14

2. On Windows, update the ae.bat file to include this new environment. Note that
   some virtual environments are targeting a different set of installed files.
   For example, one uses iPython; another is for a special idea using units.

3. Activate the virtual environment; on Windows you can use

        ae 3.14

    Otherwise, you can presumably do something like:

        venv-ideas3.14/scripts/activate

4. Install the required dependencies for formatting, linting and testing

        python -m pip install -r requirements.txt


5. If desired, deactivate the virtual environment and create new ones for
   other Python versions

        deactivate
        py -3.12 -m venv ./venv-ideas3.12

   etc.

## Running tests

While we use pytest to run tests, it is not part of the requirements file;
therefore, it must first be installed in the desired environment,
after which we simply need to type

     pytest

in the root directory. However, this does not take into account examples that
may use different code for iPython. One such example modifies the abstract
syntax tree. It must be tested explicitly within iPython as follows:

      > ipython
      Python 3.10.11 ....  IPython 8.39.0 ...
      
      In [1]: from ideas.examples import fractions_ast
      
      In [2]: hook = fractions_ast.add_hook()
         The following initializing code from ideas is included:
      
      from fractions import Fraction
      
      In [3]: 1/3
      Out[3]: Fraction(1, 3)
