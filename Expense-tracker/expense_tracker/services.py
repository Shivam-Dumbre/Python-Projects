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


def fetch_all_expenses():
    """Return all expenses ordered by date."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date")
    rows = cursor.fetchall()
    conn.close()
    return rows


def list_expenses(month: str | None = None, limit: int | None = None):
    """Return expenses optionally filtered by month and limited."""
    conn = get_connection()
    cursor = conn.cursor()

    params = ()
    if month:
        query = "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC"
        params = (f"{month}%",)
    else:
        query = "SELECT * FROM expenses ORDER BY date DESC"

    if limit:
        query += " LIMIT ?"
        params = params + (limit,)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_expense(expense_id: int) -> bool:
    """Delete an expense by id. Return True if deleted."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    changed = cursor.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def update_expense(expense_id: int, **fields) -> bool:
    """Update fields of an expense. Allowed fields: date, amount, category, note."""
    allowed = {"date", "amount", "category", "note"}
    set_parts = []
    params = []

    for key, val in fields.items():
        if key not in allowed:
            continue
        if key == "amount":
            try:
                val = float(val)
            except Exception:
                raise ValueError("Amount must be a number")
            if val <= 0:
                raise ValueError("Amount must be greater than zero")
        if key == "category" and isinstance(val, str):
            val = val.lower()
        set_parts.append(f"{key} = ?")
        params.append(val)

    if not set_parts:
        raise ValueError("No valid fields provided to update")

    params.append(expense_id)
    query = f"UPDATE expenses SET {', '.join(set_parts)} WHERE id = ?"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(params))
    changed = cursor.rowcount
    conn.commit()
    conn.close()
    return changed > 0
