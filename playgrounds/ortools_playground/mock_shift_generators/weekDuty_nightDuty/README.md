# A simplified shifts generator
Here we have three possible choices for variable types/structure to feed the cp-sat solver with:
* OPTION 1: a dictionary whose keys are tuples (name, date, shift_type)
* OPTION 2: a pandas series indexed with a MultiIndex whose levels are name, date, shift_ype
* OPTION 3: a dataframe whose columns are name, date and shift_type. Name and date are the coordinates, shift_type is a new_bool_var

So far, there is an implementation for the first two.
Since the calendar and symbolic naming handling is common to both (and will be for the third too), it has been moved do a common/ folder.

The folder weekDuty_nightDuty is now a simple python package. Therefore the programs can be run with 
```
python -m weekDuty_nightDuty.with_dicts.program
```
and 
```
python -m weekDuty_nightDuty.with_pandas_series.program
```
from the root folder
```
your_path/mock_shifts_generators
```