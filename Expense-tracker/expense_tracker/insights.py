from collections import defaultdict


def monthly_summary(expenses):
    total = 0
    by_category = defaultdict(float)

    for exp in expenses:
        total += exp["amount"]
        by_category[exp["category"]] += exp["amount"]

    return total, by_category
