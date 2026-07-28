# This level is general and does not contain any ORTools 
# contains employee, shifts, schedule, constraint (abstract)
# This way it can be tested without invoking the solver

# example of code snippet
from dataclasses import dataclass, field
from typing import Set
from shifts_generator.domain.enums import Seniority


@dataclass(frozen=True)
class Employee:
    id: str
    name: str
    roles: Set[str] = field(default_factory=set)
    max_hours_per_week: int = 40
    seniority: Seniority = Seniority.JUNIOR

    def __post_init__(self):
        if not self.id:
            raise ValueError("Employee id cannot be empty")
        if not self.name:
            raise ValueError("Employee name cannot be empty")
        if not self.roles:
            raise ValueError("Employee must have at least one role")
        if self.max_hours_per_week <= 0:
            raise ValueError("max_hours_per_week must be positive")
        if not isinstance(self.seniority, Seniority):
            raise ValueError("seniority must be a Seniority enum value")