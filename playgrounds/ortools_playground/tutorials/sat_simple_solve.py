"""simple solve"""
from ortools.sat.python import cp_model
from ortools.sat.python import cp_model_helper

def simple_sat_program():
    """minimal CP-SAT example"""
    # create the model
    model = cp_model.CpModel()

    # create the variables
    num_vals = 3
    L = 0 
    R = num_vals - 1
    x = model.new_int_var(L, R, "x")
    y = model.new_int_var(L, R, "y")
    z = model.new_int_var(L, R, "z")

    # create constrains
    model.add(x != y)

    # create solver
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("no solution found")

simple_sat_program()


