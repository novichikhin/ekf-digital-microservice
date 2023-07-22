from ekf_digital_microservice.server import schemas
from ekf_digital_microservice.server.database.holder import DatabaseHolder


async def create_subscription(
        *,
        subscription: schemas.CreateSubscription,
        holder: DatabaseHolder
) -> schemas.Subscription:
    user = await holder.user.read_by_id(id=subscription.user_id)

    subscription = await holder.subscription.create(
        source_name=subscription.source_name,
        user_id=user.id
    )

    return schemas.Subscription.from_dto(subscription=subscription)


async def get_subscription(
        *,
        id: int,
        holder: DatabaseHolder
) -> schemas.Subscription:
    subscription = await holder.subscription.read_by_id(id=id)

    return schemas.Subscription.from_dto(subscription=subscription)
