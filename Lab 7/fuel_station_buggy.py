"""Original intentionally buggy Lab 7 implementation (pre-fix demonstration)."""


def parse_purchase(text):
    grade, litres = text.split(':')
    return grade.strip().title(), float(litres)


def volume_average(volumes_csv):
    values = [int(r) for r in volumes_csv.split(',')]
    return sum(values) // len(values)


def payable_bill(text):
    bill, discount = text.split('|')
    total = float(bill) * 1.18 - float(discount)
    return max(total, 0)
