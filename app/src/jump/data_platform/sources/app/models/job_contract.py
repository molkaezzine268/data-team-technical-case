from dataclasses import dataclass
from pendulum import Date
from uuid import UUID

from .user import User
from .entity import Entity


@dataclass(eq=True, frozen=True)
class JobContract:

    id: UUID
    user: User
    entity: Entity 
    start_date: Date
    end_date: Date | None = None