from click import command, option, Choice, Context, pass_context
from pathlib import Path
from textwrap import dedent

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
            duckdb.attach(
                source_folder_path / f"{source}.sqlite", 
                f"source__{source}",
            )

            match source:
                case Source.CRM:
                    ...
                
                case Source.APP:
                    for table_name in ["users", "clients", "job_contracts", "invoices"]:
                        duckdb.execute(dedent("""\
                            CREATE TABLE IF NOT EXISTS 
                                sources.app__{table_name} 
                            AS 
                                SELECT 
                                    * 
                                FROM 
                                    source__app.{table_name}""").format(table_name=table_name)
                        )
                
                case _:
                    raise Exception(f"Unknown source! ")

        