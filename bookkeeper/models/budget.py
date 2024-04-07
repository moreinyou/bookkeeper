from dataclasses import dataclass, field
from datetime import timedelta

@dataclass(slots=True)
class Budget:
    amount: int
    term: timedelta = field(default=timedelta(days=1))
    pk: int = 0

