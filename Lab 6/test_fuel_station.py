"""Comprehensive tests for Lab 6 code and branch coverage."""
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# fuel_bill: validation, covered fuel, loyalty, grade and volume discounts.
def test_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


def test_exactly_covered_litres():
    assert fuel_bill("regular", 10, "silver") == 0


def test_unknown_grade_raises_value_error():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 20, "silver")


@pytest.mark.parametrize("litres", [-1, -0.01])
def test_negative_litres_raise_value_error(litres):
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", litres, "silver")


def test_gold_regular_gets_five_extra_covered_litres():
    assert fuel_bill("regular", 15, "gold") == 0


def test_gold_premium_gets_five_extra_covered_litres():
    assert fuel_bill("premium", 20, "gold") == 0


def test_gold_diesel_does_not_get_extra_covered_litres():
    assert fuel_bill("diesel", 21, "gold") == 90


def test_non_gold_regular_rate():
    assert fuel_bill("regular", 11, "silver") == 105


def test_non_diesel_uses_regular_rate():
    assert fuel_bill("premium", 16, "bronze") == 105


def test_diesel_uses_diesel_rate():
    assert fuel_bill("diesel", 21, "silver") == 90


def test_extra_exactly_thirty_does_not_get_bulk_discount():
    # regular covers 10 L; 40 L leaves exactly 30 chargeable litres.
    assert fuel_bill("regular", 40, "silver") == 30 * 105


def test_extra_above_thirty_gets_bulk_discount():
    # 41 L leaves 31 chargeable litres; rate becomes 105 - 6.
    assert fuel_bill("regular", 41, "silver") == 31 * 99


def test_gold_bulk_discount_applies_additional_reduction():
    # Gold regular covers 15 L; 46 L leaves 31 chargeable litres.
    assert fuel_bill("regular", 46, "gold") == 31 * 95


# pump_allowed: fleet/non-fleet and all decision outcomes.
def test_fleet_request_at_limit_is_allowed():
    assert pump_allowed(200, 20, True) is True


def test_fleet_request_above_limit_is_rejected():
    assert pump_allowed(201, 1, True) is False


def test_non_fleet_request_under_volume_limit_with_one_container_is_allowed():
    assert pump_allowed(60, 1, False) is True


def test_non_fleet_request_over_volume_limit_is_rejected():
    assert pump_allowed(61, 1, False) is False


def test_non_fleet_multiple_containers_are_rejected():
    assert pump_allowed(30, 2, False) is False


def test_non_fleet_zero_containers_follows_existing_rule():
    assert pump_allowed(30, 0, False) is True


# session_status: card/cash cutoffs, day/night and three statuses.
@pytest.mark.parametrize(
    "seconds,is_card,is_night,expected",
    [
        (60, True, False, "active"),
        (59, True, False, "warning"),
        (44, True, False, "timed_out"),
        (30, False, False, "active"),
        (29, False, False, "warning"),
        (14, False, False, "timed_out"),
        (90, True, True, "active"),
        (75, True, True, "warning"),
        (74, True, True, "timed_out"),
        (45, True, True, "timed_out"),
        (60, False, True, "active"),
        (45, False, True, "warning"),
        (44, False, True, "timed_out"),
    ],
)
def test_session_status_boundaries(seconds, is_card, is_night, expected):
    assert session_status(seconds, is_card, is_night) == expected
