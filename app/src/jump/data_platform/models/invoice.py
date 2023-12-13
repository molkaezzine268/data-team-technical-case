from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

from .client import Client
from .job_contract import JobContract


@dataclass
class Invoice:

    id: UUID
    client: Client
    job_contract: JobContract
    reference: str
    amount: Decimal