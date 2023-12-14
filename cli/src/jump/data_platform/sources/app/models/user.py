from dataclasses import dataclass
from uuid import UUID


@dataclass(eq=True, frozen=True)
class User:

    id: UUID
    first_name: str
    last_name: str
    email: str