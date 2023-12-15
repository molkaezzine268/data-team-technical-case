from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import yaml
from os import environ


class DBT:

    def __init__(self, project_folder_path: Path, duckdb_file_path: Path, log_folder_path: Path, target_folder_path: Path):
        self._project_folder_path = project_folder_path
        self._duckdb_file_path = duckdb_file_path
        self._log_folder_path = log_folder_path
        self._target_folder_path = target_folder_path

    def build(self, /, *, 
        selector: str | None = None,
        select: str | list[str] | None
    ) -> None:
        selector_args = [f"--selector={selector}"] if selector else []

        match select:
            case None:
                select_args = []
            case str():
                select_args = [f"--select={select}"]
            case list():
                select_args = [f"--select={value}" for value in select]

        profile_args = ["--profile=transient", "--target=transient"]
        
        command = ["dbt", "build"] + selector_args + select_args + profile_args

        with TemporaryDirectory(prefix="dbt_") as temp_folder_path:
            temp_folder_path = Path(temp_folder_path)

            profiles = {
                "transient": {
                    "outputs": {
                        "transient": {
                            "type": "duckdb",
                            "path": f"{self._duckdb_file_path.absolute()}",
                        }
                    },
                    "target": "transient",
                },
            }
            with ( temp_folder_path / "profiles.yml" ).open("w") as stream:
                yaml.dump(profiles, stream)

            process = run(
                ["dbt", "deps"], 
                env=environ | {
                    "DBT_PROJECT_DIR": f"{self._project_folder_path}",
                    "DBT_PROFILES_DIR": f"{temp_folder_path}",
                    "DBT_TARGET_PATH": f"{self._target_folder_path}",
                    "DBT_LOG_PATH": f"{self._log_folder_path}",
                }
            )
            if process.returncode != 0:
                raise RuntimeError(f"DBT command failed with exit code {process.returncode}!")

            process = run(
                command, 
                env=environ | {
                    "DBT_PROJECT_DIR": f"{self._project_folder_path}",
                    "DBT_PROFILES_DIR": f"{temp_folder_path}",
                    "DBT_TARGET_PATH": f"{self._target_folder_path}",
                    "DBT_LOG_PATH": f"{self._log_folder_path}",
                }
            )

            if process.returncode != 0:
                raise RuntimeError(f"DBT command failed with exit code {process.returncode}!")

    