from pathlib import Path
import duckdb
from textwrap import dedent


class DuckDB:

    def __init__(self, file_path: Path):
        self._file_path = file_path

    def __enter__(self):
        self._connection = duckdb.connect(database=f"{self._file_path}")
        self._connection.execute("INSTALL sqlite")
        self._connection.execute("LOAD sqlite")
        return self
    
    def __exit__(self, *args, **kwargs):
        self._connection.close()
        self._connection = None
    
    def attach(self, sqlite_file_path: Path, schema: str) -> None:
        if ( connection := self._connection ):
            connection.execute(
                dedent("""\
                    ATTACH 
                        '{sqlite_file_path}' 
                    AS 
                        {schema} (TYPE sqlite)
                """).format(sqlite_file_path=sqlite_file_path, schema=schema)
            )

    def create_schema(self, schema: str) -> None:
        if ( connection := self._connection ):
            connection.execute(
                dedent("""\
                    CREATE SCHEMA IF NOT EXISTS 
                        {schema}
                """).format(schema=schema)
            )

    def execute(self, sql: str) -> None:
        if ( connection := self._connection ):
            connection.execute(sql)