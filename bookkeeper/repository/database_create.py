import sqlite3

class DatabaseConnection():
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()


db_name='lovely.db'
basa_for_everything = DatabaseConnection(db_name)

basa_for_everything.execute_query('''
        CREATE TABLE IF NOT EXISTS Category (
            name TEXT,
            parent INTEGER,
            pk INTEGER PRIMARY KEY)''')

basa_for_everything.execute_query('''
        CREATE TABLE IF NOT EXISTS Expense (
            amount INTEGER,
            category INTEGER,
            expense_date DATE,
            comment TEXT,
            pk INTEGER PRIMARY KEY,
            FOREIGN KEY (category) REFERENCES Category(name))''')

basa_for_everything.execute_query('''
        CREATE TABLE IF NOT EXISTS Budget (
            period DATE,
            amount INTEGER,            
            pk INTEGER PRIMARY KEY)''')

basa_for_everything.close_connection()