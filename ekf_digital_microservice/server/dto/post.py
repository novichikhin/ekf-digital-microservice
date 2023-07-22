from dataclasses import dataclass

from ekf_digital_microservice.server import enums


@dataclass
class Post:
    id: int
    subscription_id: int
    body: str
    popularity: enums.Popularity
