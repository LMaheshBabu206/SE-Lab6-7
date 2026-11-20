"""Hypothesis properties and focused regression tests for Lab 7."""
import math
import pytest
from hypothesis import given, settings, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill


# parse_purchase: valid arbitrary grade and positive finite decimal values.
@given(
    grade=st.text(min_size=1).filter(lambda s: s.strip() != "" and ":" not in s),
    litres=st.floats(min_value=0.001, max_value=1_000_000, allow_nan=False, allow_infinity=False),
)
def test_parse_purchase_valid_inputs(grade, litres):
    parsed_grade, parsed_litres = parse_purchase(f" {grade} : {litres} ")
    assert parsed_grade == grade.strip().title()
    assert math.isclose(parsed_litres, litres, rel_tol=1e-12, abs_tol=1e-12)


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.lists(st.text())))
def test_parse_purchase_rejects_non_string_inputs(value):
    with pytest.raises(TypeError):
        parse_purchase(value)


@given(st.text().filter(lambda s: s.count(":") != 1))
def test_parse_purchase_rejects_wrong_separator_count(value):
    with pytest.raises(ValueError):
        parse_purchase(value)


@pytest.mark.parametrize("value", [":10", "regular:", " : 10 ", "regular:abc", "regular:0", "regular:-1", "regular:nan", "regular:inf"])
def test_parse_purchase_rejects_invalid_fields(value):
    with pytest.raises(ValueError):
        parse_purchase(value)


# volume_average: non-empty lists of non-negative integers.
@given(st.lists(st.integers(min_value=0, max_value=10**9), min_size=1, max_size=100))
def test_volume_average_matches_floor_average(values):
    csv = ",".join(str(value) for value in values)
    assert volume_average(csv) == sum(values) // len(values)


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.lists(st.integers())))
def test_volume_average_rejects_non_string_inputs(value):
    with pytest.raises(TypeError):
        volume_average(value)


@given(st.text().filter(lambda s: s == "" or any(not part.strip() for part in s.split(","))))
def test_volume_average_rejects_empty_csv_fields(value):
    with pytest.raises(ValueError):
        volume_average(value)


@pytest.mark.parametrize("value", ["one,2", "1.5,2", "-1,2", "1,,2", ",1", "1,", "", " "])
def test_volume_average_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        volume_average(value)


# payable_bill: non-negative finite values and bounded output.
@given(
    bill=st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
)
def test_payable_bill_matches_expected_formula(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert math.isclose(result, max(bill * 1.18 - discount, 0.0), rel_tol=1e-12, abs_tol=1e-9)
    assert result >= 0


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.lists(st.text())))
def test_payable_bill_rejects_non_string_inputs(value):
    with pytest.raises(TypeError):
        payable_bill(value)


@given(st.text().filter(lambda s: s.count("|") != 1))
def test_payable_bill_rejects_wrong_separator_count(value):
    with pytest.raises(ValueError):
        payable_bill(value)


@pytest.mark.parametrize("value", ["|10", "100|", "abc|10", "100|xyz", "-1|0", "100|-1", "nan|1", "1|inf"])
def test_payable_bill_rejects_invalid_fields(value):
    with pytest.raises(ValueError):
        payable_bill(value)


@pytest.mark.parametrize("value,expected", [("100|200", 0.0), ("100|0", 118.0), ("2500|100", 2850.0)])
def test_payable_bill_examples(value, expected):
    assert payable_bill(value) == expected
