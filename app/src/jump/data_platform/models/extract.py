#!/usr/bin/env python

from csv import DictWriter
from pathlib import Path

from store import Store


if __name__ == "__main__":
    store = Store(seed=42)
    (users, job_contracts, clients, invoices) = store.load_all()

    with (Path(__file__).parent.parent / "data" / "users.csv").open("w") as f:
        column_names = ["id", "first_name", "last_name", "email"]
        writer = DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        for user in users:
            writer.writerow({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            })

    with (Path(__file__).parent.parent / "data" / "job_contracts.csv").open("w") as f:
        column_names = ["id", "user_id", "entity", "start_date", "end_date"]
        writer = DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        for job_contract in job_contracts:
            writer.writerow({
                "id": job_contract.id,
                "user_id": job_contract.user.id,
                "entity": f"{job_contract.entity}",
                "start_date": job_contract.start_date.format("YYYY-MM-DD"),
                "end_date": end_date.format("YYYY-MM-DD") if ( end_date := job_contract.end_date ) else None,
            })

    with (Path(__file__).parent.parent / "data" / "clients.csv").open("w") as f:
        column_names = ["id", "name"]
        writer = DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        for client in clients:
            writer.writerow({
                "id": client.id,
                "name": client.name,
            })

    with (Path(__file__).parent.parent / "data" / "invoices.csv").open("w") as f:
        column_names = ["id", "job_contract_id", "client_id", "reference", "amount"]
        writer = DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        for invoice in invoices:
            writer.writerow({
                "id": invoice.id,
                "job_contract_id": invoice.job_contract.id,
                "client_id": invoice.client.id,
                "reference": invoice.reference,
                "amount": invoice.amount,
            })