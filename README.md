# Shifts-generator
Shifts-generator will be a webapp to generate monthly shifts for teams of physicians in a hospital ward. It can handle requirements such as personnel roles (Senior/Junior), team's temporary roles (eg. Accoglimento), personnel's temporary roles (eg. AROS), day and night shifts, mandatory off time and vacation time.
A better description will come when... Some of the actual application will be there! Even this README is a very early work in progress...

# Instructions for devs
1. uv basics
2. Clone repo & set env
3. Managing packages
4. Running scripts 
5. Ruff commands
6. Running the type checker
7. How to run tests


## uv basics
To install uv:
```
pip install uv 
```
To check if it's available and see the help menu with all commands (there's also a --help flag, but it works either way):
```
uv 
```
To see all python versions & to install or uninstall specific ones (for example 3.11 & 3.12) 
```
uv python list
uv python install 3.11 3.12
uv python uninstall 3.11 3.12
```

## Clone repo & set env
```
git clone https://github.com/begg90/Shifts-generator
cd Shifts-generator
uv sync
```

## Managing packages

To install a new package, update the toml, the lock file & the project environment (with the --dev flag if it's for development)
```
uv add <package name>  
uv add --dev <package name>
```
To uninstall a package and remove it from all files 
```
uv remove <package name>
uv remove --dev <package name>
```
`uv lock` will attempt to update the specified package in the lock file to the latest compatible version, while keeping the rest of the file intact
```
uv lock --upgrade-package <package name>
```
To update all packages:
```
uv lock --upgrade
```

## Running scripts
```
uv run <file_name>.py
```
It can be used to run scripts or commands in the project environment. Before the invocation, uv will verify that the lockfile is up-to-date with the toml, and that the environment is up-to-date with the lockfile, keeping the project in-sync without the need for manual intervention. uv run guarantees that the command is run in an environment with all required dependencies at their locked versions (if needed, uv sync will manually update the environment).

## Ruff commands
Best practice: run both linter & formatter before a pull. 
To run the Ruff linter over the entire project or on a specified script
```
uv run ruff check
uv run ruff check src/file.py
```
To resolve the issues automatically 
```
uv run ruff check --fix
```
To run the Ruff formatter on the project or on a script
```
uv run ruff format
uv run ruff format src/file.py
``` 

### Ignoring errors
If there is a line that needs to ignore the lint rules, add a # noqa comment next to it. For example:
```
from typing import Iterable  # noqa
```
It can be specified which rule to ignore:
```
from typing import Iterable  # noqa: UP035
```
The same can be applied to an entire script, by adding the following line at the beginning of a file: 
```
# ruff: noqa: UP035
```
## Running the type checker
To run Pyrefly over the project
```
uv run pyrefly check
```
or over a file
```
uv run pyrefly check <file_name>
```
### Ignoring errors
To ignore errors by line, type 
```
# pyrefly: ignore[<error)type>] # <brief explanation for other devs>
```
next to the interested line. To ignore all errors in a file, type
```
# pyrefly: ignore-errors
```
at the very begginning of the file.

Type checking can be disabled in sub-folders. Modify the .toml by creating a sub-group
```
[[tool.pyrefly.sub-config]]
matches = "<folder_name>/**"
```
and disabling specific errors
```
[tool.pyrefly.sub-config.errors]
<error_type> = false
```
The errors of the whole codeline can be ignored with 
```
uv run pyrefly suppress
```
This will place  suppression comments on the line before each error. Alternatively, these errors can be saved in a baseline file and Pyrefly will automatically ignore them.
See the Pyrefly documentation for further instructions.
### Automatic type annotation
Pyrefly can infer type of unannotated code by the way it is used in the current codebase. This should not replace manual review or manual annotation, as the method is experimental and it relies entirely on the current code rather than on the intention behind it. To use this tool, type
```
uv run pyrefly infer <path_to_file>
```
or
```
uv run pyrefly infer <path_to_folder>
```
### Other tools
Pyrefly can measure how much the code is annotated with types, which can be used in CI if it falls under a treshold. 
Pyrefly can also generate stubs files for new modules, provided the code is fully annotated. We could use both tools in the future, this is a written reminder.
## Running tests
`uv run pytest` or `uv run pytest -v` or `uv run -m pytest -v`

