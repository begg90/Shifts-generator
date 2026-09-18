# SIMPLIFIED SENIOR DOCTORS SHIFT
# each day there is ONE shift (a night shift)
# each shift is done by 1 doctor
# doctors do not work consecutive shifts
# there is a 30 days period schedule
# the workload is evenly distributed

# in this example the variables are saved in a dictionary

from ortools.sat.python import cp_model
#from ortools.sat.python import cp_model_helper

def get_data():
    doctors = ["eenie",
            "meenie",
            "miney",
            "moe",
            "tom",
            "jerry"]
    shift_types = ["NightDuty"]
    num_days = 30 # to mimic a month
    dates = list(range(num_days)) # NB this goes from 0, NOT like a calendar
    return doctors, dates, shift_types

class scheduled_model(cp_model.CpModel):
    """our model including variables and constraints"""
    def __init__(self, doctors, dates, shift_types):
        cp_model.CpModel.__init__(self)
        self._doctors = doctors
        self._dates = dates
        self._shift_types = shift_types
        self.shifts = {}

    def create_variables(self):
        # a dictionary for now, a pandas series later
        for doc in self._doctors:
            for day in self._dates:
                for shift in self._shift_types:
                    self.shifts[(doc,day,shift)] = self.new_bool_var(f"shift_{doc}_day{day}_{shift}")
        return self.shifts
    
    def one_employee_per_shift(self):
        #constraint
        for day in self._dates:
            for shift in self._shift_types:
                self.add_exactly_one(self.shifts[doc,day,shift] for doc in self._doctors)
        return

    def forbid_consecutive_shifts(self):
        # constraint
        for doc in self._doctors:
            for shift in self._shift_types:
                for day in range(len(self._dates)-1):
                    self.add_at_most_one([self.shifts[doc,self._dates[day],shift],self.shifts[doc,self._dates[day+1],shift]])
        return            

    def evenly_distribute_workload(self):
        # constraint
        min_shifts_per_doctor = (len(self._dates) * len(self._shift_types)) // len(self._doctors)
        if len(self._dates) * len(self._shift_types) % len(self._doctors) == 0:
            max_shifts_per_doctor = min_shifts_per_doctor
        else:
            max_shifts_per_doctor = min_shifts_per_doctor + 1
        for doc in self._doctors:
            shifts_worked = []
            for day in self._dates:
                for shift in self._shift_types:
                    shifts_worked.append(self.shifts[((doc,day,shift))])
            self.add(min_shifts_per_doctor <= sum(shifts_worked))     
            self.add(sum(shifts_worked) <= max_shifts_per_doctor)
        return    


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
        for day in self._dates:
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




def main() -> None:
    # data
    [doctors,dates,shift_types] = get_data()
    # create model
    model = scheduled_model(doctors, dates, shift_types)
    model.create_variables()
    model.one_employee_per_shift()
    model.forbid_consecutive_shifts()
    model.evenly_distribute_workload()
    
    # create model
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # enumerate all solutions
    solver.parameters.enumerate_all_solutions = True

    # Display the first five solutions.
    solution_limit = 5
    solution_printer = doctorsPartialSolutionPrinter(
        model.shifts, doctors, dates, shift_types, solution_limit)

    # invoke the solver
    solver.solve(model, solution_printer)


if __name__ == "__main__":
    main()