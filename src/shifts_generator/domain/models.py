"""This module contains the dataclass Employee.

Usage example:

foo = Employee("John", Seniority.SENIOR)
"""

from dataclasses import dataclass, field

from shifts_generator.domain.enums import Seniority, ShiftList

"""
Let's keep this sentence for now.
This level is general and does not contain any ORTools.
contains employee, shifts, schedule, constraint (abstract)
This way it can be tested without invoking the solver"""


DEFAULT_SHIFTS: dict[Seniority, tuple[ShiftList, ...]] = {
    Seniority.JUNIOR: (ShiftList.DUTY_WEEK,),
    Seniority.MEDIOR: (ShiftList.DUTY_WEEK, ShiftList.NIGHT_DUTY),
    Seniority.SENIOR: (ShiftList.NIGHT_DUTY,),
}


@dataclass  # (frozen=TRUE) ?
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
