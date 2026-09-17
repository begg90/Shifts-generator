# SIMPLIFIED SENIOR DOCTORS SHIFT
# each day there is ONE shift (a night shift)
# each shift is done by 1 doctor
# doctors do not work consecutive shifts
# there is a 30 days period schedule
# the workload is evenly distributed

# in this example the variables are saved in a dictionary

from ortools.sat.python import cp_model
#from ortools.sat.python import cp_model_helper

# Data
doctors = ["eenie",
           "meenie",
           "miney",
           "moe",
           "tom",
           "jerry"]
shift_types = ["NightDuty"]
num_days = 30 # to mimic a month
dates = list(range(num_days)) # NB this goes from 0, NOT like a calendar

# CREATE MODEL
model = cp_model.CpModel()
model.clear_assumptions

# CREATE VARIABLES
# a dictionary for now, a pandas series later
shifts = {}
for doc in doctors:
    for day in dates:
        for shift in shift_types:
            shifts[(doc,day,shift)] = model.new_bool_var(f"shift_{doc}_day{day}_{shift}")

#print(shifts)

# CREATE CONSTRAINTS
# assign doctors to shifts, with rules:
# 1. each shift is assigned to a single doctor
# 2. no doctor works consecutive days

# Constraint: assign each shift to a single doctor
for day in dates:
    for shift in shift_types:
        model.add_exactly_one(shifts[doc,day,shift] for doc in doctors)
#print(model)

# Constraint: doctors do not work consecutive shifts
for doc in doctors:
    for shift in shift_types:
        for day in range(len(dates)-1):
            model.add_at_most_one([shifts[doc,dates[day],shift],shifts[doc,dates[day+1],shift]])
#print(model)

# Constraint: the shifts are evenly ditributed among doctors
min_shifts_per_doctor = (len(dates) * len(shift_types)) // len(doctors)
if len(dates) * len(shift_types) % len(doctors) == 0:
    max_shifts_per_doctor = min_shifts_per_doctor
else:
    max_shifts_per_doctor = min_shifts_per_doctor + 1
for doc in doctors:
    shifts_worked = []
    for day in dates:
        for shift in shift_types:
            shifts_worked.append(shifts[((doc,day,shift))])
    model.add(min_shifts_per_doctor <= sum(shifts_worked))     
    model.add(sum(shifts_worked) <= max_shifts_per_doctor)
#print(model)

# CREATE SOLVER
# update solver parameters
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# enumerate all solutions
solver.parameters.enumerate_all_solutions = True

# register a solution callback
class doctorsPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """print intermediate solutions"""

    def __init__(self, shifts, doctors, dates, shift_types, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._doctors = doctors
        self._dates = dates
        self._shift_types = shift_types
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for day in dates:
            print(f"Day {day}")
            for doc in self._doctors:
                is_working = False
                for shift in self._shift_types:
                    if self.value(self._shifts[(doc,day,shift)]):
                        is_working = True
                        print(f"Doctor {doc} works shift {shift}")
                if not is_working:
                    print(f"doctor {doc} does not work")
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.stop_search()
    
    def solutionCount(self):
        return self._solution_count


# Display the first five solutions.
solution_limit = 5
solution_printer = doctorsPartialSolutionPrinter(
    shifts, doctors, dates, shift_types, solution_limit)

# INVOKE THE SOLVER
solver.solve(model, solution_printer)