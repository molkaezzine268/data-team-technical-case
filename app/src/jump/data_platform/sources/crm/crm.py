from functools import cache
from faker import Faker
from typing import Generator

from .models import Customer
from ..app.models import User


class CRM:

    def __init__(self, users: list[User], faker: Faker):
        self._users = users
        self._faker = faker

    def list_customers(self) -> list[Customer]:
        def iter_customers() -> Generator[Customer, None, None]:
            for user in self._users:
                last_name = user.last_name
                first_name = user.first_name
                email = user.email
                satisfaction_score = self._faker.pyint(min_value=0, max_value=10) if self._faker.boolean() else None

                yield Customer(
                    last_name=last_name,
                    first_name=first_name,
                    email=email,
                    satisfaction_score=satisfaction_score
                )
        return list(iter_customers())