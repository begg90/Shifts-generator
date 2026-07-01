# Shifts-generator

# Instructions 
1. Clone repo
2. Set up environment on VS Code

# Clone repo
git clone https://github.com/begg90/Shifts-generator

# Set up the environment on VS Code
## With pip
### Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
### MacOS/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## With uv (recommended)
### Windows PowerShell
uv venv .venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
### MacOS/Linux
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

VS Code might not use the correct environment right away. In that case, do
Ctrl + Shift + P --> python: Select interpreter --> <repo>/.venv/bin/python









# TO DO:
- [x] settare repo gituhb
- [ ] quando partire con la parte di interfaccia grafica
- [ ] studiare OR-tools
- [x] caricare i constraints su github
- [x] aggiungere esempio di output
- [ ] tradurre i constraints in python
- [ ] definire architettura base
