from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from shifts_generator.utils.time import CalendarManager


@pytest.fixture
def cal() -> CalendarManager:
    return CalendarManager(2026, 9)


def test_year_not_empty():
    with pytest.raises(ValueError):
        CalendarManager(year=None, month=9)


def test_month_not_empty():
    with pytest.raises(ValueError):
        CalendarManager(year=2026, month=None)


@pytest.mark.parametrize("year, month, n_days", [(2026, 1, 31), (2026, 2, 28), (2026, 4, 30), (2028, 2, 29)])
def test_dates_covers_whole_month(year, month, n_days) -> None:
    cal = CalendarManager(year, month)
    assert len(cal.dates) == n_days
    assert cal.dates[0] == pd.Timestamp(year, month, 1)
    assert cal.dates[-1] == pd.Timestamp(year, month, n_days)
    assert cal.dates.is_monotonic_increasing


def test_is_a_holiday_has_one_entry_per_day(cal: CalendarManager) -> None:
    assert len(cal.is_a_holiday) == len(cal.dates)
    assert set(cal.is_a_holiday.values()) <= {0, 1}


def test_is_frozen(cal: CalendarManager) -> None:
    # with pytest.raises(Exception):
    with pytest.raises(FrozenInstanceError):
        cal.year = 2027


def test_position(cal: CalendarManager) -> None:
    assert cal.position(pd.Timestamp("2026-09-03")) == 2  # noqa: PLR2004


def test_position_outside_calendar(cal: CalendarManager) -> None:
    with pytest.raises(KeyError):
        cal.position("2026-01-01")


def test_dates_are_unique(cal: CalendarManager) -> None:
    assert cal.dates.is_unique
