import pytest

from shifts_generator.domain.enums import Seniority, ShiftList
from shifts_generator.domain.models import DEFAULT_SHIFTS, Employee


def test_special_uses_available_shifts():
    shifts = [ShiftList.NIGHT_DUTY, ShiftList.DUTY_WEEK]
    doc = Employee(name="John", seniority=Seniority.SPECIAL, available_shifts=shifts)
    assert doc.available_shifts == shifts


def test_special_without_available_shifts_raises():
    with pytest.raises(ValueError, match="SPECIAL"):
        Employee(name="John", seniority=Seniority.SPECIAL)


def test_special_with_empty_shifts_raises():
    with pytest.raises(ValueError):
        Employee(name="John", seniority=Seniority.SPECIAL, available_shifts=[])


def test_available_shifts_rejected_for_not_special():
    shifts = [ShiftList.NIGHT_DUTY, ShiftList.DUTY_WEEK]
    with pytest.raises(ValueError):
        Employee(name="John", seniority=Seniority.JUNIOR, available_shifts=shifts)


@pytest.mark.parametrize("seniority", list(DEFAULT_SHIFTS))
def test_default_shifts_match_seniority(seniority):
    doc = Employee(name="John", seniority=seniority)
    assert doc.available_shifts == list(DEFAULT_SHIFTS[seniority])
