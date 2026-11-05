"""Code-coverage tests for bike_share_rental.py."""
import pytest
from bike_share_rental import can_unlock, dock_status, ride_cost


@pytest.mark.parametrize(
    ("bike_type", "minutes", "subscriber", "peak", "expected"),
    [
        ("standard", 45, False, False, 40),
        ("electric", 30, False, False, 35),
        ("cargo", 30, False, True, 50),
        ("standard", 30, True, False, 0),
        ("electric", 60, True, False, 35),
        ("standard", 30, False, True, 35),
        ("standard", 181, False, False, 240),
    ],
)
def test_ride_cost_pricing_scenarios(bike_type, minutes, subscriber, peak, expected):
    assert ride_cost(bike_type, minutes, subscriber, peak) == expected


@pytest.mark.parametrize(
    ("bike_type", "minutes", "subscriber", "peak", "message"),
    [
        ("mountain", 30, False, False, "unknown bike type"),
        ("standard", 0, False, False, "invalid duration"),
        ("standard", -1, True, True, "invalid duration"),
    ],
)
def test_ride_cost_rejects_invalid_inputs(bike_type, minutes, subscriber, peak, message):
    with pytest.raises(ValueError, match=message):
        ride_cost(bike_type, minutes, subscriber, peak)


@pytest.mark.parametrize(
    ("bikes_docked", "capacity", "expected"),
    [
        (0, 10, "empty"),
        (10, 10, "full"),
        (1, 10, "few bikes"),
        (5, 6, "few slots"),
        (5, 10, "available"),
    ],
)
def test_dock_status_scenarios(bikes_docked, capacity, expected):
    assert dock_status(bikes_docked, capacity) == expected


@pytest.mark.parametrize(
    ("bikes_docked", "capacity", "message"),
    [
        (0, 0, "invalid capacity"),
        (3, -1, "invalid capacity"),
        (-1, 10, "invalid bike count"),
        (11, 10, "invalid bike count"),
    ],
)
def test_dock_status_rejects_invalid_inputs(bikes_docked, capacity, message):
    with pytest.raises(ValueError, match=message):
        dock_status(bikes_docked, capacity)


@pytest.mark.parametrize(
    ("balance", "active_ride", "age", "expected"),
    [
        (100, False, 20, True),
        (49, False, 20, False),
        (100, False, 17, True),
        (99, False, 17, False),
        (100, False, 15, False),
        (100, True, 20, False),
    ],
)
def test_can_unlock_scenarios(balance, active_ride, age, expected):
    assert can_unlock(balance, active_ride, age) is expected
