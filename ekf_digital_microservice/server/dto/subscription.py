from dataclasses import dataclass


@dataclass
class Subscription:
    id: int
    source_name: str
    user_id: int
