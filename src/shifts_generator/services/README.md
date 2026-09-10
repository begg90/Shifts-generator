This folder contains a bridge between the backend and streamlit.
Streamlit does not invoke ORTools, and does not modify the data itself.
Though it does collect input data from the user.

`schedule_service.py` --> calls the solver and
post-process results

`validation.py` --> input validation, input conversion, e.g. CSV to domain models


BEA's questions:
- does `validation.py` belong to this folder or is it better suited for `utils/` or `IO/`? Perhaps the actual post-process and validation can be done here with functions that live in one of those other folders.