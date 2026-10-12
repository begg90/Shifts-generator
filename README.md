# Shifts-generator
Shifts-generator will be a webapp to generate monthly shifts for teams of physicians in a hospital ward. It can handle requirements such as personnel roles (Senior/Junior), team's temporary roles (eg. Accoglimento), personnel's temporary roles (eg. AROS), day and night shifts, mandatory off time and vacation time.
A better description will come when... Some of the actual application will be there! Even this README is a very early work in progress...

# Instructions for devs
1. Clone repo
2. Checking uv
3. Checking python versions
4. Install package 
5. Uninstall package
6. Update a package
7. Running scripts
8. How to run tests

## Clone repo
```
git clone https://github.com/begg90/Shifts-generator
cd Shifts-generator
```

## Checking uv
To check that uv is available, and see the help menu with all available commands, type in the terminal
```
uv 
```
## Checking python versions
To see all python versions and those available
```
uv  python list
```
to install a specific version (for example 3.11 & 3.12) 
```
uv python install 3.11 3.12
```
switch to unistall for the opposite 

## Install package

To install a new package, update the toml, the lock file & the project environment:
```
uv add <package name>  
```
If it's only for the development of the project, it can include the flag:

```
uv add --dev <package name>
```
## Uninstall package

Simply exchange add with remove to unistall a package and remove it from all files (toml, lock) 
```
uv remove <package name>
uv remove --dev <package name>
```

## Update a package 
```
uv lock --upgrade-package <package name>
```
This will attempt to update the specified package to the latest compatible version, while keeping the rest of the lockfile intact.


## Running scripts
```
uv run example.py
```
It can be used to run scripts or commands in the project environment. Before the invocation, uv will verify that the lockfile is up-to-date with the toml, and that the environment is up-to-date with the lockfile, keeping the project in-sync without the need for manual intervention. uv run guarantees that the command is run in an environment with all required dependencies at their locked versions ( if needed, we can use uv sync to manually update the environment).

## Running tests
`pytest` or `pytest -v` or `python -m pytest -v`

