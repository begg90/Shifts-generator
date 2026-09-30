# symbolic names - ... and where to find them?

from enum import Enum, auto

class SeniorityLevel(Enum):
    JUNIOR = auto()
    SENIOR = auto()

class ShiftList(Enum):
    DUTY_WEEK = auto()
    NIGHT_DUTY = auto()
