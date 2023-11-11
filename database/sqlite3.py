from __future__ import annotations

from properties import const
from sqlite3 import Cursor
from database.interface import Database, User
import dataclasses as dc
from typing import get_type_hints
import sqlite3

CREATE_TABLE_SQL: str | None = None
CREATE_USER_SQL: tuple[str, tuple] | None = None

PY2SQL = {
    'int': 'INT',
    'str': 'TEXT',
    'bool': 'BOOLEAN'
}


def _annotations(duck: type):
    resolved = get_type_hints(duck)
    return map(lambda f: (f.name, resolved[f.name]), dc.fields(duck))


def _unfold_annotations(field: str, ty: type) -> dict[str, type]:
    if PY2SQL.get(ty.__name__) is not None:
        return {field: ty}
    if field != "":
        field += '_'
    result = {}
    for subfield, subty in _annotations(ty):
        result.update(_unfold_annotations(field + subfield, subty))
    return result


def _dataclass_from_sql(dataclass: type, sql: list):
    result = []
    for _field, ty in _annotations(dataclass):
        if PY2SQL.get(ty.__name__) is not None:
            result.append(sql.pop())
            continue
        result.append(_dataclass_from_sql(ty, sql))
    return dataclass(*result)


class SQLiteDB(Database):
    def __init__(self, path: str, name: str, user: type, default_values_for_new_users: dict[str, str] | None = None):
        self._path = path
        self._name = name
        self.__path = None
        self.__name = None
        self._new_user_defaults = default_values_for_new_users
        self._UFIELDS = _unfold_annotations("", user)

    @property
    def path(self):
        if self.__path is None:
            self.__path = self._path() if callable(self._path) else self._path
            del self._path
        return self.__path
    
    @property
    def name(self):
        if self.__name is None:
            self.__name = self._name() if callable(self._name) else self._name
            del self._name
        return self.__name

    def update_user(self, uid: int, **kwargs):
        if _fetch_user_or_none_if_nonpresent(uid, self.name, self.path, self._UFIELDS) is None:
            _create_user(uid, self.name, self.path, self._UFIELDS)
            if self._new_user_defaults is not None:
                self.update_user(uid, **self._new_user_defaults)
        update = ", ".join([(field + ' = ' + '"' + value.replace('"', '""') + '"') for field, value in kwargs.items()])
        _mutate(f'UPDATE {self.name} SET {update} WHERE uid = ?', self.path, (uid,))

    def fetch_user(self, uid: int):
        if (fetched := _fetch_user_or_none_if_nonpresent(uid, self.name, self.path, self._UFIELDS)) is None:
            _create_user(uid, self.name, self.path, self._UFIELDS)
            if self._new_user_defaults is not None:
                self.update_user(uid, **self._new_user_defaults)
            fetched = _fetch_user_or_none_if_nonpresent(uid, self.name, self.path, self._UFIELDS)
        return fetched


def _fetch_user_or_none_if_nonpresent(uid: int, name, path, UFIELDS) -> User | None:
    _create_table_if_not_exists(name, path, UFIELDS)
    if (fetched := _fetch(f"SELECT * FROM {name} WHERE uid=?", path, (uid,)).fetchone()) is None:
        return
    return _dataclass_from_sql(User, list(fetched)[::-1])


def _create_table_if_not_exists(name, path, UFIELDS):
    global CREATE_TABLE_SQL
    if CREATE_TABLE_SQL is None:
        fields = ', '.join(
            [f'{field} {PY2SQL[value.__name__]}{" PRIMARY KEY" if field == "uid" else ""}'
             for field, value in UFIELDS.items()])
        CREATE_TABLE_SQL = f"CREATE TABLE IF NOT EXISTS {name}({fields});"
    _mutate(CREATE_TABLE_SQL, path)


def _create_user(uid: int, name, path, UFIELDS):
    global CREATE_USER_SQL

    if CREATE_USER_SQL is None:
        fields, values = zip(*[(field, ty()) for field, ty in UFIELDS.items() if field != 'uid'])
        placeholders = ('?,' * len(UFIELDS))[:-1]
        CREATE_USER_SQL = f"INSERT INTO {name}" \
                          f" (uid, {', '.join(fields)}) VALUES({placeholders});", values
    _mutate(CREATE_USER_SQL[0], path, (uid, *CREATE_USER_SQL[1]))


def _mutate(request: str, path, *args, **kwargs):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(request, *args, **kwargs)
    con.commit()
    cur.close()


def _fetch(request: str, path, *args, **kwargs) -> Cursor:
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur.execute(request, *args, **kwargs)
