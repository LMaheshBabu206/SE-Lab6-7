"""Hardened fuel-station input processors for Lab 7 fuzz testing."""
import math


def parse_purchase(text):
    """Parse 'grade:litres'; reject malformed, empty or invalid purchases."""
    if not isinstance(text, str):
        raise TypeError("purchase must be a string")
    if text.count(":") != 1:
        raise ValueError("purchase must contain exactly one ':' separator")
    grade, litres_text = text.split(":")
    grade = grade.strip()
    litres_text = litres_text.strip()
    if not grade:
        raise ValueError("fuel grade cannot be empty")
    if not litres_text:
        raise ValueError("litres cannot be empty")
    try:
        litres = float(litres_text)
    except ValueError as exc:
        raise ValueError("litres must be numeric") from exc
    if not math.isfinite(litres):
        raise ValueError("litres must be finite")
    if litres <= 0:
        raise ValueError("litres must be greater than zero")
    return grade.title(), litres


def volume_average(volumes_csv):
    """Return the integer-floor average of a non-empty CSV of nonnegative volumes."""
    if not isinstance(volumes_csv, str):
        raise TypeError("volumes must be a CSV string")
    parts = volumes_csv.split(",")
    if not parts or any(not part.strip() for part in parts):
        raise ValueError("volumes must contain non-empty comma-separated values")
    values = []
    for part in parts:
        try:
            value = int(part.strip())
        except ValueError as exc:
            raise ValueError("each volume must be an integer") from exc
        if value < 0:
            raise ValueError("volumes cannot be negative")
        values.append(value)
    return sum(values) // len(values)


def payable_bill(text):
    """Parse 'bill|discount' and calculate a non-negative payable total."""
    if not isinstance(text, str):
        raise TypeError("bill details must be a string")
    if text.count("|") != 1:
        raise ValueError("bill details must contain exactly one '|' separator")
    bill_text, discount_text = (part.strip() for part in text.split("|"))
    if not bill_text or not discount_text:
        raise ValueError("bill and discount must both be provided")
    try:
        bill = float(bill_text)
        discount = float(discount_text)
    except ValueError as exc:
        raise ValueError("bill and discount must be numeric") from exc
    if not math.isfinite(bill) or not math.isfinite(discount):
        raise ValueError("bill and discount must be finite")
    if bill < 0 or discount < 0:
        raise ValueError("bill and discount cannot be negative")
    total = bill * 1.18 - discount
    return max(total, 0.0)


def main():
    print("==== Running parse_purchase ====")
    try:
        result = parse_purchase(input("Enter grade:litres (e.g. diesel:25): "))
        print("Grade and Litres:", result)
    except (TypeError, ValueError) as exc:
        print("Invalid purchase:", exc)

    print("\n==== Running volume_average ====")
    try:
        result = volume_average(input("Enter pump volumes in litres as CSV (e.g. 10,25,40): "))
        print("Average Volume:", result)
    except (TypeError, ValueError) as exc:
        print("Invalid volumes:", exc)

    print("\n==== Running payable_bill ====")
    try:
        result = payable_bill(input("Enter bill|discount (e.g. 2500|100): "))
        print("Payable Bill:", result)
    except (TypeError, ValueError) as exc:
        print("Invalid bill:", exc)


if __name__ == "__main__":
    main()
