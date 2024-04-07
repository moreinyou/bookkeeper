from dataclasses import dataclass

@dataclass(slots=True)
class Budget:
    """ в этом классе описано как должен выглядеть бюджет, хранит период, сумму и пк"""
    period: int
    amount: int
    pk: int = 0

