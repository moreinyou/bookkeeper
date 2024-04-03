from bookkeeper.repository.sqlite_repository import SQLiteRepository

import sqlite3
import pytest
from unittest.mock import Mock


@pytest.fixture
def db_connection():
    con = sqlite3.connect(':memory:')
    yield con
    con.close()


def test_add(db_connection):
    class MockModel:
        def __init__(self, pk, field1, field2):
            self.pk = pk
            self.field1 = field1
            self.field2 = field2

    mock_obj = MockModel(0, 'value1', 'value2')
    repo = SQLiteRepository(':memory:', MockModel)
    pk = repo.add(mock_obj)

    assert pk != 0  # Проверяем, что pk был установлен
    assert pk == mock_obj.pk  # Проверяем, что pk был установлен корректно

def test_get(db_connection):
    class MockModel:
        def __init__(self, pk, field1, field2):
            self.pk = pk
            self.field1 = field1
            self.field2 = field2

    mock_obj = MockModel(0, 'value1', 'value2')
    repo = SQLiteRepository(':memory:', MockModel)
    pk = repo.add(mock_obj)

    retrieved_obj = repo.get(pk)

    assert retrieved_obj.pk == pk  # Проверяем, что получен объект с правильным pk
    assert retrieved_obj.field1 == mock_obj.field1  # Проверяем, что поле field1 было получено
    assert retrieved_obj.field2 == mock_obj.field2  # Проверяем, что поле field2 было получено


def test_get_all(db_connection):
    class MockModel:
        def __init__(self, pk, field1, field2):
            self.pk = pk
            self.field1 = field1
            self.field2 = field2

    mock_obj1 = MockModel(0, 'value1', 'value2')
    mock_obj2 = MockModel(0, 'value3', 'value4')

    repo = SQLiteRepository(':memory:', MockModel)
    repo.add(mock_obj1)
    repo.add(mock_obj2)

    all_objs = repo.get_all()

    assert len(all_objs) == 2  # Проверяем, что получены все объекты
    # Дополнительные проверки можно добавить здесь


def test_update(db_connection):
    class MockModel:
        def __init__(self, pk, field1, field2):
            self.pk = pk
            self.field1 = field1
            self.field2 = field2

    mock_obj = MockModel(0, 'value1', 'value2')

    repo = SQLiteRepository(':memory:', MockModel)
    pk = repo.add(mock_obj)

    mock_obj.field1 = 'updated_value1'
    mock_obj.field2 = 'updated_value2'

    repo.update(mock_obj)

    updated_obj = repo.get(pk)

    assert updated_obj.field1 == 'updated_value1'  # Проверяем обновление поля field1
    assert updated_obj.field2 == 'updated_value2'  # Проверяем обновление поля field2


def test_delete(db_connection):
    class MockModel:
        def __init__(self, pk, field1, field2):
            self.pk = pk
            self.field1 = field1
            self.field2 = field2

    mock_obj = MockModel(0, 'value1', 'value2')

    repo = SQLiteRepository(':memory:', MockModel)
    pk = repo.add(mock_obj)

    repo.delete(mock_obj)

    deleted_obj = repo.get(pk)

    assert deleted_obj is None  # Проверяем, что объект был удален
