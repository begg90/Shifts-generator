# Shifts-generator
Shifts-generator will be a webapp to generate monthly shifts for teams of physicians in a hospital ward. It can handle requirements such as personnel roles (Senior/Junior), team's temporary roles (eg. Accoglimento), personnel's temporary roles (eg. AROS), day and night shifts, mandatory off time and vacation time.
A better description will come when... Some of the actual application will be there! Even this README is a very early work in progress...

# Instructions for devs
1. Clone repo
2. Set up environment on VS Code

## Clone repo
```
git clone https://github.com/begg90/Shifts-generator
cd Shifts-generator
```

## Set up the environment on VS Code
### With pip
#### Windows PowerShell
```
python3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
#### MacOS/Linux
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### With uv (recommended)
#### Windows PowerShell
```
uv venv .venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```
#### MacOS/Linux
```
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

VS Code might not use the correct environment right away. In that case, do
Ctrl + Shift + P --> python: Select interpreter --> <repo>/.venv/bin/python

## Running tests
`python -m pytest -v` or `pytest -v`


## Troubleshooting
If pytest doesn not find src/, activate python.terminal.useEnvFile in VS Code (File --> Preferences --> Settings --> type python.terminal.useEnvFile and select it)