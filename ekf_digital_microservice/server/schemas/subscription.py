from pydantic import BaseModel

from ekf_digital_microservice.server import dto


class BaseSubscription(BaseModel):
    source_name: str
    user_id: int


class Subscription(BaseSubscription):
    id: int

    @classmethod
    def from_dto(cls, subscription: dto.Subscription) -> "Subscription":
        return Subscription(
            id=subscription.id,
            source_name=subscription.source_name,
            user_id=subscription.user_id
        )


class CreateSubscription(BaseSubscription):
    pass
