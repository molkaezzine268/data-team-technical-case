from dataclasses import dataclass


@dataclass
class Customer:

    last_name: str
    first_name: str
    email: str | None = None

    satifaction_score: int | None = None