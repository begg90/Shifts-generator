# a calendar manager

# use datetime to handle atomic dates
# use calendar to keep track of days belonging to bridge weeks
# use pandas to have access to useful methods, e.g. sorting, getting weekdays...
# in the future: use holidays to collect holiday days

# atomic representation (days in month): 
# calendar months are represented as pandas DatetimeIndex.
# Each day is a pd.DateStamp which is a datetime.date object, e.g. '2026-09-01'

# composite representation (weeks in month):
# weeks in a month are represented as closed pandas IntervalIndex.
# Each week is a pandas interval, e.g. [2026-09-07 00:00:00, 2026-09-12 00:00:00],
# where the left is Monday and the right is Saturday of the same week
# Because this is specific for a type of shift, Sundays are excluded and the weeks included
# are those that begin in the selected month (i.e. excluding weeks bridging previous and current month, 
# including weeks bridging current and following month)

import datetime
import calendar
import pandas as pd

class CalendarManager:
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month

    def dates(self) -> pd.DatetimeIndex:
        """returns a complete month as a pandas DateTimeIndex."""
        _, num_days = calendar.monthrange(self.year, self.month)
        days = [datetime.date(self.year, self.month, d) for d in range(1, num_days + 1)]
        return pd.to_datetime(days)

    
    def duty_weeks(self) -> pd.IntervalIndex:
        """Returns an IntervalIndex, each interval spanning Monday-Saturday (inclusive) for weeks
        whose Monday falls in this month."""
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdatescalendar(self.year, self.month)
        bounds = [(w[0], w[5]) for w in weeks if w[0].month == self.month]  # (Monday, Saturday)
        mondays, saturdays = zip(*bounds)
        return pd.IntervalIndex.from_arrays(
            pd.to_datetime(mondays), pd.to_datetime(saturdays), closed="both"
        )

    def duty_week_day_map(self) -> dict[pd.Interval, pd.DatetimeIndex]:
            return {
                week: pd.date_range(week.left, week.right, freq="D")
                for week in self.duty_weeks()
            }

    # might not be needed
    def duty_week_day_map_asperiod(self) -> dict[pd.Period, pd.DatetimeIndex]:
        """returns a dictionary: week Period -> its 6 Mon-Sat working days."""
        return {
            week: pd.date_range(week.start_time.normalize(), periods=6, freq="D")
            for week in self.duty_weeks()
        }
    # might not be needed
    def duty_weeks_asperiod(self) -> pd.PeriodIndex:
            """returns Mon-Sun weeks of the month as PeriodIndex for weeks
            whose Monday falls in this month."""
            cal = calendar.Calendar(firstweekday=0)
            weeks = cal.monthdatescalendar(self.year, self.month)
            mondays = [w[0] for w in weeks if w[0].month == self.month]
            return pd.PeriodIndex(mondays, freq="W-SUN") # freq"W-SUN" means weekly, starting and excluding Sunday. Hence it starts on MONDAY but it finishes a week later... on Sunday!
    
    
# EXAMPLE that will be removed, only here to make it easy to explore the calendar manager
# uncomment to visualize 
""" year = 2026
month = 9
cal = CalendarManager(year,month)
print(cal.dates())
print(cal.dates()[0].weekday())
print(cal.duty_weeks())
print(cal.duty_weeks()[0])
print(type(cal.duty_weeks()[0]))

print(cal.duty_weeks()[0].left)
print(cal.duty_weeks()[0].right) """