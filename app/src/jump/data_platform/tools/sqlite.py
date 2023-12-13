from pathlib import Path
import sqlite3


class SQLite:

    def __init__(self, file_path: Path):
        self._file_path = file_path

    def __enter__(self):
        self._connection = sqlite3.connect(self._file_path)
        return self
    
    def __exit__(self, *args, **kwargs):
        if ( connection := self._connection ):
            connection.close()
        
        self._connection = None

    def create_table_and_insert_values(self, table_name, create_table_sql, insert_sql, values):
        if ( connection := self._connection):
            connection.execute("DROP TABLE IF EXISTS {table_name}".format(table_name=table_name))
            connection.execute(create_table_sql.format(table_name=table_name))
            connection.executemany(insert_sql.format(table_name=table_name), values)
            connection.commit()