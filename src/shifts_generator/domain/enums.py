"""Symbolic constants grouped in classes."""

from enum import Enum


class Seniority(Enum):
    "Seniority levels represented by strings."

    JUNIOR = "junior"
    MEDIOR = "medior"
    SENIOR = "senior"
    SPECIAL = "special"


class ShiftList(Enum):
    "Shift types represented by strings."

    # TODO: complete list of shifts with appropriate naming
    DUTY_WEEK = "duty_week"
    NIGHT_DUTY = "night_duty"
