# SIMPLIFIED SENIOR AND JUNIOR DOCTORS SHIFT
# each day there are TWO shifts: a day shift and a night shift
# juniors work the day shift, seniors work the night shift                      ---> valid_combos()
# there is a 30 days period schedule

# constraints that are valid for both shift types:
# each shift is done by 1 doctor                                                ---> constraint: one_employee_per_shift()
# the workload is evenly distributed                                            ---> (1) distribute_senior_workload()
#                                                                                    (2) distribute_dutyWeek_workload()

# constraints that are valid for the day shift only:
# junior doctors work Monday to Saturday included, hence six consecutive days.                  ---> constraint: assign_weekDuty()
# sunday is a rest day for all junior doctors (Sundays will become dayDuty in a later version). ---> valid_combos()
# junior doctors do not work consecute shifts                                                   ---> forbid_consecutive_dutyWeek()
# not more than 2 dutyWeeks per month                                                           ---> ? DO NOT DO YET
# The one in the previous line does not prevent assigning 2 weeks to 2 people
# and leaving a 3rd unassigned. Hence, we need a distribution of workload.
# We probably don't need a "no more than 2 weeks per month" constraint because there are 4 weeks.
# Though, it is good to look at exceptions of 5 weeks long months and how it combines with this handling of the planning

# constraints that are valid for the night shift only:
# senior doctors do not work consecutive shifts                                 ---> forbid_consecutive_nightDuty()

# in this example the variables are saved in a dictionary


from ortools.sat.python import cp_model
from ortools.sat.python import cp_model_helper
from time_organizer import my_calendar

# constant parameters that should belong to an enums kind of section
SENIOR = 0 # not sure we need them as enums, though
JUNIOR = 1

def get_data():
    doctors = [{"name":"eenie","seniority":SENIOR},
            {"name":"miney","seniority":SENIOR},
            {"name":"meenie","seniority":SENIOR},
            {"name":"moe","seniority":SENIOR},
            {"name":"tom","seniority":SENIOR},
            {"name":"jerry","seniority":SENIOR},
            {"name":"schiavo1","seniority":JUNIOR},
            {"name":"schiavo2","seniority":JUNIOR},
            {"name":"schiavo3","seniority":JUNIOR}]

    shift_types = ["dutyWeek","nightDuty"]
    # calendar
    year = 2026
    month = 9
    senior_cal = my_calendar(year,month)
    junior_cal = my_calendar(year,month)
    senior_cal.get_month_asstrings()
    senior_cal.month_cleanup()
    junior_cal.get_weeks_asstrings()
    junior_cal.weeks_cleanup()
    junior_cal.weeks_removeSundays()
    junior_cal.get_month_asstrings()
    junior_cal.month_cleanup()
    junior_cal.month_removeSundays()
    return doctors, senior_cal, junior_cal, shift_types


def seniority(doctors):
    juniors = [doc["name"] for doc in doctors if doc["seniority"] == JUNIOR]
    seniors = [doc["name"] for doc in doctors if doc["seniority"] == SENIOR]
    return juniors, seniors

def valid_combos(doctors,senior_month,junior_month,shift_types):
    # NB: not a fan of this solution because combos cannot be accessed with readable keys but with indices
    juniors,seniors = seniority(doctors)
    # careful: combos must be hashable and lists aren't.
    combos = ([(doc,date,shift_types[0]) for doc in juniors for date in junior_month] + 
              [(doc,date,shift_types[-1]) for doc in seniors for date in senior_month])
    return combos

class scheduled_model(cp_model.CpModel):

    def __init__(self, doctors,senior_cal,work_weeks,shift_types,combos): 
        cp_model.CpModel.__init__(self)
        self._doctors = doctors
        self._senior_dates = senior_cal
        self._work_weeks = work_weeks
        self._index = combos
        self._shift_types = shift_types
        self.shifts = {}
        self.dutyWeek = {} # this one could even be _dutyWeek

    def create_variables(self):
        for combo in self._index:
            self.shifts[combo] = self.new_bool_var(f"shift_{combo[0]}_day{combo[1][0]}_{combo[2]}")
        juniors,s = seniority(self._doctors)
        for doc in juniors:
            for week in self._work_weeks:
                self.dutyWeek[(doc,week)] = self.new_bool_var(f"dutyWeek_{doc}_{self._work_weeks.index(week)}")      
        return self.shifts,self.dutyWeek

    def one_employee_per_nightDuty(self):
        #constraint
        j,seniors = seniority(self._doctors)
        for day in self._senior_dates:
            # keep who_can_work for future FREE days
            who_can_work = [
                self.shifts[doc,day,self._shift_types[1]] for doc in seniors if (doc,day,self._shift_types[1]) in self._index
            ]
            self.add_exactly_one(who_can_work)
        return
    
    def one_employee_per_dutyWeek(self):
            #constraint
            juniors,s = seniority(self._doctors)
            for week in self._work_weeks:
                who_can_work = [self.dutyWeek[doc,week] for doc in juniors]
                self.add_exactly_one(who_can_work)
            return
    
    def forbid_consecutive_nightDuty(self):
        # constraint
        # seniors cannot work consecutive night shifts
        j,seniors = seniority(self._doctors)
        for doc in seniors:
            for day in range(len(self._senior_dates)-1):
                self.add_at_most_one([self.shifts[doc,self._senior_dates[day],"nightDuty"], 
                                      self.shifts[doc,self._senior_dates[day+1],"nightDuty"]])
        return

    def assign_dutyWeek(self):
        # constraint
        # juniors work six consecutive days of duty, i.e. a dutyWeek
        juniors,s = seniority(self._doctors)    
        for doc in juniors:
            for week in self._work_weeks:
                for date in week:
                    self.add(self.shifts[doc,date,"dutyWeek"] == 1).only_enforce_if(self.dutyWeek[doc,week])
        return

    def forbid_consecutive_dutyWeek(self):
        # constraint
        # juniors cannot work consecutive duty weeks
        juniors,s = seniority(self._doctors)
        for doc in juniors:
            for n in range(len(self._work_weeks)-1):
                self.add_at_most_one([self.dutyWeek[(doc, self._work_weeks[n])], self.dutyWeek[(doc, self._work_weeks[n+1])]])
        return

    def distribute_nightDuty_workload(self):
        j,seniors = seniority(self._doctors)
        # NOT a nice solution, definitely NOT general
        # e.g. as soon as vacation days are included, this does not work anymore
        total_shifts = sum(1 for combo in self._index if combo[0] == seniors[0]) # look at one senior only. Extra ugly solution.
        min_shifts_per_doctor = total_shifts // len(seniors)
        if total_shifts % len(seniors) == 0:
            max_shifts_per_doctor = min_shifts_per_doctor
        else:
            max_shifts_per_doctor = min_shifts_per_doctor + 1
        for doc in seniors:
            shifts_worked = sum( 
                self.shifts[(doc,day,shift)] 
                for day in self._senior_dates
                for shift in self._shift_types
                if (doc,day,shift) in self._index
            )    
            self.add(min_shifts_per_doctor <= shifts_worked)     
            self.add(shifts_worked <= max_shifts_per_doctor)
        return    

    def distribute_dutyWeek_workload(self):
        juniors,s = seniority(self._doctors)
        total_shifts = len(self._work_weeks)
        print(total_shifts)
        min_shifts_per_doctor = total_shifts // len(juniors)
        print(min_shifts_per_doctor)
        if total_shifts % len(juniors) == 0:
            max_shifts_per_doctor = min_shifts_per_doctor
        else:
            max_shifts_per_doctor = min_shifts_per_doctor + 1
        print(max_shifts_per_doctor)
        for doc in juniors:
            shifts_worked = sum( 
                self.shifts[(doc,day,shift)]
                for day in self._senior_dates
                for shift in self._shift_types
                if (doc,day,shift) in self._index
            )
            self.add(min_shifts_per_doctor * 6 <= shifts_worked)     
            self.add(shifts_worked <= max_shifts_per_doctor * 6) # could this be worse? Doubt it
        return

class doctorsPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, shifts, doctors, senior_cal, shift_types, combos, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._doctors = doctors
        self._dates = senior_cal
        self._index = combos
        self._shift_types = shift_types
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        # TO DO: change this for better visualization
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for day in self._dates:
            print(f"Day {day}")
            for doc in self._doctors:
                is_working = False
                for shift in self._shift_types:
                    if (doc["name"],day,shift) in self._index:
                        if self.value(self._shifts[(doc["name"],day,shift)]):
                            is_working = True
                            print(f"Doctor {doc["name"]} works {shift}")
                        if not is_working:
                            print(f"Doctor {doc["name"]} does not work {shift}")
                    #else:
                    #    print(f"ELSE Doctor {doc["name"]} does not work")


        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.stop_search()
    
    def solutionCount(self):
        return self._solution_count
        


def main() -> None:
    # data
    doctors, senior_cal, junior_cal, shift_types = get_data()
    # create index 
    combos = valid_combos(doctors,senior_cal.month,junior_cal.month,shift_types)
    # create model
    model = scheduled_model(doctors,senior_cal.month,junior_cal.weeks,shift_types,combos)
    model.create_variables()
    model.one_employee_per_nightDuty()
    model.one_employee_per_dutyWeek()
    model.forbid_consecutive_nightDuty()
    model.assign_dutyWeek()
    model.distribute_nightDuty_workload()
    model.distribute_dutyWeek_workload()
    #print(model)

    # create model
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # enumerate all solutions
    solver.parameters.enumerate_all_solutions = True

    # Display the first five solutions.
    solution_limit = 5
    solution_printer = doctorsPartialSolutionPrinter(
        model.shifts, doctors, senior_cal.month, shift_types, combos, solution_limit)

    # invoke the solver
    status = solver.solve(model, solution_printer)
    #print(status)


if __name__ == "__main__":
    main()