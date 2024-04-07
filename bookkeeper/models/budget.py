from dataclasses import dataclass

@dataclass(slots=True)
class Budget:
    period: int
    amount: int
    pk: int = 0

