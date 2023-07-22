from ekf_digital_microservice.server import schemas
from ekf_digital_microservice.server.database.holder import DatabaseHolder


async def create_user(
        *,
        user: schemas.CreateUser,
        holder: DatabaseHolder
) -> schemas.User:
    user = await holder.user.create(name=user.name)

    return schemas.User.from_dto(user=user)


async def get_user(
        *,
        id: int,
        holder: DatabaseHolder
) -> schemas.User:
    user = await holder.user.read_by_id(id=id)

    return schemas.User.from_dto(user=user)
