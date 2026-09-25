import calendar

cal = calendar.Calendar()

# get month as a list of tuples containing (yyyy,mm,dd,weekdaynumber)
# only keep tuples of (dd,weekdaynumber)
# remove days belonging to previous month (they do not need planning). Here they are saved with their dd as in a classical calendar
# rename extra days of following month as zeros (the same as with weeks)
# rename weekdaynumber as weekdayname, e.g. weekdaynumber  = 0 ---> weekdayname = "MONDAY"

# get month as a list containing weeks as lists of tuples (dd,weekdaynumber)
# remove days belonging to previous month (they do not need planning). Here they are saved with their dd == 0
# rename weekdaynumber as weekdayname, e.g. weekdaynumber  = 0 ---> weekdayname = "MONDAY"


class my_calendar(calendar.Calendar):

    def __init__(self,year,month):
        calendar.Calendar.__init__(self)
        self._year = year
        self._month = month
        self.month = []
        self.weeks = []

    def __repr__(self):
        lines = [
            f"my_calendar(",
            f"  year={self._year},",
            f"  month={self._month},",
            f"  calendar_weeks={self.weeks},",
            f"  calendar_days={self.month}",
            f")"
        ]
        return "\n".join(lines)

    def get_month_asnumbers(self):
            # month as tuples of (dd, weekdayname)
            self.month = [ (day,week_day) for y,m,day,week_day in self.itermonthdays4(self._year,self._month) ]
            return self.month
    
    def get_month_asstrings(self):
        # month as tuples of (dd, weekdayname)
        self.month = [ (day,calendar.day_name[week_day]) for y,m,day,week_day in self.itermonthdays4(self._year,self._month) ]
        return self.month    

    def month_cleanup(self):
        # keep days from the 1st of the month till the end
        self.month = [ (day,w) for day,w in self.month[:6] if 1 <= day <= 6 ] + self.month[6:]
        # set the days belonging to the following month to zero
        self.month = self.month[:-6] + [(0,w) if 1 <= day <= 6 else (day,w) for day,w in self.month[-6:]]       
        return self.month          

    def month_removeSundays(self):
        self.month = [ (day, w) for day,w in self.month if w != calendar.SUNDAY and w != "Sunday"]
        return self.month

    def get_weeks_asnumbers(self): # needs a better name
        self.weeks = [tuple(week) for week in self.monthdays2calendar(self._year, self._month)]    
        return self.weeks

    def get_weeks_asstrings(self): # needs a better name
        # rename days from number to string
        self.weeks = [
            tuple( (day,calendar.day_name[week_day]) for day,week_day in week) 
            for week in self.monthdays2calendar(self._year, self._month)
        ]
        return self.weeks    

    def weeks_cleanup(self):
        # discard week whose planning belongs to previous month
        self.weeks = [tuple(week) for week in self.weeks if week[0][0] !=0]
        return self.weeks 
    
    def weeks_removeSundays(self):
        self.weeks = [tuple(week[:-1]) for week in self.weeks]
        return self.weeks

           

