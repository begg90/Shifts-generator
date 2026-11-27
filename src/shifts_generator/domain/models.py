"""This module contains the dataclasses Employee and Schedule.

Usage example:

foo = Employee("John", Seniority.SENIOR)
cal = CalendarManager(2026,9)
foo = Schedule(cal)


Let's keep this sentence for now.
This level is general and does not contain any ORTools.
contains employee, shifts, schedule, constraint (abstract)
This way it can be tested without invoking the solver
"""

from dataclasses import InitVar, dataclass, field
from typing import Final

from pandas import Timestamp

from shifts_generator.domain.enums import Seniority, ShiftList
from shifts_generator.utils.time import CalendarManager

DEFAULT_SHIFTS: dict[Seniority, tuple[ShiftList, ...]] = {
    Seniority.JUNIOR: (ShiftList.DUTY_WEEK,),
    Seniority.MEDIOR: (ShiftList.DUTY_WEEK, ShiftList.ON_CALL_NIGHT),
    Seniority.SENIOR: (ShiftList.ON_CALL_NIGHT,),
}


@dataclass  # TODO: (frozen=True)
class Employee:
    """A class representing an Employee.

    Attributes:
        name (str): name of the Employee
        seniority (Seniority): seniority level of the Employee
        available_shifts (list[ShiftList] | None): list of shifts that can be assigned
        to the Employee
    """

    name: str
    seniority: Seniority
    # TODO: unavailability: list[datetime]
    available_shifts: list[ShiftList] | None = field(default=None)

    def __post_init__(self):
        """validate name and seniority, assign (default) available_shifts."""
        if not self.name:
            raise ValueError("Employee name cannot be empty")
        if not isinstance(self.seniority, Seniority):
            raise ValueError("seniority must be a Seniority enum value")
        if self.seniority is Seniority.SPECIAL:
            if not self.available_shifts:
                raise ValueError(f"{self.name}: SPECIAL doctors need an explicit shift list")
            self.available_shifts = list(self.available_shifts)
        else:
            if self.available_shifts is not None:
                raise ValueError(f"{self.name}: custom shifts are only allowed for SPECIAL")
            self.available_shifts = list(DEFAULT_SHIFTS[self.seniority])


# DAILY_SHIFTS is probably NOT complete
# NB. this schedule is now hardcoded
# TODO: it should come from input. HOW?
DAILY_SHIFTS: Final[tuple[tuple[ShiftList, ...], ...]] = (
    (
        ShiftList.DUTY_WEEK,
        ShiftList.DUTY_WEEK_SUPPORT,
        ShiftList.ON_CALL_NIGHT,
    ),  # MON-SAT
    (
        ShiftList.DUTY_WEEK,
        ShiftList.DUTY_WEEK_SUPPORT,
        ShiftList.ON_CALL_NIGHT,
        ShiftList.AROS_NIGHT,
    ),  # MON-SAT + ER_support
    (ShiftList.ON_CALL_24h,),  # SUN
    (
        ShiftList.ON_CALL_24h,
        ShiftList.AROS_DAY,
    ),  # SUN, holidays, + ER_support
)


@dataclass(frozen=True)
class Schedule:
    """A calendar in which for each day,
     there is a dictionary of shifts to cover.

    Attributes:
        cal (~shifts_generator.utils.time.CalendarManager): contains dates and holiday days
        first_er_support_day (~pandas.Timestamp): first day of support to the ER;
            ER support is assumed to happen every other day starting from this
        required (dict[~pandas.Timestamp, tuple[ShiftList, ...]]): contains collection
            of required shift types for each day of the month
    """

    cal: CalendarManager
    er_support_start: InitVar[Timestamp | None] = None
    first_er_support_day: Timestamp = field(init=False)
    required: dict[Timestamp, tuple[ShiftList, ...]] = field(init=False, repr=False, compare=False)

    def __post_init__(self, er_support_start: Timestamp | None) -> None:
        """assign first_er_support_day and required."""

        value = self.cal.dates[0] if er_support_start is None else er_support_start
        object.__setattr__(self, "first_er_support_day", value)

        required = {key: [] for key in self.cal.dates}
        er_support_schedule = self._select_alternate_days()
        for day in self.cal.dates:
            if not self.cal.is_a_holiday[day] and er_support_schedule[day]:
                required[day].append(DAILY_SHIFTS[1])
            elif not self.cal.is_a_holiday[day] and not er_support_schedule[day]:
                required[day].append(DAILY_SHIFTS[0])
            elif self.cal.is_a_holiday[day] and er_support_schedule[day]:
                required[day].append(DAILY_SHIFTS[3])
            else:
                required[day].append(DAILY_SHIFTS[2])
        object.__setattr__(self, "required", required)

    def _select_alternate_days(self):
        """Mark every other day using ``first_er_support_day``.

        The pattern covers the whole calendar, including earlier days.
        Values are 1 (selected) or 0.
        """
        start = self.cal.position(self.first_er_support_day)
        return {day: int(n - start) % 2 == 0 for n, day in enumerate(self.cal.dates)}
