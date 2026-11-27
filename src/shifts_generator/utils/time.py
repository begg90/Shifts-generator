"""A module to handle all things concerning time.

It contains the class CalendarManager.

Usage example:
c = CalendarManager(2026,9)
"""

import calendar
import datetime
from dataclasses import dataclass, field
from typing import Literal

import holidays
import pandas as pd


@dataclass(frozen=True)
class CalendarManager:
    """
    A class that provides
    a calendar and a collection of holiday days for given
    year and month.

    Args:
        year (int): integer representing the year, e.g. 2026
        month (int): integer representing the month, e.g. 9
        dates (~pandas.DatetimeIndex): calendar where each day is a pandas.DateStamp
            e.g. '2026-09-01'
        is_a_holiday (tuple[int, ...]): mask where 1 is a holiday and 0 is a weekday
    """

    year: int
    month: int
    dates: pd.DatetimeIndex = field(init=False, repr=False, compare=False)
    is_a_holiday: dict[pd.Timestamp, Literal[1, 0]] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        """Validate year and month, create calendar and holidays mask."""
        # TODO: is this the best place to validate the input data?
        if not self.year:
            raise ValueError("Year cannot be empty")
        if not self.month:
            raise ValueError("Month cannot be empty")
        # TODO: put in _method?
        _, num_days = calendar.monthrange(self.year, self.month)
        dates = pd.to_datetime([datetime.date(self.year, self.month, d) for d in range(1, num_days + 1)])
        # TODO: put in _method?
        h = holidays.country_holidays("IT", subdiv="VR", years=self.year)
        is_a_holiday = dict([(d, 1) if d.weekday() == calendar.SUNDAY or d.date() in h else (d, 0) for d in dates])

        object.__setattr__(self, "dates", dates)
        object.__setattr__(self, "is_a_holiday", is_a_holiday)

    def position(self, day: pd.Timestamp) -> int:
        """Return index of day. Raise KeyError if it isn't in the calendar."""
        p = self.dates.get_loc(day)
        assert isinstance(p, int), "calendar dates are unique"
        return p
