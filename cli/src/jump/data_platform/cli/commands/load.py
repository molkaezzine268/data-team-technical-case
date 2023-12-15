from click import command, option, Choice, Context, pass_context
from pathlib import Path
from textwrap import dedent
from halo import Halo

from ...tools import DuckDB

from .source import Source


@command()
@option("--lakehouse-folder", "-l", "lakehouse_folder_path", type=Path)
@option("--source-folder", "-e", "source_folder_path", type=Path)
@option(
    "--sources", 
    "-s", 
    "sources", 
    type=Choice([source.value for source in Source]),
    callback=lambda context, param, values: [Source(value) for value in values],
    multiple=True,
    default=[source.value for source in Source]
)
@pass_context
def load(context: Context, source_folder_path: Path | None, lakehouse_folder_path: Path | None, sources: list[Source]):
    source_folder_path = source_folder_path or context.obj.data_folder_path / "sources"
    
    lakehouse_folder_path = lakehouse_folder_path or context.obj.data_folder_path / "lakehouse"
    lakehouse_folder_path.mkdir(parents=True, exist_ok=True)

    with DuckDB(lakehouse_folder_path / "lakehouse.duckdb") as duckdb:
        duckdb.create_schema("sources")
        for source in sources:
            match source:
                case Source.CRM:
                    for table_name in ["customers"]:
                        spinner = Halo(text=f"Loading CRM table {table_name} to the Lakehouse... ", spinner="dots")
                        spinner.start()
                        duckdb.execute(dedent("""\
                            CREATE TABLE IF NOT EXISTS 
                                sources.crm__{table_name} 
                            AS 
                                SELECT 
                                    * 
                                FROM 
                                    read_csv_auto('{csv_file_path}', header = true)
                        """).format(table_name=table_name, csv_file_path=source_folder_path / f"{table_name}.csv"))
                        spinner.stop_and_persist(symbol="✅".encode('utf-8'), text=f"Successfully loaded CRM table {table_name} to the Lakehouse! ")
                
                case Source.APP:
                    for table_name in ["users", "clients", "job_contracts", "invoices"]:
                        spinner = Halo(text=f"Loading App table {table_name} to the Lakehouse... ", spinner="dots")
                        spinner.start()
                        duckdb.execute(dedent("""\
                            CREATE TABLE IF NOT EXISTS 
                                sources.app__{table_name} 
                            AS 
                                SELECT 
                                    * 
                                FROM 
                                    read_csv_auto('{csv_file_path}', header = true)
                        """).format(table_name=table_name, csv_file_path=source_folder_path / f"{table_name}.csv"))
                        spinner.stop_and_persist(symbol="✅".encode('utf-8'), text=f"Successfully loaded App table {table_name} to the Lakehouse! ")
                
                case _:
                    raise Exception(f"Unknown source! ")

        