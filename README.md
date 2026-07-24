# Shifts-generator
Shifts-generator will be a webapp to generate monthly shifts for teams of physicians in a hospital ward. It can handle requirements such as personnel roles (Senior/Junior), team's temporary roles (eg. Accoglimento), personnel's temporary roles (eg. AROS), day and night shifts, mandatory off time and vacation time.
A better description will come when... Some of the actual application will be there! Even this README is a very early work in progress...

# Instructions for devs
1. Clone repo
2. (Recommended) Set up environment on VS Code
3. Install package
4. (Optional) Install dev tools
5. (Optional) Install webapp tools
6. How to update local environment
7. How to run tests

## Clone repo
```
git clone https://github.com/begg90/Shifts-generator
cd Shifts-generator
```

## Set up the environment on VS Code
This is recommended to devs who need to install dev tools.
### With pip
#### Windows PowerShell
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```
#### MacOS/Linux
```
python -m venv .venv
source .venv/bin/activate
```

### With uv
#### Windows PowerShell
```
uv venv .venv
.venv\Scripts\Activate.ps1
```
#### MacOS/Linux
```
uv venv .venv
source .venv/bin/activate
```
VS Code might not use the correct environment right away. In that case, do
Ctrl + Shift + P --> python: Select interpreter --> <repo>/.venv/

## Install package
```
pip install -e . 
```
or
```
uv pip install -e . 
```

## Install dev tools
```
pip install -r dev-requirements.txt
```
or
```
uv pip install -r dev-requirements.txt
```

## Install webapp tools
```
pip install -r requirements.txt
```
or
```
uv pip install -r requirements.txt
```

## Running tests
`pytest` or `pytest -v` or `python -m pytest -v`

## How to update local enviroment
New packages need to be added to the project depending on their use.
Dependencies used in the backend must be added to the ```.toml``` file. Dependencies used in the webapp must be added to ```requirements.txt```. Dependencies that are dev tools must be added to ```dev-requirements.txt```

## How to deactivate the virtual environment
Simply write 
 ```   deactivate ```
into the terminal.