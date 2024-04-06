import pytest


from dataclasses import dataclass, field
from datetime import datetime, timedelta

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget


@pytest.fixture
def repo():
    return MemoryRepository()

def test_budget_init(repo):
    budget = Budget(1, 100)
    assert budget.category == 1
    assert budget.amount == 100
    assert budget.term == timedelta(days=1)
    assert budget.pk == 0

def test_budget_custom_term(repo):
    custom_term = timedelta(days=30)
    budget = Budget(1, 100, term=custom_term)
    assert budget.category == 1
    assert budget.amount == 100
    assert budget.term == custom_term
    assert budget.pk == 0

def test_budget_pk(repo):
    budget = Budget(1, 100, pk=5)
    assert budget.category == 1
    assert budget.amount == 100
    assert budget.term == timedelta(days=1)
    assert budget.pk == 5