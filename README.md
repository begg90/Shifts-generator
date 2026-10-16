# Shifts-generator
Shifts-generator will be a webapp to generate monthly shifts for teams of physicians in a hospital ward. It can handle requirements such as personnel roles (Senior/Junior), team's temporary roles (eg. Accoglimento), personnel's temporary roles (eg. AROS), day and night shifts, mandatory off time and vacation time.
A better description will come when... Some of the actual application will be there! Even this README is a very early work in progress...

# Instructions for devs
1. uv basics
2. Clone repo & set env
3. Managing packages
4. Running scripts 
5. 
6. 
7. 
8. How to run tests


## uv basics
To install uv:
```
pip install uv 
```
To check if it's available and see the help menu with all commands, type in the terminal
```
uv  # or
uv --help
```
To see all python versions & to install specific ones (for example 3.11 & 3.12) 
```
uv python list
uv python install 3.11 3.12
```
switch to uninstall for the opposite 


## Clone repo & set env
```
git clone https://github.com/begg90/Shifts-generator
cd Shifts-generator
uv sync
```

## Managing packages

To install a new package, update the toml, the lock file & the project environment, run the following (with the --dev flag if it's for development)
```
uv add <package name>  
uv add --dev <package name>
```
Simply switch to remove to uninstall a package and remove it from all files (toml, lock) 
```
uv remove <package name>
uv remove --dev <package name>
```
This will attempt to update the specified package in the lock file to the latest compatible version, while keeping the rest of the file intact
```
uv lock --upgrade-package <package name>
```

## Running scripts
```
uv run example.py
```
It can be used to run scripts or commands in the project environment. Before the invocation, uv will verify that the lockfile is up-to-date with the toml, and that the environment is up-to-date with the lockfile, keeping the project in-sync without the need for manual intervention. uv run guarantees that the command is run in an environment with all required dependencies at their locked versions (if needed, uv sync will manually update the environment).

## Running tests
`uv run pytest` or `uv run pytest -v` or `uv run -m pytest -v`

