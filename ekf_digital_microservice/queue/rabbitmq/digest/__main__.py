import asyncio

import aiohttp
import msgpack
from aio_pika.abc import AbstractIncomingMessage

from ekf_digital_microservice.common import types
from ekf_digital_microservice.common.queue.rabbitmq.factory import rabbitmq_create_connection


async def on_digests(message: AbstractIncomingMessage, session: aiohttp.ClientSession) -> None:
    """
    Получение постов по айди юзера, фильтрация, отправка на главное приложение (бэкенд)

    На бэкенде уже дайджесты записываются в БД
    """
    user_id = msgpack.unpackb(message.body)

    async with session.get(f"/post/by_user_id/{user_id}") as response:
        response.raise_for_status()

        posts = await response.json()

    posts = [{"post_id": post["id"]} for post in posts if post["popularity"] in ["medium", "high"]]

    if not posts:
        await message.ack()
        return

    async with session.post("/digest/", json=posts) as response:
        response.raise_for_status()

    await message.ack()


async def main() -> None:
    settings = types.Settings()

    session = aiohttp.ClientSession(
        base_url=f"http://server:{settings.server_port}",
        headers={"rmq-token": settings.rabbitmq_token}
    )

    connection = await rabbitmq_create_connection(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_client_port,
        login=settings.rabbitmq_login,
        password=settings.rabbitmq_password
    )
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=3)

    queue = await channel.declare_queue("digests")

    await queue.consume(callback=lambda message: on_digests(message=message, session=session))

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
