# SIMPLIFIED SENIOR AND JUNIOR DOCTORS SHIFT
# each day there are TWO shifts: a day shift and a night shift
# juniors work the day shift, seniors work the night shift                      ---> valid_combos()
# there is a month long period schedule

# constraints that are valid for both shift types:
# each shift is done by 1 doctor                                                ---> (1) one_employee_per_nightDuty()
#                                                                                    (2) one_employee_per_dutyWeek()
# the workload is evenly distributed                                            ---> (1) distribute_nightDuty_workload()
#                                                                                    (2) distribute_dutyWeek_workload()
# forbit consecutive shifts                                                     ---> (1) forbid_consecutive_nightDuty()
#                                                                                    (2) forbid_consecutive_dutyWeek()

# constraints that are valid for the day shift only:
# junior doctors work Monday to Saturday included, hence six consecutive days.                  ---> assign_dutyWeek()
# Sunday is a rest day for all junior doctors (Sundays will become dayDuty in a later version). --->  obtained with valid_combos()
# not more than 2 dutyWeeks per month                                                           ---> ? DO NOT IMPLEMENT: redundant
# The one in the previous line does not prevent assigning 2 weeks to 2 people
# and leaving a 3rd unassigned. Hence, we need a distribution of workload.
# We probably don't need a "no more than 2 weeks per month" constraint because there are 4 weeks.
# Though, it is good to look at exceptions of 5 weeks long months and how it combines with this handling of the planning

# Here the variables are pandas series


from ortools.sat.python import cp_model
import pandas as pd
from time_organizer import my_calendar
from local_enums import SeniorityLevel, ShiftList

def get_data():
    # personnel
    doctors = [{"name":"eenie","seniority":SeniorityLevel.SENIOR.name},
               {"name":"meenie","seniority":SeniorityLevel.SENIOR.name},
               {"name":"miney","seniority":SeniorityLevel.SENIOR.name},
               {"name":"moe","seniority":SeniorityLevel.SENIOR.name},
               {"name":"tom","seniority":SeniorityLevel.SENIOR.name},
               {"name":"jerry","seniority":SeniorityLevel.SENIOR.name},
               {"name":"mini1","seniority":SeniorityLevel.JUNIOR.name},
               {"name":"mini2","seniority":SeniorityLevel.JUNIOR.name},
               {"name":"mini3","seniority":SeniorityLevel.JUNIOR.name}]

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
    juniors,seniors = seniority(doctors)
    # careful: combos must be hashable and lists aren't.
    combos = ([(doc,date,ShiftList.DUTY_WEEK.name) for doc in juniors for date in junior_month] + 
              [(doc,date,ShiftList.NIGHT_DUTY.name) for doc in seniors for date in senior_month])
    return combos

class scheduled_model(cp_model.CpModel):
    """our model including variables and constraints"""
    def __init__(self,valid_index:pd.MultiIndex,dutyWeek_index:pd.MultiIndex): 
        cp_model.CpModel.__init__(self)
        self._valid_index = valid_index
        self._dutyWeek_index = dutyWeek_index
        self.shifts = {}
        self.dutyWeek = {} # this one could even be _dutyWeek

    def create_variables(self):
        """creates variable shifts and dutyWeek"""
        self.shifts = self.new_bool_var_series(name="shifts", index=self._valid_index)
        self.dutyWeek = self.new_bool_var_series(name="dutyWeek", index=self._dutyWeek_index)   
        return self.shifts,self.dutyWeek

    def one_employee_per_nightDuty(self):
        """constraint: assigns one senior per night duty shift"""
        who_can_work = self.shifts.xs(ShiftList.NIGHT_DUTY.name, level = "shift_type")
        for _, doctors in who_can_work.groupby(level = "date"):
            self.add_exactly_one(doctors)
        return
    
    def one_employee_per_dutyWeek(self):
        """constraint: assigns one junior per duty week shift Mon-Sat"""
        for _, doctors in self.dutyWeek.groupby(level = "week"):
            self.add_exactly_one(doctors)
        return
    
    def forbid_consecutive_nightDuty(self):
        """constraint: seniors cannot work consecutive night shifts"""
        duty_shifts = self.shifts.xs(ShiftList.NIGHT_DUTY.name, level = "shift_type")
        for _, date in duty_shifts.groupby(level = "doctor"):
            # make sure the dates are sorted
            # THIS is not sorted enough. The days belonging to the following month are not in the right place!!!
            date = date.sort_index(level = "date")
            for current_day,following_day in zip(date.iloc[:-1], date.iloc[1:]):
                self.add_at_most_one([current_day,following_day])
        return

    def forbid_consecutive_dutyWeek(self):
        """constraint: juniors cannot work consecutive duty weeks"""
        for _, week in self.dutyWeek.groupby(level = "doctor"):
            for current_week, following_week in zip(week.iloc[:-1],week.iloc[1:]):
                self.add_at_most_one([current_week,following_week])
        return

    def assign_dutyWeek(self):
        """constraint: translates duty weeks into day shifts"""
        duty_shifts = self.shifts.xs(ShiftList.DUTY_WEEK.name, level = "shift_type")
        for (doc, week), duty_week in self.dutyWeek.items():
            for date in week:
                self.add(duty_shifts.loc[(doc, date)] == duty_week)
        return

    def distribute_nightDuty_workload(self):
        """evenly distributs night duty shifts to seniors"""
        # NB. this can be generalized
        mask = self._valid_index.get_level_values(level = "shift_type") == ShiftList.NIGHT_DUTY.name
        total_shifts = self._valid_index[mask].get_level_values(level = "date").nunique()
        ndocs = self._valid_index[mask].get_level_values(level = "doctor").nunique()
        min_shifts_per_doctor = total_shifts // ndocs
        if total_shifts % ndocs == 0:
            max_shifts_per_doctor = min_shifts_per_doctor
        else:
            max_shifts_per_doctor = min_shifts_per_doctor + 1

        night_duty = self.shifts.xs( ShiftList.NIGHT_DUTY.name, level = "shift_type")
        shifts_worked = night_duty.groupby(level = "doctor").agg(sum)#sum()
        for doc, workload in shifts_worked.items():
            self.add(min_shifts_per_doctor <= workload)
            self.add(workload <= max_shifts_per_doctor)
        return    

    def distribute_dutyWeek_workload(self):
        """evenly distributs duty weeks shifts to juniors"""
        total_shifts = self._dutyWeek_index.get_level_values("week").nunique()
        ndocs = self._dutyWeek_index.get_level_values("doctor").nunique()
        min_shifts_per_doctor = total_shifts // ndocs
        if total_shifts % ndocs == 0:
            max_shifts_per_doctor = min_shifts_per_doctor
        else:
            max_shifts_per_doctor = min_shifts_per_doctor + 1

        shifts_worked = self.dutyWeek.groupby(level = "doctor").agg(sum)
        for doc,workload in shifts_worked.items():
            self.add(min_shifts_per_doctor <= workload)     
            self.add(workload <= max_shifts_per_doctor)
        return

class doctorsPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """print intermediate solutions"""
    def __init__(self, shifts:pd.Series, dutyWeek:pd.Series, work_month, work_weeks, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._dutyWeek = dutyWeek
        self._work_month = work_month
        self._work_weeks = work_weeks
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        all_doctors = self._shifts.index.get_level_values(level = "doctor").unique()
        dutyWeek_docs = self._dutyWeek.index.get_level_values(level = "doctor").unique()
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for day in self._work_month:
            print(f"Day {day}")
            for doc in all_doctors:     
                for shift in ShiftList:
                    key = (doc,day,shift.name)
                    if key in self._shifts.index:
                        if self.value(self._shifts.loc[key]):
                            print(f"Doctor {doc} works {shift.name}")
                        else:
                            print(f"Doctor {doc} X")    
        # print dutyWeek
        week_number = 1 # ugly fix for now
        for week in self._work_weeks:
            print(f"Week {week_number}")
            for doc in dutyWeek_docs:
                if self.value(self._dutyWeek.loc[doc,week]):
                    print(f"Doctor {doc} works {ShiftList.DUTY_WEEK.name}")
                else:
                    print(f"Doctor {doc} X")
            week_number += 1 
  
        print(f"\n STATISTICS:\n")  
        night_duty = self._shifts.xs( ShiftList.NIGHT_DUTY.name, level = "shift_type")
        shifts_worked = night_duty.groupby(level = "doctor").agg(sum)
        for doc, _ in shifts_worked.items():
            shifts_number = self.value(shifts_worked[doc])
            print(f"Doctor {doc}'s number of {ShiftList.NIGHT_DUTY.name} shifts: {shifts_number} ")     

        shifts_worked = self._dutyWeek.groupby(level = "doctor").agg(sum)
        for doc, _ in shifts_worked.items():
            shifts_number = self.value(shifts_worked[doc])
            print(f"Doctor {doc}'s number of {ShiftList.DUTY_WEEK.name} shifts: {shifts_number} ")  
            
        if self._solution_count >= self._solution_limit:
            print(f"\n Stop search after {self._solution_limit} solutions")
            self.stop_search()
    
    def solutionCount(self):
        return self._solution_count
        


def main() -> None:
    # data
    doctors, senior_cal, dutyWeek_cal = get_data()
    # create index 
    combos = valid_combos(doctors,senior_cal.month,dutyWeek_cal.month)
    # create a MultiIndex with combos
    valid_index = pd.MultiIndex.from_tuples(combos, names= ["doctor","date","shift_type"])
    # create a MukltiIndex for the dutyWeek shift
    juniors,_ = seniority(doctors)
    dutyWeek_index = pd.MultiIndex.from_product([juniors, dutyWeek_cal.weeks], names=["doctor", "week"])
    # create model
    model = scheduled_model(valid_index,dutyWeek_index)
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

    # display the first solution_limit solutions
    solution_limit = 1
    solution_printer = doctorsPartialSolutionPrinter(
        model.shifts, model.dutyWeek, senior_cal.month, dutyWeek_cal.weeks,solution_limit)

    # invoke the solver
    status = solver.solve(model, solution_printer)
    print(status)


if __name__ == "__main__":
    main()