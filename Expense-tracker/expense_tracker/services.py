from datetime import date
from .db import get_connection
from .models import Expense


def add_expense(expense: Expense):
    if expense.amount <= 0:
        raise ValueError("Amount must be greater than zero")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (date, amount, category, note)
        VALUES (?, ?, ?, ?)
        """,
        (expense.date, expense.amount, expense.category.lower(), expense.note),
    )

    conn.commit()
    conn.close()


def fetch_expenses_for_month(month: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE date LIKE ?
        """,
        (f"{month}%",),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
