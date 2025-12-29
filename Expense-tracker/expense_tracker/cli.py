import argparse
from datetime import date

from .db import init_db
from .models import Expense
from .services import (
    add_expense,
    fetch_expenses_for_month,
    fetch_all_expenses,
    list_expenses,
    delete_expense,
    update_expense,
)
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

    # LIST COMMAND
    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("--month", required=False, help="YYYY-MM")
    list_parser.add_argument("--limit", type=int, required=False, help="Max number to show")

    # REMOVE COMMAND
    remove_parser = subparsers.add_parser("remove", help="Remove expense by id")
    remove_parser.add_argument("id", type=int, help="Expense id")

    # EDIT COMMAND
    edit_parser = subparsers.add_parser("edit", help="Edit expense by id")
    edit_parser.add_argument("id", type=int, help="Expense id")
    edit_parser.add_argument("--amount", type=float)
    edit_parser.add_argument("--category")
    edit_parser.add_argument("--note")
    edit_parser.add_argument("--date")

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
        return

    elif args.command == "summary":
        # Determine which expenses to load
        if args.month:
            expenses = fetch_expenses_for_month(args.month)
            title = f"Month: {args.month}"
        else:
            expenses = fetch_all_expenses()
            title = "All-time Summary"

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
        return

    elif args.command == "list":
        expenses = list_expenses(month=getattr(args, "month", None), limit=getattr(args, "limit", None))
        if not expenses:
            print("No expenses found")
            return
        print()
        print(f"Listing expenses{(' for ' + args.month) if getattr(args, 'month', None) else ''}")
        print("-" * 60)
        print(f"{'ID':>3} {'Date':10} {'Category':12} {'Amount':>10}  Note")
        for r in expenses:
            print(f"{r['id']:3} {r['date']:10} {r['category']:<12} ₹{r['amount']:8.2f}  {r['note']}")
        return

    elif args.command == "remove":
        deleted = delete_expense(args.id)
        if deleted:
            print(f"Expense {args.id} deleted.")
        else:
            print(f"Expense with id {args.id} not found.")
        return

    elif args.command == "edit":
        fields = {}
        for attr in ("amount", "category", "note", "date"):
            val = getattr(args, attr, None)
            if val is not None:
                fields[attr] = val

        if not fields:
            print("No fields provided to update. Use --amount/--category/--note/--date")
            return

        try:
            updated = update_expense(args.id, **fields)
        except ValueError as e:
            print("Error:", e)
            return

        if updated:
            print(f"Expense {args.id} updated.")
        else:
            print(f"Expense with id {args.id} not found.")
        return


if __name__ == "__main__":
    main()
