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
    # names in Italian, and tmp choices in English:
    # guardia diurna            DUTY_WEEK
    # aiuto guardia diurna      SUPPORT_DUTY_WEEK
    # reperibile giorno/notte   ON_CALL_NIGHT/ON_CALL_24h
    # AROS giorno/notte         AROS_DAY/AR0S_NIGHT
    # accoglimento              ER_SUPPORT (Emergency Room Support)
    # TODO: NB. on_call_night/on_call_24h does not matter for the solver.
    # They might as well become one shift type, ON_CALL. Check with users
    DUTY_WEEK = "duty_week"
    DUTY_WEEK_SUPPORT = "duty_week_support"
    ON_CALL_NIGHT = "on_call_night"
    ON_CALL_24h = "on_call_24h"
    AROS_DAY = "AROS_day"
    AROS_NIGHT = "AROS_night"
    ER_SUPPORT = "ER_support"
