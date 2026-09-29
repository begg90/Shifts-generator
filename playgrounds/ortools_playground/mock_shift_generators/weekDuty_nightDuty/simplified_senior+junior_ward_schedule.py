# SIMPLIFIED SENIOR AND JUNIOR DOCTORS SHIFT
# each day there are TWO shifts: a day shift and a night shift
# juniors work the day shift, seniors work the night shift                      ---> valid_combos()
# there is a 30 days period schedule

# constraints that are valid for both shift types:
# each shift is done by 1 doctor                                                ---> constraint: one_employee_per_shift()
# the workload is evenly distributed                                            ---> (1) distribute_senior_workload()
#                                                                                    (2) distribute_dutyWeek_workload()

# constraints that are valid for the day shift only:
# junior doctors work Monday to Saturday included, hence six consecutive days.                  ---> constraint: assign_dutyWeek()
# sunday is a rest day for all junior doctors (Sundays will become dayDuty in a later version). ---> valid_combos()
# junior doctors do not work consecute shifts                                                   ---> forbid_consecutive_dutyWeek()
# not more than 2 dutyWeeks per month                                                           ---> ? DO NOT IMPLEMENT: redundant
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
from local_enums import SeniorityLevel, ShiftList

# constant parameters that should belong to an enums kind of section

def get_data():
    doctors = [{"name":"eenie","seniority":SeniorityLevel.SENIOR.name},
               {"name":"meenie","seniority":SeniorityLevel.SENIOR.name},
               {"name":"miney","seniority":SeniorityLevel.SENIOR.name},
               {"name":"moe","seniority":SeniorityLevel.SENIOR.name},
               {"name":"tom","seniority":SeniorityLevel.SENIOR.name},
               {"name":"jerry","seniority":SeniorityLevel.SENIOR.name},
               {"name":"schiavo1","seniority":SeniorityLevel.JUNIOR.name},
               {"name":"schiavo2","seniority":SeniorityLevel.JUNIOR.name},
               {"name":"schiavo3","seniority":SeniorityLevel.JUNIOR.name}]

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
    return doctors, senior_cal, junior_cal


def seniority(doctors):
    juniors = [doc["name"] for doc in doctors if doc["seniority"] == SeniorityLevel.JUNIOR.name]
    seniors = [doc["name"] for doc in doctors if doc["seniority"] == SeniorityLevel.SENIOR.name]
    return juniors, seniors

def valid_combos(doctors,senior_month,junior_month):
    # NB: not a fan of this solution because combos cannot be accessed with readable keys but with indices
    juniors,seniors = seniority(doctors)
    # careful: combos must be hashable and lists aren't.
    combos = ([(doc,date,ShiftList.DUTY_WEEK.name) for doc in juniors for date in junior_month] + 
              [(doc,date,ShiftList.NIGHT_DUTY.name) for doc in seniors for date in senior_month])
    return combos


class scheduled_model(cp_model.CpModel):

    def __init__(self, doctors,senior_cal,work_weeks,combos): 
        cp_model.CpModel.__init__(self)
        self._doctors = doctors
        self._senior_dates = senior_cal
        self._work_weeks = work_weeks
        self._index = combos
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
            # keep who_can_work for future FREE days handling
            who_can_work = [
                self.shifts[doc,day,ShiftList.NIGHT_DUTY.name] for doc in seniors if (doc,day,ShiftList.NIGHT_DUTY.name) in self._index
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
                self.add_at_most_one([self.shifts[doc,self._senior_dates[day],ShiftList.NIGHT_DUTY.name], 
                                      self.shifts[doc,self._senior_dates[day+1],ShiftList.NIGHT_DUTY.name]])
        return

    def forbid_consecutive_dutyWeek(self):
        # constraint
        # juniors cannot work consecutive duty weeks
        juniors,s = seniority(self._doctors)
        for doc in juniors:
            for n in range(len(self._work_weeks)-1):
                self.add_at_most_one([self.dutyWeek[(doc, self._work_weeks[n])], self.dutyWeek[(doc, self._work_weeks[n+1])]])
        return

    def assign_dutyWeek(self):
        # constraint
        # juniors work six consecutive days of duty, i.e. a dutyWeek
        # NB: ALL variables should be contrained, otherwise the solver assign them to 1
        juniors,s = seniority(self._doctors)    
        for doc in juniors:
            for week in self._work_weeks:
                for date in week:
                    # an example using only_enforce_if
                    #self.add(self.shifts[doc,date,ShiftList.DUTY_WEEK.name] == 1).only_enforce_if(self.dutyWeek[doc,week])
                    #self.add(self.shifts[doc,date,ShiftList.DUTY_WEEK.name] == 0).only_enforce_if(self.dutyWeek[doc,week].Not())
                    # a clearer expression of the above 
                    self.add(self.shifts[doc,date,ShiftList.DUTY_WEEK.name] == self.dutyWeek[doc,week])
        return

    def distribute_nightDuty_workload(self):
        j,seniors = seniority(self._doctors)
        total_shifts = len(set([(day, shift) for d, day, shift in self._index if shift == ShiftList.NIGHT_DUTY.name]))
        min_shifts_per_doctor = total_shifts // len(seniors)
        if total_shifts % len(seniors) == 0:
            max_shifts_per_doctor = min_shifts_per_doctor
        else:
            max_shifts_per_doctor = min_shifts_per_doctor + 1
        for doc in seniors:
            shifts_worked = sum( 
                self.shifts[(doc,day,ShiftList.NIGHT_DUTY.name)] 
                for day in self._senior_dates
                if (doc,day,ShiftList.NIGHT_DUTY.name) in self._index
            )    
            self.add(min_shifts_per_doctor <= shifts_worked)     
            self.add(shifts_worked <= max_shifts_per_doctor)
        return    

    def distribute_dutyWeek_workload(self):
        juniors,s = seniority(self._doctors)
        total_shifts = len(self._work_weeks)
        min_shifts_per_doctor = total_shifts // len(juniors)
        if total_shifts % len(juniors) == 0:
            max_shifts_per_doctor = min_shifts_per_doctor
        else:
            max_shifts_per_doctor = min_shifts_per_doctor + 1
        for doc in juniors:
            shifts_worked = sum(self.dutyWeek[(doc,week)] for week in self._work_weeks)
            self.add(min_shifts_per_doctor <= shifts_worked)     
            self.add(shifts_worked <= max_shifts_per_doctor)
        return

class doctorsPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, shifts, dutyWeek, doctors, senior_cal, work_weeks, combos, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self.dutyWeek = dutyWeek
        self._doctors = doctors
        self._dates = senior_cal
        self._work_weeks = work_weeks
        self._index = combos
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        juniors,seniors = seniority(self._doctors)
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for day in self._dates:
            print(f"Day {day}")
            for doc in self._doctors:    
                is_working = False
                for shift in ShiftList:
                    if (doc["name"],day,shift.name) in self._index:
                        if self.value(self._shifts[(doc["name"],day,shift.name)]):
                            is_working = True
                            print(f"Doctor {doc["name"]} works {shift.name}")
                        if not is_working:
                            print(f"Doctor {doc["name"]} does not work")
        for week in self._work_weeks:
            print(f"Week {week}")
            for doc in juniors:
                is_working = False
                if self.value(self.dutyWeek[doc,week]):
                    is_working = True
                    print(f"Doctor {doc} works {ShiftList.DUTY_WEEK.name}")
                if not is_working:
                    print(f"Doctor {doc} does not work")
                        

        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.stop_search()
    
    def solutionCount(self):
        return self._solution_count
        


def main() -> None:
    # data
    doctors, senior_cal, junior_cal = get_data()
    # create index 
    combos = valid_combos(doctors,senior_cal.month,junior_cal.month)
    # create model
    model = scheduled_model(doctors,senior_cal.month,junior_cal.weeks,combos)
    model.create_variables()
    # night duty
    model.one_employee_per_nightDuty()
    model.distribute_nightDuty_workload()
    model.forbid_consecutive_nightDuty()
    # duty week
    model.one_employee_per_dutyWeek()
    model.distribute_dutyWeek_workload()
    model.forbid_consecutive_dutyWeek()
    model.assign_dutyWeek()
    #print(model)

    # create model
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # enumerate all solutions
    solver.parameters.enumerate_all_solutions = True

    # display the first five solutions.
    solution_limit = 2
    solution_printer = doctorsPartialSolutionPrinter(
        model.shifts, model.dutyWeek, doctors, senior_cal.month, model._work_weeks, combos, solution_limit)

    # invoke the solver
    status = solver.solve(model, solution_printer)
    print(status)


if __name__ == "__main__":
    main()