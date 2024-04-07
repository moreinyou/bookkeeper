from datetime import datetime

import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.expense import Expense, date_withouttime


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    e = Expense(amount=100, category=1, expense_date=date_withouttime(), comment='test', pk=1)
    assert e.amount == 100
    assert e.category == 1


def test_create_brief():
    e = Expense(100, 1)
    assert e.amount == 100
    assert e.category == 1


def test_can_add_to_repo(repo):
    e = Expense(100, 1)
    pk = repo.add(e)
    assert e.pk == pk

def test_date_withouttime():
    current_day = datetime.now()
    expected_day = datetime.date(current_day.year, current_day.month, current_day.day)
    actual_day = date_withouttime()
    assert actual_day == expected_day