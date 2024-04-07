"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime, time

def date_withouttime():
    current_day = datetime.date(datetime.combine(datetime.now(), time.min))
    return current_day

@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: datetime = field(default_factory = date_withouttime)
    comment: str = ''
    pk: int = 0
