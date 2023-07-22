import aio_pika
import msgpack
from aio_pika.abc import AbstractChannel

from ekf_digital_microservice.server import schemas, dto
from ekf_digital_microservice.server.database.holder import DatabaseHolder


async def create_digests(
        *,
        digests: list[schemas.CreateDigest],
        holder: DatabaseHolder
) -> list[schemas.Digest]:
    digests = await holder.digest.create(
        create_digests=[
            dto.CreateDigest(post_id=digest.post_id) for digest in digests
        ]
    )

    return [schemas.Digest.from_dto(digest=digest) for digest in digests]


async def get_digest(
        *,
        id: int,
        holder: DatabaseHolder
) -> schemas.Digest:
    digest = await holder.digest.read_by_id(id=id)

    return schemas.Digest.from_dto(digest=digest)


async def generate_digests(
        *,
        user_id: int,
        holder: DatabaseHolder,
        rmq_channel: AbstractChannel
) -> None:
    user = await holder.user.read_by_id(id=user_id)

    await rmq_channel.default_exchange.publish(
        message=aio_pika.Message(
            body=msgpack.packb(user.id)
        ),
        routing_key="digests"
    )
