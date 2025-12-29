import argparse
from datetime import date

from .db import init_db
from .models import Expense
from .services import add_expense, fetch_expenses_for_month
from .insights import monthly_summary


def main():
    init_db()

    parser = argparse.ArgumentParser(
        prog="expense",
        description="Personal Expense Tracker",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ADD COMMAND
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--note", default="")
    add_parser.add_argument("--date", default=date.today().isoformat())

    # SUMMARY COMMAND
    summary_parser = subparsers.add_parser("summary", help="Monthly summary")
    summary_parser.add_argument("--month", required=False, help="YYYY-MM")

    args = parser.parse_args()

    if args.command == "add":
        expense = Expense(
            amount=args.amount,
            category=args.category,
            note=args.note,
            date=args.date,
        )
        add_expense(expense)
        print("Expense added successfully")

    elif args.command == "summary":
        print("DEBUG: summary command reached")

    if args.month:
        expenses = fetch_expenses_for_month(args.month)
        title = f"Month: {args.month}"
    else:
        expenses = fetch_all_expenses()
        title = "All-time Summary"

    print(f"DEBUG: expenses loaded -> {expenses}")

    total, by_category = monthly_summary(expenses)

    print(f"\n{title}")
    print("-" * 30)
    print(f"Total Spend: ₹{total:.2f}\n")


    print("By Category:")
    if not by_category:
            print("No expenses found")
    else:
            for cat, amt in by_category.items():
                print(f"{cat.capitalize():12} ₹{amt:.2f}")
