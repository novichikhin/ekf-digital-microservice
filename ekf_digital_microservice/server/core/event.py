from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from ekf_digital_microservice.common import types
from ekf_digital_microservice.common.queue.rabbitmq.factory import rabbitmq_create_connection
from ekf_digital_microservice.server.api.api_v1.dependencies.database import DatabaseEngineMarker
from ekf_digital_microservice.server.api.api_v1.dependencies.rabbitmq import RMQChannelMarker
from ekf_digital_microservice.server.api.api_v1.dependencies.setting import SettingsMarker


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: types.Settings = app.dependency_overrides[SettingsMarker]()

    rmq_connection = await rabbitmq_create_connection(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_client_port,
        login=settings.rabbitmq_login,
        password=settings.rabbitmq_password
    )
    rmq_channel = await rmq_connection.channel()

    app.dependency_overrides.update(
        {
            RMQChannelMarker: lambda: rmq_channel
        }
    )

    yield

    engine: AsyncEngine = app.dependency_overrides[DatabaseEngineMarker]()

    await rmq_channel.close()
    await rmq_connection.close()
    await engine.dispose()
