from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal
from pendulum import Date

from .client import Client
from .job_contract import JobContract


@dataclass(eq=True, frozen=True)
class Invoice:

    id: UUID
    client: Client
    job_contract: JobContract
    reference: str
    issue_date: Date
    amount: Decimal