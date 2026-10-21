# ruff: noqa

import pandas as pd

def create_solution_dataframe(solution:pd.Series, shift_type):
        shifts = solution.xs(shift_type, level = "shift_type")
        rows = []
        for (doc,date), shift_value in shifts.items():
            if shift_value:
                rows.append({"date": date, "doc": doc,})

        return pd.DataFrame(rows).sort_values("date")


# TO DO:
# create an interface that has solution and shift_type as paramenters, 
# and create_solution_dataframe as method.
# than create two classes, one for the dict and one for the series solution 
# that have a create_solution_dataframe method 
# after that, the plotting is the same for each program

# Q: do we need it, really?