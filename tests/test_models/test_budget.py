import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget

@pytest.fixture
def repo():
    return MemoryRepository()

def test_create_with_full_args_list():
    b = Budget(period=2, amount=100, pk=1)
    assert b.period == 2
    assert b.amount == 100

def test_create_brief():
    b = Budget(1, 100)
    assert b.period == 1
    assert b.amount == 100


def test_can_add_to_repo(repo):
    b = Budget(100, 1)
    pk = repo.add(b)
    assert b.pk == pk