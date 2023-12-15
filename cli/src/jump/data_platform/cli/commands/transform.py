from click import command, option, pass_context, Context, Choice
from subprocess import run
from pathlib import Path
from halo import Halo

from ...tools import DBT, DuckDB

from .layer import Layer


@command()
@option(
    "--lakehouse-folder", "lakehouse_folder_path", 
    type=Path, 
)
@option(
    "--dbt-target-folder", "dbt_target_folder_path",
    type=Path,
)
@option(
    "--dbt-project-folder", "dbt_project_folder_path",
    type=Path,
)
@option(
    "--dbt-log-folder", "dbt_log_folder_path",
    type=Path,
)
@option(
    "--layer", "layers", 
    type=Choice([source.value for source in Layer]),
    callback=lambda context, param, values: [Layer(value) for value in values],
    multiple=True,
    default=[source.value for source in Layer],
)
@pass_context
def transform(
    context: Context, 
    lakehouse_folder_path: Path | None, 
    dbt_project_folder_path: Path | None,
    dbt_target_folder_path: Path | None, 
    dbt_log_folder_path: Path | None, 
    layers: list[Layer]
):
    lakehouse_folder_path = lakehouse_folder_path or context.obj.data_folder_path / "lakehouse"
    duckdb_file_path = lakehouse_folder_path / "lakehouse.duckdb"
    with DuckDB(duckdb_file_path) as duckdb:
        for layer in layers:
            duckdb.create_schema(f"{layer}")

    dbt_project_folder_path = dbt_project_folder_path or context.obj.project_folder_path / "dbt"

    dbt_target_folder_path = dbt_target_folder_path or context.obj.data_folder_path / "dbt"
    dbt_target_folder_path.mkdir(parents=True, exist_ok=True)
    
    dbt_log_folder_path = dbt_log_folder_path or context.obj.log_folder_path / "dbt"
    dbt_log_folder_path.mkdir(parents=True, exist_ok=True)

    spinner = Halo(text=f"Transforming layers using DBT... ", spinner="dots")
    spinner.start()
    try:
        dbt = DBT(
            project_folder_path=dbt_project_folder_path, 
            duckdb_file_path=duckdb_file_path,
            log_folder_path=dbt_log_folder_path,
            target_folder_path=dbt_target_folder_path,
        )
        dbt.build(select=[layer.value for layer in layers])
        spinner.stop_and_persist(symbol="✅".encode('utf-8'), text=f"Successfully transformed layers using DBT! ")
    except Exception as exception:
        spinner.stop_and_persist(symbol="❌".encode('utf-8'), text=f"Unable to transform layers using DBT! ")
        raise exception