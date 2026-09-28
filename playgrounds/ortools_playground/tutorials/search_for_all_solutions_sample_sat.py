"""simple solve"""
from ortools.sat.python import cp_model
from ortools.sat.python import cp_model_helper

"""
VarArraySolutionPrinter MUST inherit from cp_model.CpSolverSolutionCallback.
You can customize what info you want in your callback. Here there is a function that prints
all variables values (NOTE: variables are IntVar. Does not work with boolean variables, probably)
and counts the solutions.
A second solution that is decorated with property returns the solution count.
The name function on_solution_callback is mandatory because it is an attribute of cp_model.CpSolverSolutionCallback

solver.parameters.enumerate_all_solutions = True : this should be enabled
solve() now expects TWO parameters, solve(model, CpSolverSolutionCallback_obj)

Questions:
- Is there something available in cp_model.CpSolverSolutionCallback or must it be 100% customized?
"""

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v} = {self.value(v)}", end = " ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count


def search_for_all_solutions_sample_sat():
    """showcase calling the solver to show all solutions"""
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
    solution_printer = VarArraySolutionPrinter([x,y,z])
    # enumerate all solutions
    solver.parameters.enumerate_all_solutions = True
    # solve
    status = solver.solve(model, solution_printer)

    print(f"status =  {solver.status_name(status)}")
    print(f"number of solutions found = {solution_printer.solution_count}")


search_for_all_solutions_sample_sat()