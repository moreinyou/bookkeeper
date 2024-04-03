import sqlite3
from typing import Any

from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.cls = cls

    def add(self, obj: T) -> int:

        field_names = list(self.fields.keys())
        field_names.remove('pk')
        names = ', '.join(field_names)
        p = ', '.join("?" * len(field_names))
        values = [getattr(obj, x) for x in field_names]

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            #cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'INSERT INTO {self.table_name} ({names}) VALUES ({p})', values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {self.table_name} WHERE pk = {pk}')
            row = cur.fetchone()
            obj = self.cls(*row)
        con.close()
        return obj


    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'SELECT * FROM {self.table_name} ')
            row = cur.fetchall()
            obj_list = []
            for val in row:
                obj = self.cls(*val)
                obj_list.append(obj)
        con.close()
        if where is None:
            return obj_list
        else:
            return [obj for obj in obj_list
                    if all(getattr(obj, attr) == value for attr, value in where.items())]


    def update(self, obj: T) -> None:
        ''' этот метод должен заменить один объект на другой'''
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')

        field_names = list(self.fields.keys())
        field_names.remove('pk')
        names = ', '.join(field_names)
        p = ', '.join("?" * len(field_names))
        values = [getattr(obj, x) for x in field_names]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            #cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'UPDATE {self.table_name} SET ({names}) = ({p}) WHERE pk = {obj.pk}', values)
        return None
        con.close()

    def delete(self, obj: T) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {obj.pk}')
        return None
        con.close()