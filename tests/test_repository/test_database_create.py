import pytest
import sqlite3
from bookkeeper.repository.database_create import DatabaseConnection

@pytest.fixture
def db_connection():
    db_name = 'lovely.db'
    return DatabaseConnection(db_name)

def test_execute_query_cat(db_connection):
    # Проверяем, что метод execute_query создает таблицу Category
    db_connection.execute_query('''
            CREATE TABLE IF NOT EXISTS Category (
                name TEXT,
                parent INTEGER,
                pk INTEGER PRIMARY KEY)''')
    cursor = db_connection.conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="Category"')
    result = cursor.fetchone()
    assert result is not None

def test_execute_query_exp(db_connection):
    # Проверяем, что метод execute_query создает таблицу Expense
    db_connection.execute_query('''
            CREATE TABLE IF NOT EXISTS Expense (
                amount INTEGER,
                category INTEGER,
                expense_date DATE,
                comment TEXT,
                pk INTEGER PRIMARY KEY,
                FOREIGN KEY (category) REFERENCES Category(name))''')
    cursor = db_connection.conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="Expense"')
    result = cursor.fetchone()
    assert result is not None

def test_execute_query_bud(db_connection):
    # Проверяем, что метод execute_query создает таблицу Budget
    db_connection.execute_query('''
            CREATE TABLE IF NOT EXISTS Budget (
                period INTEGER,
                amount INTEGER,            
                pk INTEGER PRIMARY KEY)''')
    cursor = db_connection.conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="Budget"')
    result = cursor.fetchone()
    assert result is not None
def test_execute_query_with_params(db_connection):
    # Проверяем, что метод execute_query с параметрами работает корректно
    query = "INSERT INTO Category (name, parent) VALUES (?, ?)"
    params = ("Category1", 0)
    db_connection.execute_query(query, params)
    cursor = db_connection.conn.cursor()
    cursor.execute('SELECT name FROM Category WHERE name="Category1"')
    result = cursor.fetchone()
    assert result is not None

def test_close_connection(db_connection):
    # Проверяем, что метод close_connection закрывает соединение с базой данных
    db_connection.close_connection()
    with pytest.raises(sqlite3.ProgrammingError):
        db_connection.execute_query('SELECT 1')