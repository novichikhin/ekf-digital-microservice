import aio_pika
from aio_pika.abc import AbstractConnection


async def rabbitmq_create_connection(
        *,
        host: str,
        port: int,
        login: str,
        password: str
) -> AbstractConnection:
    return await aio_pika.connect(
        host=host,
        port=port,
        login=login,
        password=password
    )
