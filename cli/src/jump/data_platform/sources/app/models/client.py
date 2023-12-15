from dataclasses import dataclass
from uuid import UUID


@dataclass(eq=True, frozen=True)
class Client:

    id: UUID
    name: str