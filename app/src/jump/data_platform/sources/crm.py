from functools import cache
from faker import Faker

from ..models import Customer


class CRM:

    def __init__(self, faker: Faker):
        self._faker = faker

    def list_customers(self) -> list[Customer]:
        return []