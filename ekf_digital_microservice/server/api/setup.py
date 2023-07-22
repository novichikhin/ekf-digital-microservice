from fastapi import FastAPI

from ekf_digital_microservice.common import types
from ekf_digital_microservice.server.api.api_v1.dependencies.database import (
    DatabaseEngineMarker,
    DatabaseSessionMarker,
    DatabaseHolderMarker
)
from ekf_digital_microservice.server.api.api_v1.dependencies.setting import SettingsMarker
from ekf_digital_microservice.server.api.api_v1.endpoints.setup import register_routers
from ekf_digital_microservice.server.api.api_v1.exception import register_exceptions
from ekf_digital_microservice.server.core.event import lifespan
from ekf_digital_microservice.server.database.factory import (
    sa_create_engine,
    sa_build_connection_uri,
    sa_create_session_factory,
    sa_create_holder
)


def register_app(settings: types.Settings) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    engine = sa_create_engine(
        connection_uri=sa_build_connection_uri(
            driver=settings.pg_driver,
            host=settings.pg_host,
            port=settings.pg_port,
            user=settings.pg_user,
            password=settings.pg_password,
            db=settings.pg_db
        )
    )
    session_factory = sa_create_session_factory(engine=engine)

    register_routers(app=app)
    register_exceptions(app=app)

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings,
            DatabaseEngineMarker: lambda: engine,
            DatabaseSessionMarker: lambda: session_factory,
            DatabaseHolderMarker: sa_create_holder(session_factory=session_factory)
        }
    )

    return app
