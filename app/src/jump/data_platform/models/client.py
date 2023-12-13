from dataclasses import dataclass
from uuid import UUID


@dataclass
class Client:

    id: UUID
    name: str