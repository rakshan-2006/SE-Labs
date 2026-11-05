"""Branch-coverage tests for every decision in bike_share_rental.py.

These tests intentionally hit both outcomes of compound and sequential
conditions, plus boundary values around thresholds.
"""
import pytest
from bike_share_rental import can_unlock, dock_status, ride_cost


@pytest.mark.parametrize(
    ("bike_type", "minutes", "subscriber", "peak", "expected"),
    [
        ("standard", 1, False, False, 20),
        ("standard", 30, True, False, 0),
        ("standard", 31, True, False, 20),
        ("electric", 30, False, False, 35),
        ("cargo", 30, False, True, 50),
        ("standard", 30, False, True, 35),
        ("standard", 180, False, False, 120),
        ("standard", 181, False, False, 240),
    ],
)
def test_ride_cost_decision_branches(bike_type, minutes, subscriber, peak, expected):
    assert ride_cost(bike_type, minutes, subscriber, peak) == expected


@pytest.mark.parametrize(
    ("bike_type", "minutes", "subscriber", "peak", "message"),
    [
        ("unknown", 30, False, False, "unknown bike type"),
        ("standard", 0, False, False, "invalid duration"),
        ("standard", -30, False, True, "invalid duration"),
    ],
)
def test_ride_cost_validation_branches(bike_type, minutes, subscriber, peak, message):
    with pytest.raises(ValueError, match=message):
        ride_cost(bike_type, minutes, subscriber, peak)


@pytest.mark.parametrize(
    ("bikes", "capacity", "expected"),
    [
        (0, 10, "empty"),
        (10, 10, "full"),
        (1, 10, "few bikes"),
        (2, 10, "few bikes"),
        (3, 10, "available"),
        (8, 10, "few slots"),
        (7, 10, "available"),
    ],
)
def test_dock_status_decision_branches(bikes, capacity, expected):
    assert dock_status(bikes, capacity) == expected


@pytest.mark.parametrize(
    ("bikes", "capacity", "message"),
    [
        (0, 0, "invalid capacity"),
        (1, -1, "invalid capacity"),
        (-1, 10, "invalid bike count"),
        (11, 10, "invalid bike count"),
    ],
)
def test_dock_status_validation_branches(bikes, capacity, message):
    with pytest.raises(ValueError, match=message):
        dock_status(bikes, capacity)


@pytest.mark.parametrize(
    ("balance", "active", "age", "expected"),
    [
        (500, True, 30, False),
        (500, False, 15, False),
        (100, False, 16, True),
        (99, False, 16, False),
        (100, False, 17, True),
        (99, False, 17, False),
        (50, False, 18, True),
        (49, False, 18, False),
    ],
)
def test_can_unlock_all_decision_outcomes(balance, active, age, expected):
    assert can_unlock(balance, active, age) is expected
