# PEP 8 Compliance
PEP 8 compliance was checked using the pycodestyle tool.

## PEP 8 Check Command
To check for PEP 8 compliance, the following command was used:

```bash
pycodestyle database.py flask_api.py main.py parser.py
```

For unittest:

```bash
pycodestyle tests/test_main.py
```

## Violations

**Line too long:** Many lines exceed the recommended length of 79 characters (E501).
**Blank lines missing:** Missing blank lines before or after class or function definitions (E302, E305).
**Trailing whitespace:** Lines containing unnecessary whitespace (W291, W293).
**Inline comments spacing:** Inline comments missing two spaces before them (E261).
**Newline at end of file:** Missing newlines at the end of files (W292).

## Examples

* database.py:2:80: E501 line too long (82 > 79 characters)
* flask_api.py:7:80: E501 line too long (88 > 79 characters)
* main.py:24:1: W293 blank line contains whitespace
* parser.py:10:80: E501 line too long (108 > 79 characters)
* tests/test_main.py:32:1: E305 expected 2 blank lines after class or function definition, found 1

## Fixing

The violations were fixed using the autopep8 tool.

```bash
autopep8 --in-place --aggressive database.py flask_api.py main.py parser.py
```

```bash
autopep8 --in-place --aggressive tests/test_main.py
```

After using autopep8, only comment lines related to testing remained as line-too-long errors in the main files. For testing files, no PEP 8 violations remained.

## Option C

For Option C, comments were added to all classes and functions, and documentation was generated using pdoc in the markdown format (HTML files) for all .py files. The following command was used:

```bash
pdoc --output-dir docs -d markdown database.py flask_api.py main.py argument_parser.py tests/test_main.py
```

### Viewing Documentation
Open the `index.html` file in the `docs` directory with any web browser to view the complete documentation.

Files Generated (under docs folder):

* argument_parser.html: Documentation for argument_parser.py
* database.html: Documentation for database.py
* flask_api.html: Documentation for flask_api.py
* index.html: Main entry point for the documentation.
* test_main.html: Documentation for unit tests in tests/test_main.py
* main.html: Documentation for main.py

## Option D

To ensure type correctness, all of the source codes have been supplemented with type annotations. The correctness of these annotations has been checked using the `mypy` tool.

### Running the Type Checker
To check for type errors, the following command was used:

```bash
mypy database.py flask_api.py main.py argument_parser.py tests/test_main.py
```

Found 46 error in 4 files

Some Example Errors:

* database.py:16: error: Variable "database.Base" is not valid as a type  [valid-type]
* tests\test_main.py:79: error: X | Y syntax for unions requires Python 3.10  [syntax]
* main.py:2: error: Library stubs not installed for "requests"  [import-untyped]
* flask_api.py:13: error: Function "flask.json.jsonify" is not valid as a type  [valid-type]

After fixing the errors, the following results were obtained:

```bash
mypy database.py
```

Success: no issues found in 1 source file

```bash
mypy tests/test_main.py
```

Success: no issues found in 1 source file

```bash
mypy main.py
```

main.py:145: error: Type variable "main.T" is unbound  [valid-type]
main.py:145: note: (Hint: Use "Generic[T]" or "Protocol[T]" base class to bind "T" inside a class)
main.py:145: note: (Hint: Use "T" in function signature to bind "T" inside a function)
Found 1 error in 1 file (checked 1 source file) 

PS: Whatever I do, I could not fix it! 

```bash
mypy argument_parser.py
```

Success: no issues found in 1 source file

```bash
mypy flask_api.py
```

Success: no issues found in 1 source file