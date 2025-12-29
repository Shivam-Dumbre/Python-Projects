from dataclasses import dataclass
from datetime import date


@dataclass
class Expense:
    amount: float
    category: str
    note: str = ""
    date: str = date.today().isoformat()
