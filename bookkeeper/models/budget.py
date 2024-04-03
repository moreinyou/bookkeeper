from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass(slots=True)
class Budget:
    category: int
    amount: int
    term: timedelta = field(default=timedelta(days=1))
    pk: int = 0