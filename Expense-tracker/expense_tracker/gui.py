import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from typing import Optional

from .services import (
    list_expenses,
    add_expense,
    update_expense,
    delete_expense,
)
from .models import Expense
from .insights import monthly_summary


class ExpenseDialog(tk.Toplevel):
    def __init__(self, master, title="Add Expense", expense: Optional[dict] = None):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)

        self.result = None

        tk.Label(self, text="Amount:").grid(row=0, column=0, sticky="e")
        self.amount_var = tk.StringVar(value=str(expense.get("amount") if expense else ""))
        tk.Entry(self, textvariable=self.amount_var).grid(row=0, column=1)

        tk.Label(self, text="Category:").grid(row=1, column=0, sticky="e")
        self.category_var = tk.StringVar(value=expense.get("category") if expense else "")
        tk.Entry(self, textvariable=self.category_var).grid(row=1, column=1)

        tk.Label(self, text="Note:").grid(row=2, column=0, sticky="e")
        self.note_var = tk.StringVar(value=expense.get("note") if expense else "")
        tk.Entry(self, textvariable=self.note_var).grid(row=2, column=1)

        tk.Label(self, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")
        self.date_var = tk.StringVar(value=expense.get("date") if expense else date.today().isoformat())
        tk.Entry(self, textvariable=self.date_var).grid(row=3, column=1)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=6)
        tk.Button(btn_frame, text="OK", width=10, command=self.on_ok).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Cancel", width=10, command=self.destroy).pack(side="left")

        self.bind('<Return>', lambda e: self.on_ok())
        self.bind('<Escape>', lambda e: self.destroy())
        self.grab_set()
        self.wait_window()

    def on_ok(self):
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError("Amount must be > 0")
        except Exception as e:
            messagebox.showerror("Invalid input", f"Amount error: {e}")
            return

        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("Invalid input", "Category is required")
            return

        note = self.note_var.get().strip()
        date_val = self.date_var.get().strip()

        self.result = {
            "amount": amount,
            "category": category,
            "note": note,
            "date": date_val,
        }
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("750x400")

        # Toolbar
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x", padx=6, pady=6)

        tk.Button(toolbar, text="Add", command=self.add_expense).pack(side="left")
        tk.Button(toolbar, text="Edit", command=self.edit_selected).pack(side="left")
        tk.Button(toolbar, text="Remove", command=self.remove_selected).pack(side="left")
        tk.Button(toolbar, text="Summary", command=self.show_summary).pack(side="left")
        tk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")

        tk.Label(toolbar, text="Month:").pack(side="left", padx=(10, 2))
        self.month_var = tk.StringVar()
        tk.Entry(toolbar, width=10, textvariable=self.month_var).pack(side="left")

        tk.Label(toolbar, text="Limit:").pack(side="left", padx=(8, 2))
        self.limit_var = tk.StringVar()
        tk.Entry(toolbar, width=6, textvariable=self.limit_var).pack(side="left")

        # Treeview
        cols = ("id", "date", "category", "amount", "note")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("note", text="Note")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("date", width=100)
        self.tree.column("category", width=120)
        self.tree.column("amount", width=100, anchor="e")
        self.tree.column("note", width=300)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        self.refresh()

    def _get_filters(self):
        month = self.month_var.get().strip() or None
        limit = None
        if self.limit_var.get().strip():
            try:
                limit = int(self.limit_var.get())
            except Exception:
                messagebox.showerror("Invalid limit", "Limit must be an integer")
                return None, None
        return month, limit

    def refresh(self):
        month, limit = self._get_filters()
        if month is None and self.month_var.get().strip():
            return

        for i in self.tree.get_children():
            self.tree.delete(i)

        rows = list_expenses(month=month, limit=limit)
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["date"], r["category"].capitalize(), f"{r['amount']:.2f}", r["note"]))

    def add_expense(self):
        dlg = ExpenseDialog(self, "Add Expense")
        if not dlg.result:
            return
        exp = Expense(amount=dlg.result["amount"], category=dlg.result["category"], note=dlg.result["note"], date=dlg.result["date"]) 
        try:
            add_expense(exp)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Please select an expense first.")
            return None
        item = self.tree.item(sel[0])
        return int(item["values"][0])

    def edit_selected(self):
        eid = self._selected_id()
        if eid is None:
            return

        # fetch the record (list_expenses with limit and then find id) - simple approach
        rows = list_expenses(limit=5000)
        rec = None
        for r in rows:
            if r["id"] == eid:
                rec = r
                break
        if not rec:
            messagebox.showerror("Not found", "Expense not found")
            return

        dlg = ExpenseDialog(self, "Edit Expense", expense=rec)
        if not dlg.result:
            return
        try:
            ok = update_expense(eid, **dlg.result)
            if ok:
                self.refresh()
            else:
                messagebox.showerror("Error", "Update failed")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_selected(self):
        eid = self._selected_id()
        if eid is None:
            return
        if not messagebox.askyesno("Confirm", f"Delete expense {eid}?"):
            return
        ok = delete_expense(eid)
        if ok:
            self.refresh()
        else:
            messagebox.showerror("Error", "Delete failed or id not found")

    def show_summary(self):
        month = self.month_var.get().strip() or None
        if month:
            rows = list_expenses(month=month)
            title = f"Month: {month}"
        else:
            rows = list_expenses()
            title = "All-time Summary"

        total, by_category = monthly_summary(rows)
        txt = f"{title}\n\nTotal: {total:.2f}\n\nBy category:\n"
        for k, v in by_category.items():
            txt += f"{k.capitalize():12} {v:.2f}\n"
        messagebox.showinfo("Summary", txt)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
