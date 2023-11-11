from database.sqlite3 import SQLiteDB
from properties import const


db = SQLiteDB(lambda: const("dbMainPath"), lambda: const("dbMainTableName"))
