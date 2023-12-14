from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Customer:

    last_name: str
    first_name: str
    email: str | None = None

    satisfaction_score: int | None = None