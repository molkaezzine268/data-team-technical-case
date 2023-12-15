from typing import Any, Callable, TypeVar
from click import command, option, pass_context, Context, Choice
from pathlib import Path
from enum import StrEnum, auto
from textwrap import dedent
from csv import DictWriter

from ...sources.app import App
from ...sources.crm import CRM

from .source import Source



@command()
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
def extract(context: Context, source_folder_path: Path | None, sources: list[Source]):
    source_folder_path = source_folder_path or context.obj.data_folder_path / "sources"
    source_folder_path.mkdir(parents=True, exist_ok=True)
    
    app = App(faker=context.obj.faker)
    users = app.list_users()
    crm = CRM(users=users, faker=context.obj.faker)

    for source in sources:
        match source:
            case Source.CRM:
                print("Extract CRM data...")
                write_csv_file(
                    source_folder_path / "customers.csv",
                    crm.list_customers(),
                    ["last_name", "first_name", "email", "satisfaction_score"],
                    lambda customer: {
                        "last_name": customer.last_name,
                        "first_name": customer.first_name,
                        "email": customer.email,
                        "satisfaction_score": customer.satisfaction_score,
                    }
                )

            case Source.APP:
                print("Extract App data...")
                app = App(faker=context.obj.faker)

                write_csv_file(
                    source_folder_path / "users.csv", 
                    app.list_users(), 
                    ["id", "first_name", "last_name", "email"], 
                    lambda user: {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                    }
                )
                
                write_csv_file(
                    source_folder_path / "job_contracts.csv", 
                    app.list_job_contracts(), 
                    ["id", "user_id", "entity", "start_date", "end_date"], 
                    lambda job_contract: {
                        "id": job_contract.id,
                        "user_id": job_contract.user.id,
                        "entity": job_contract.entity,
                        "start_date": job_contract.start_date.format("YYYY-MM-DD"),
                        "end_date": job_contract.end_date.format("YYYY-MM-DD") if ( end_date := job_contract.end_date ) else None,
                    }
                )

                write_csv_file(
                    source_folder_path / "clients.csv", 
                    app.list_clients(), 
                    ["id", "name"], 
                    lambda client: {
                        "id": client.id,
                        "name": client.name,
                    }
                )

                write_csv_file(
                    source_folder_path / "invoices.csv", 
                    app.list_invoices(), 
                    ["id", "job_contract_id", "client_id", "reference", "amount", "issue_date"], 
                    lambda invoice: {
                        "id": invoice.id,
                        "job_contract_id": invoice.job_contract.id,
                        "client_id": invoice.client.id,
                        "reference": invoice.reference,
                        "amount": invoice.amount,
                        "issue_date": invoice.issue_date.format("YYYY-MM-DD"),
                    }
                )
                
            case _:
                raise Exception(f"Unknown source! ")


T = TypeVar("T")

def write_csv_file(
    file_path: Path, 
    rows: list[T], 
    column_names: list[str], 
    transform: Callable[[T], dict[str, Any]],
) -> None:
    with file_path.open("w") as f:
        writer = DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        writer.writerows([transform(row) for row in rows])