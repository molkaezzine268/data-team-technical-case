from click import command, option, pass_context, Context, Choice
from pathlib import Path
from enum import StrEnum, auto
import sqlite3
from textwrap import dedent

from ...sources.app import App
from ...sources.crm import CRM
from ...tools import SQLite

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
                with SQLite(source_folder_path / "crm.sqlite") as sqlite:
                    _extract_customers(crm, sqlite)

            case Source.APP:
                print("Extract App data...")
                app = App(faker=context.obj.faker)
                with SQLite(source_folder_path / "app.sqlite") as sqlite:
                    _extract_users(app, sqlite)
                    _extract_job_contracts(app, sqlite)
                    _extract_clients(app, sqlite)
                    _extract_invoices(app, sqlite)
                
            case _:
                raise Exception(f"Unknown source! ")
            

def _extract_users(app: App, sqlite: SQLite) -> None:
    sqlite.create_table_and_insert_values(
        "users",
        dedent("""
            CREATE TABLE
                {table_name} (
                    id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL
                )        
        """),
        dedent("""
            INSERT INTO 
                {table_name} (
                    id,
                    first_name,
                    last_name,
                    email
                )
            VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """),
        [
            (
                f"{user.id}", 
                user.first_name, 
                user.last_name, 
                user.email,
            )
            for user in app.list_users()
        ],
    )


def _extract_job_contracts(app: App, sqlite: SQLite) -> None:
    sqlite.create_table_and_insert_values(
        "job_contracts",
        dedent("""\
            CREATE TABLE
                {table_name} (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    entity TEXT NOT NULL,
                    start_date DATE,
                    end_date DATE
                )        
        """),
        dedent("""\
            INSERT INTO 
                {table_name} (
                    id,
                    user_id,
                    entity,
                    start_date,
                    end_date
                )
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """),
        [
            (
                f"{job_contract.id}", 
                f"{job_contract.user.id}", 
                f"{job_contract.entity}", 
                job_contract.start_date.format("YYYY-MM-DD"),
                end_date.format("YYYY-MM-DD") if ( end_date := job_contract.end_date ) else None
            )
            for job_contract in app.list_job_contracts()
        ],
    )

def _extract_clients(app: App, sqlite: SQLite) -> None:
    sqlite.create_table_and_insert_values(
        "clients",
        dedent("""\
            CREATE TABLE
                {table_name} (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                )        
        """),
        dedent("""\
            INSERT INTO 
                {table_name} (
                    id,
                    name
                )
            VALUES (
                ?,
                ?
            )
        """),
        [
            (
                f"{client.id}", 
                client.name,
            )
            for client in app.list_clients()
        ],
    )


def _extract_invoices(app: App, sqlite: SQLite) -> None:
    sqlite.create_table_and_insert_values(
        "invoices",
        dedent("""
            CREATE TABLE
                {table_name} (
                    id TEXT PRIMARY KEY,
                    job_contract_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    reference TEXT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    issue_date DATE NOT NULL
                )        
        """),
        dedent("""
            INSERT INTO 
                {table_name} (
                    id,
                    job_contract_id,
                    client_id,
                    reference,
                    amount,
                    issue_date
                )
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """),
        [
            (
                f"{invoice.id}", 
                f"{invoice.job_contract.id}", 
                f"{invoice.client.id}", 
                invoice.reference,
                f"{invoice.amount}",
                invoice.issue_date.format("YYYY-MM-DD"),
            )
            for invoice in app.list_invoices()
        ],
    )


def _extract_customers(crm: CRM, sqlite: SQLite) -> None:
    sqlite.create_table_and_insert_values(
        "customers",
        dedent("""
            CREATE TABLE
                {table_name} (
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    satisfaction_score INTEGER
                )        
        """),
        dedent("""
            INSERT INTO 
                {table_name} (
                    last_name,
                    first_name,
                    email,
                    satisfaction_score
                )
            VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """),
        [
            (
                customer.last_name, 
                customer.first_name, 
                customer.email,
                customer.satisfaction_score,
            )
            for customer in crm.list_customers()
        ],
    )