from itertools import pairwise

import pytest
from pandas import Timestamp

from shifts_generator.domain.enums import Seniority, ShiftList
from shifts_generator.domain.models import DEFAULT_SHIFTS, Employee, Schedule
from shifts_generator.utils.time import CalendarManager


# ---------------------------
# Test dataclass Employee
# ---------------------------
def test_special_uses_available_shifts():
    shifts = [ShiftList.ON_CALL_NIGHT, ShiftList.DUTY_WEEK]
    doc = Employee(name="John", seniority=Seniority.SPECIAL, available_shifts=shifts)
    assert doc.available_shifts == shifts


def test_special_without_available_shifts_raises():
    with pytest.raises(ValueError, match="SPECIAL"):
        Employee(name="John", seniority=Seniority.SPECIAL)


def test_special_with_empty_shifts_raises():
    with pytest.raises(ValueError):
        Employee(name="John", seniority=Seniority.SPECIAL, available_shifts=[])


def test_available_shifts_rejected_for_not_special():
    shifts = [ShiftList.ON_CALL_NIGHT, ShiftList.DUTY_WEEK]
    with pytest.raises(ValueError):
        Employee(name="John", seniority=Seniority.JUNIOR, available_shifts=shifts)


@pytest.mark.parametrize("seniority", list(DEFAULT_SHIFTS))
def test_default_shifts_match_seniority(seniority: Seniority):
    doc = Employee(name="John", seniority=seniority)
    assert doc.available_shifts == list(DEFAULT_SHIFTS[seniority])


# ---------------------------
# Test dataclass Schedule
# ---------------------------
@pytest.mark.parametrize("start", [Timestamp("2026-12-01"), Timestamp("2026-12-04")])
def test_select_alternate_days(start: Timestamp) -> None:
    cal = CalendarManager(2026, 12)
    obj = Schedule(cal, start)
    schedule = obj._select_alternate_days()
    values = list(schedule.values())

    assert schedule[start] == 1
    assert all(a + b == 1 for a, b in pairwise(values))
