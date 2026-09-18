# nurses shifts
# each day there are 3 shifts of 8 hours
# each shift is done by 1 nurse
# no nurse works more than 1 shift per day
# there is a 3 days period schedule

from ortools.sat.python import cp_model
# from ortools.sat.python import cp_model_helper ## is this the helper for this package?

# Data
num_nurses = 4
num_shifts = 3
num_days = 3
all_nurses = range(num_nurses)
all_shifts = range(num_shifts)
all_days = range(num_days)

# create model
model = cp_model.CpModel()

# create variables
shifts = {} # a dictionary, then
for n in all_nurses:
    for d in all_days:
        for s in all_shifts:
            shifts[(n,d,s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")
# ie: key (n,d,s) of dictionary shifts has value model.new_bool_var(f"shift_n{n}_d{d}_s{s}")
# each key has a boolean value type which is 1 (true) if that shift on that day is assigned to that nurse.

# assign nurses to shifts, with rules
# 1. each shift is assigned to a single nurse
# 2. each nurse works at most one shift per day

# Constraint: assign each shift to a single nurse
for d in all_days:
    for s in all_shifts:
        model.add_exactly_one(shifts[(n,d,s)] for n in all_nurses)

# Constraint: each nurse works at most one shift per day
for n in all_nurses:
    for d in all_days:
        model.add_at_most_one(shifts[(n,d,s)] for s in all_shifts)

# Constraint: the shifts are evenly ditributed among nurses
min_shifts_per_nurse = (num_days * num_shifts) // num_nurses
if num_days * num_shifts % num_nurses == 0:
    max_shifts_per_nurse = min_shifts_per_nurse
else:
    max_shifts_per_nurse = min_shifts_per_nurse + 1
for n in all_nurses:
    shifts_worked = []
    for d in all_days:
        for s in all_shifts:
            shifts_worked.append(shifts[((n,d,s))])
    model.add(min_shifts_per_nurse <= sum(shifts_worked)) # this is added for each n. Does it create an independent constrain for each n?     
    model.add(sum(shifts_worked) <= max_shifts_per_nurse)  

# update solver parameters
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# enumerate all solutions
solver.parameters.enumerate_all_solutions = True

# register a solution callback (on the solver!)
class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """print intermediate solutions"""

    def __init__(self, shifts, num_nurses, num_days, num_shifts, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for d in range(self._num_days):
            print(f"Day {d}")
            for n in range(self._num_nurses):
                is_working = False
                for s in range(self._num_shifts):
                    if self.value(self._shifts[(n,d,s)]):
                        is_working = True
                        print(f"Numers {n} works shift {s}")
                if not is_working:
                    print(f"Nurse {n} does not work")
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.stop_search()
    
    def solutionCount(self):
        return self._solution_count

# Display the first five solutions.
solution_limit = 5
solution_printer = NursesPartialSolutionPrinter(
    shifts, num_nurses, num_days, num_shifts, solution_limit)

# invoke the solver
solver.solve(model, solution_printer)