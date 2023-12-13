#!/usr/bin/env python

from typing import Generator

from pendulum import Date, today, instance
from faker import Faker
from unidecode import unidecode
from datetime import datetime

from models import User, Client, Invoice, JobContract, Entity


class Store:

    def __init__(self, seed: int = 0):
        self._seed = seed
        self._faker = Faker(locale="fr_FR", seed=seed)
        self._invoice_sample_size = 10000
        self._user_sample_size = 500
        self._client_sample_size = 100

    

    def _random_date(self) -> Date:
        end_date = today()
        start_date = end_date.subtract(years=2).start_of("year")
        assert end_date > start_date
        return self._random_date_between(start_date, end_date)

    def _random_date_between(self, start_date: Date, end_date: Date | None = None) -> Date:
        date_time = instance(
            datetime.combine(
                self._faker.date_between(start_date=start_date, end_date=end_date),
                datetime.min.time(),
            )
        )
        date = date_time.date()
        return date

    def _list_random_users(self) -> list[User]:
        def iter_users() -> Generator[User, None, None]:
            for _ in range(self._user_sample_size):
                id = self._faker.uuid4()
                first_name = self._faker.first_name()
                last_name = self._faker.last_name()
                email = "%(first_name)s.%(last_name)s@%(domain)s" % {
                    "first_name": unidecode(first_name).lower(),
                    "last_name": unidecode(last_name).lower(),
                    "domain": self._faker.free_email_domain().lower(),
                }

                yield User(
                    id=id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
        return list(iter_users())

    def _list_random_clients(self) -> list[Client]:
        

    def _list_random_invoices(self, clients: list[Client], job_contracts: list[JobContract], sample_size: int = 1000) -> list[Invoice]:
        

    def load_all(self) -> tuple[
        list[User],
        list[JobContract], 
        list[Client],
        list[Invoice],
    ]:
        users = self._list_random_users()
        job_contracts = self._list_random_job_contracts(users=users)
        clients = self._list_random_clients()
        invoices = self._list_random_invoices(clients=clients, job_contracts=job_contracts)
        return (
            users,
            job_contracts,
            clients,
            invoices,
        )